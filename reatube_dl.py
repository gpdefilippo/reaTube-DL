#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  1 22:29:43 2022

@author: ginodefilippo
"""
from __future__ import unicode_literals
import os
import tkinter as tk
from tkinter import colorchooser
import youtube_dl
import reaper_python as rp

class ReaTubeDl:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.download_url = ""
        self.save_dir = '~/Documents/Reaper/ReaTubeDl/'
        self.color = "#5799db"

        self.setup_tk()
    
    def color_choose(self):
        self.color = colorchooser.askcolor(self.color)

    def on_return(self, event):
        self.download_url = self.e.get()
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
        # --extract-audio, --audio-format "mp3"
        # -o 'self.save_dir/%(playlist)s/%(chapter_number)s - %(chapter)s/%(title)s.%(ext)s'
        self.root.destroy()

    def close(self, event):
        self.root.quit()
        self.root.destroy()
 
    def setup_tk(self):
        self.e = tk.Entry(root)
        self.e.pack()
        self.b = tk.Button(root, text='Choose Color',command=self.color_choose)
        self.b.pack(side="left")
        
        self.e.bind("<Return>", self.on_return)
        self.root.bind("<Escape>", self.close)
        
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
        
def download_url(url: str, ydl_opts: dict=None):
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])       

root = tk.Tk()

readown = ReaTubeDl(root)
root.mainloop()
