import kivy
import subprocess
import os
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QMessageBox, QLabel
from PySide6.QtCore import QTimer, Qt
import pyqtgraph as pg
from constants import wireshark_file_path
from random import randint
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QProgressBar, QLabel, QListWidgetItem
from PyQt5.QtGui import QPainter, QBrush, QColor
from PyQt5.QtCore import Qt
from scapy.all import *
import math
from kivy.clock import Clock



class Home(App):
    def build(self):
        root = FloatLayout()

        # Background Image
        bg_image = Image(source='image.png', allow_stretch=True, keep_ratio=False, size=(400,400))
        root.add_widget(bg_image)

        

        # Sidebar
    
        sidebar_button = Button(text='≡', size_hint=(None, None), size=(100, 100), pos_hint = {'left' : 1, 'top': 0.998})
        sidebar_button.bind(on_release=self.show_sidebar)
        

        root.add_widget(sidebar_button)
        return root

    def show_sidebar(self, instance):
        # Popup for Sidebar
        content = BoxLayout(orientation='vertical')
        task1_label = Button(text='Personal Information')
        task2_label = Button(text='Visual Aid')
        task3_label = Button(text='WireShark Demo')
        task4_label = Button(text='Transfer Speed/Packets')
        task5_label = Button(text='Entropy Calculations')

        task2_label.bind(on_press=self.open_visualaid)  # Binding the function to Task 2
        task5_label.bind(on_press=self.filter_analysis_win)

        content.add_widget(task1_label)
        content.add_widget(task2_label)
        content.add_widget(task3_label)
        content.add_widget(task4_label)
        content.add_widget(task5_label)

        popup = Popup(title='Menu', content=content, size_hint=(None, 1), width=350)
        popup.open()

    def open_visualaid(self, instance):
        try:
            subprocess.Popen(['python', 'visualaid.py'])  # Launch visualaid.py script
        except Exception as e:
            print(f"Error occurred while launching visualaid.py: {e}")

    def filter_analysis_win(self, instance):
        try:
            subprocess.Popen(['python', 'filter_analysis_win.py'])
        except Exception as e:
            print(f"Error occurred while launching filter_analysis_win.py: {e}")


if __name__ == "__main__":
    Home().run()
