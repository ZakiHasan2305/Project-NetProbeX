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
from constants import get_wireshark_file_path
wireshark_file_path = get_wireshark_file_path()
from random import randint
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QProgressBar, QLabel, QListWidgetItem
from PyQt5.QtGui import QPainter, QBrush, QColor
from PyQt5.QtCore import Qt
from scapy.all import *
import math
from kivy.clock import Clock



class Home(App):
    def build(self):
        root = FloatLayout(size=(800, 800))

        # Background Image
        bg_image = Image(source='image.png', allow_stretch=True, keep_ratio=False, size=(800,800))
        root.add_widget(bg_image)

        # Adding close button
        close_button = Button(text='Close', size_hint=(0.2, 0.1), pos_hint={'right': 1, 'top': 1})
        close_button.bind(on_press=self.confirm_close)
        root.add_widget(close_button)


        

        # Sidebar
    
        sidebar_button = Button(text='≡', size_hint=(None, None), size=(100, 100), pos_hint = {'left' : 1, 'top': 0.998})
        sidebar_button.bind(on_release=self.show_sidebar)
        

        root.add_widget(sidebar_button)
        return root
    def confirm_close(self, instance):
        content = BoxLayout(orientation='vertical')
        content.add_widget(Label(text='Are you sure you want to close the application?'))

        # Create "Yes" button to close the app
        yes_button = Button(text='Yes', size_hint=(1, None), height=40)
        yes_button.bind(on_press=self.close_app)
        content.add_widget(yes_button)

        # Create "No" button to cancel
        no_button = Button(text='No', size_hint=(1, None), height=40)
        content.add_widget(no_button)

        # Create Popup
        popup = Popup(title='Confirmation', content=content, size_hint=(None, None), size=(450, 300))
        popup.open()

        # Bind "No" button to dismiss the popup
        no_button.bind(on_press=popup.dismiss)

    def close_app(self, instance):
        App.get_running_app().stop()

    def show_sidebar(self, instance):
        # Popup for Sidebar
        content = BoxLayout(orientation='vertical')
        task1_label = Button(text='Basic Information')
        task2_label = Button(text='Byte Analysis')
        task3_label = Button(text='Start a Session')
        task4_label = Button(text='Packet Analysis')
        task5_label = Button(text='Attack Detetction')
        task6_label = Button(text='Update File Path')

        task1_label.bind(on_press=self.personal_infortation)
        task2_label.bind(on_press=self.open_visualaid)  # Binding the function to Task 2
        task3_label.bind(on_press=self.open_wireshark)
        task4_label.bind(on_press=self.performace_analysis)
        task5_label.bind(on_press=self.filter_analysis_win)
        task6_label.bind(on_press=self.update_filepath)


        content.add_widget(task3_label)
        content.add_widget(task6_label)
        content.add_widget(task1_label)
        content.add_widget(task2_label)
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

    def personal_infortation(self,instance):
        try:
            subprocess.Popen(['python','packetsandlinks.py'])
        except Exception as e:
            print(f"Error occured while launcing packetsandlinks.py: {e}")

    def performace_analysis(self,instance):
        try:
            subprocess.Popen(['python','performanceAnalysis.py'])
        except Exception as e:
            print(f"Error occured while launcing performanceAnalysis.py: {e}")
    
    def open_wireshark(self,instance):
        try:
            subprocess.Popen(['python','open_wireshark.py'])
        except Exception as e:
            print(f"Error occured while launcing open_wireshark.py: {e}")

    def update_filepath(self,instance):
        try:
            subprocess.Popen(['python','update_wireshark_path.py'])
        except Exception as e:
            print(f"Error occured while launcing update_wireshark_path.py.py: {e}")


if __name__ == "__main__":
    Home().run()
