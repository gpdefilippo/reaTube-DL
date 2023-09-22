#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  1 22:29:43 2022

@author: ginodefilippo
"""
from __future__ import unicode_literals
import os
import sys
from PyQt5 import QtWidgets, QtGui, QtCore
from yt_dlp import YoutubeDL
import reaper_python as rp


class ReaTubeDl(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.download_url = 'https://www.youtube.com/watch?v=6JGKY1CX3V0'  # TEMP
        self.save_dir = '/Users/ginodefilippo/Documents/REAPER/ReaTubeDl'
        self.color = QtGui.QColor("#5799db")

        self.setup_ui()

    def color_choose(self):
        color = QtWidgets.QColorDialog.getColor(self.color)
        if color.isValid():
            self.color = color
            self.color_indicator.setStyleSheet(f'background-color: {self.color.name()}')

    def download(self):
        self.download_url = self.url_entry.text()
        out_file = os.path.join(self.save_dir, '%(title)s.%(ext)s')
        ydl_opts = {
            'outtmpl': out_file,
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'logger': MyLogger(),
            'progress_hooks': [my_hook],
        }
        download_url(self.download_url, ydl_opts)
        self.close()

    def setup_ui(self):
        self.setWindowTitle("ReaTubeDl")

        # Define items to place in layout
        self.url_label = QtWidgets.QLabel("Enter Youtube URL:")
        self.url_entry = QtWidgets.QLineEdit()
        self.url_entry.setText(self.download_url)  # Temp along with filled in self.download_url
        self.color_button = QtWidgets.QPushButton("Select Track Color:")
        self.download_button = QtWidgets.QPushButton("Download")

        self.color_indicator = QtWidgets.QFrame()
        self.color_indicator.setFixedSize(30, 30)  # Set the size of the color indicator
        self.color_indicator.setStyleSheet(f'background-color: {self.color.name()}') # Set the initial color

        # Define layout with prior items
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.url_label)
        layout.addWidget(self.url_entry)
        color_layout = QtWidgets.QHBoxLayout()
        color_layout.addWidget(self.color_button)
        color_layout.addWidget(self.color_indicator)  # Add the color indicator to the layout
        layout.addLayout(color_layout)
        layout.addWidget(self.download_button)

        self.setLayout(layout)

        self.color_button.clicked.connect(self.color_choose)
        self.download_button.clicked.connect(self.download)
        # self.url_entry.returnPressed.connect(self.download)

        self.show()


class MyLogger():
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')


def download_url(url: str, ydl_opts: dict = None):
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = ReaTubeDl()
    sys.exit(app.exec_())
