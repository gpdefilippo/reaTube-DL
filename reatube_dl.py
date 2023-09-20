#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  1 22:29:43 2022

@author: ginodefilippo
"""
import os
import sys
from PyQt5 import QtWidgets, QtGui, QtCore
import youtube_dl
import reaper_python as rp


class ReaTubeDl(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.download_url = ""
        self.save_dir = '~/Documents/Reaper/ReaTubeDl/'
        self.color = QtGui.QColor("#5799db")

        self.setup_ui()

    def color_choose(self):
        color = QtWidgets.QColorDialog.getColor(self.color)
        if color.isValid():
            self.color = color

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

    def close(self):
        self.close()

    def setup_ui(self):
        self.setWindowTitle("ReaTubeDl")

        self.url_label = QtWidgets.QLabel("Enter URL:")
        self.url_entry = QtWidgets.QLineEdit()
        self.color_button = QtWidgets.QPushButton("Choose Color")
        self.download_button = QtWidgets.QPushButton("Download")

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.url_label)
        layout.addWidget(self.url_entry)
        layout.addWidget(self.color_button)
        layout.addWidget(self.download_button)

        self.setLayout(layout)

        self.color_button.clicked.connect(self.color_choose)
        self.download_button.clicked.connect(self.download)
        self.url_entry.returnPressed.connect(self.download)

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
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = ReaTubeDl()
    sys.exit(app.exec_())
