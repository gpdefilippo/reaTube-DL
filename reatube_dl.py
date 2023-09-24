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
import reapy

audio_formats_ext = {'aac': 'm4a', 'alac': 'm4a', 'flac': 'flac', 'm4a': 'm4a', 'mp3': 'mp3', 'opus': 'opus',
                     'vorbis': 'ogg', 'wav': 'wav'}


class ReaTubeDl(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.audio_format = 'mp3'
        self.download_url = 'https://www.youtube.com/watch?v=6JGKY1CX3V0'  # TEMP
        self.project = reapy.Project()  # Might leave this in the init to prevent user switching projects while running
        self.save_dir = self.project.path
        self.out_file = ''
        self.color = QtGui.QColor("#5799db")

        self.setup_ui()

    def color_choose(self):
        color = QtWidgets.QColorDialog.getColor(self.color)
        if color.isValid():
            self.color = color
            self.color_indicator.setStyleSheet(f'background-color: {self.color.name()}')

    def download_add_track(self):
        try:
            self.download_thread = DownloadThread(self)
            self.download_thread.finished.connect(self.on_download_finished)
            self.download_thread.start()
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")
        finally:
            self.close()

    def on_download_finished(self, out_file):
        self.out_file = out_file
        self.add2track()

    def download(self):
        QtCore.QCoreApplication.processEvents()
        self.download_url = self.url_entry.text()
        self.audio_format = self.audio_format_dropdown.currentText()
        out_file = os.path.join(self.save_dir, '%(title)s.%(ext)s')
        ydl_opts = {
            'outtmpl': out_file,
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': self.audio_format,
                'preferredquality': '192',
            }],
            'logger': MyLogger(),
            'progress_hooks': [lambda d: my_hook(d, self.status_bar)],
        }
        self.out_file = download(self.download_url, ydl_opts)

    def add2track(self):
        new_track = self.project.add_track(0, 'YoutubeTrack')
        self.project.cursor_position = 0
        new_track.color = self.color.getRgb()[0:3]
        new_track.make_only_selected_track()
        reapy.reascript_api.InsertMedia(self.out_file, 0)

    def setup_ui(self):
        self.setWindowTitle("ReaTubeDl")

        central_widget = QtWidgets.QWidget()  # Create a central widget
        self.setCentralWidget(central_widget)

        self.status_bar = QtWidgets.QStatusBar()
        self.setStatusBar(self.status_bar)

        # Define items to place in layout
        url_label = QtWidgets.QLabel("Enter Youtube URL:")
        self.url_entry = QtWidgets.QLineEdit()
        self.url_entry.setText(self.download_url)  # Temp along with filled in self.download_url

        audio_format_label = QtWidgets.QLabel("Select Preferred Audio Format:")
        self.audio_format_dropdown = QtWidgets.QComboBox()
        self.audio_format_dropdown.addItems(audio_formats_ext.keys())
        self.audio_format_dropdown.setCurrentIndex(self.audio_format_dropdown.findText('mp3'))

        color_button = QtWidgets.QPushButton("Select Track Color:")
        download_button = QtWidgets.QPushButton("Download")

        self.color_indicator = QtWidgets.QFrame()
        self.color_indicator.setFixedSize(30, 30)  # Set the size of the color indicator
        self.color_indicator.setStyleSheet(f'background-color: {self.color.name()}')  # Set the initial color

        # Define layout with prior items
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(url_label)
        layout.addWidget(self.url_entry)
        color_layout = QtWidgets.QHBoxLayout()
        color_layout.addWidget(color_button)
        color_layout.addWidget(self.color_indicator)  # Add the color indicator to the layout
        layout.addLayout(color_layout)
        audio_format_layout = QtWidgets.QHBoxLayout()
        audio_format_layout.addWidget(audio_format_label)
        audio_format_layout.addWidget(self.audio_format_dropdown)
        layout.addLayout(audio_format_layout)
        layout.addWidget(download_button)

        central_widget.setLayout(layout)

        color_button.clicked.connect(self.color_choose)
        download_button.clicked.connect(self.download_add_track)

        self.show()


class MyLogger:
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


def my_hook(d, status_bar):
    if d['status'] == 'finished':
        status_bar.showMessage("Download finished.")
    elif d['status'] == 'downloading':
        progress = d['_percent_str']
        status_bar.showMessage(f"Downloading: {progress}")


# Create a new class for handling the download in a separate thread
class DownloadThread(QtCore.QThread):
    finished = QtCore.pyqtSignal(str)

    def __init__(self, parent):
        super().__init__()
        self.parent = parent

    def run(self):
        out_file = self.parent.download()
        self.finished.emit(out_file)


def download(url: str, ydl_opts: dict = None):
    with YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        out_filename = ydl.prepare_filename(info_dict)

        new_file_format = ydl.params['postprocessors'][0]['preferredcodec']
        new_file_ext = audio_formats_ext[new_file_format]
        out_filename = out_filename[:-4] + new_file_ext  # Change file type
        return out_filename


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = ReaTubeDl()
    sys.exit(app.exec_())
