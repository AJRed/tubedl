 
from pytube import YouTube
import ffmpeg
import tkinter as tk

def getText():
    url = urlbox.get()
    yt = YouTube(url)
    yt.streams.first().download()



window = tk.Tk()

frame_main = tk.Frame(master=window)
frame_main.grid(row=1, column=1)

title = tk.Label(master=frame_main, text="YouTube Download")
title.grid(row=0, column=1)

urlbox = tk.Entry(master=frame_main)
urlbox.grid(row=1, column=1)

btn_get = tk.Button(master=frame_main, text="get", command=getText)
btn_get.grid(row=1, column=0)

lbl_desc = tk.Label(master=frame_main, text="Downloads highest quality\n progressive stream available")
lbl_desc.grid(row=2, column=1)




window.mainloop()


#video = yt.streams.get_by_itag('251').download()




