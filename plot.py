import matplotlib.pyplot as plt
import numpy as np
import requests
import time
import pygame
from collections import deque
import logging
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

# Set up logging
logging.basicConfig(filename='bark_detections.log', level=logging.INFO, 
                    format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

class DetectionBuffer:
    def __init__(self, buffer_time=120):  # buffer_time in seconds
        self.buffer_time = buffer_time
        self.detections = deque()
        self.last_notification_time = 0

    def add_detection(self, timestamp):
        self.detections.append(timestamp)
        self.clean_old_detections()

    def clean_old_detections(self):
        current_time = time.time()
        while self.detections and current_time - self.detections[0] > self.buffer_time:
            self.detections.popleft()

    def should_notify(self):
        current_time = time.time()
        if len(self.detections) >= 3 and current_time - self.last_notification_time > self.buffer_time:
            self.last_notification_time = current_time
            return True
        return False

class Plotter():
    def __init__(self, win_size=96, n_wins=10, n_bands=64, n_classes=50, msd_labels=None, FIG_SIZE=(8, 8), blit=True, telegram_token=None, channel_id=None):
        # Telegram
        self.n_classes = n_classes
        self.msd_labels = msd_labels
        self.telegram_token = os.getenv('TELEGRAM_TOKEN')
        self.channel_id = os.getenv('CHAT_ID')
        self.play_audio = os.getenv('PLAY_AUDIO')
        
        # Detection buffer
        self.detection_buffer = DetectionBuffer()
        
        # Detection threshold
        self.detection_threshold = 0.2
        self.detected_class_index = 0

        # Detection counter
        self.total_detections = 0

        self.audio_file = os.getenv('AUDIO_FILE_PATH')
        self.max_audio_plays = 5
        self.audio_play_count = 0
        pygame.mixer.init()

    def send_telegram_message(self, message):
        if self.telegram_token and self.channel_id:
            try:
                url = f"https://api.telegram.org/bot{self.telegram_token}/sendMessage?chat_id={self.channel_id}&text={message}"
                response = requests.get(url)
                print(response.json())
            except Exception as e:
                print(f"Failed to send message to Telegram channel. Error: {e}")

    def play_audio_alert(self):
        if self.audio_play_count < self.max_audio_plays:
            pygame.mixer.music.load(self.audio_file)
            pygame.mixer.music.play()
            self.audio_play_count += 1
            logging.info(f"Audio alert played. Play count: {self.audio_play_count}")
        else:
            logging.info("Maximum audio alerts reached. Alert not played.")

    def __call__(self, new_spec_col=None, new_act_col=None):
        if new_act_col[self.detected_class_index, 0] > self.detection_threshold:
            current_time = time.time()
            self.total_detections += 1
            self.detection_buffer.add_detection(current_time)

            if self.detection_buffer.should_notify():
                message = f"Detection event for class '{self.msd_labels[self.detected_class_index]}'!"
                print(message)
                logging.info(f"Notification sent: {message}")
                if self.play_audio:
                    self.play_audio_alert()
                text = "🐶 bark is detected!"
                self.send_telegram_message(text)
            else:
                logging.info(f"Bark detected but notification suppressed. Total detections: {self.total_detections}")

        # Log buffer status periodically (e.g., every 60 seconds)
        if self.total_detections % 60 == 0:
            logging.info(f"Buffer status: {len(self.detection_buffer.detections)} detections in the last {self.detection_buffer.buffer_time} seconds")
