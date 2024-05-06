from pytube import YouTube
import tkinter as tk


class GUI:
	def __init__(self):
		self.url = ""
		self.window = tk.Tk()
		self.frame_main = tk.Frame(master=self.window)
		self.lbl_title = tk.Label(master=self.frame_main, text="Youtube Downloader")
		self.lbl_info = tk.Label(master=self.frame_main, text="Downloads highest quality\nprogressive stream available.")
		self.btn_get = tk.Button(master=self.frame_main, text="Get", command=self._on_download_button_clicked)
		self.fld_url = tk.Entry(master=self.frame_main)
		
		self.frame_main.grid(row=1, column=1)
		self.lbl_title.grid(row=1, column=1)
		self.lbl_info.grid(row=2, column=1)
		self.btn_get.grid(row=1, column=0)
		self.fld_url.grid(row=1, column=1)

	def mainloop(self):
		self.window.mainloop()

	def _on_download_button_clicked(self):
		self.url = self.fld_url.get()
		self.lbl_info["fg"] = "#7A7A00"
		self.lbl_info["text"] = "Download in progress..."
		self.window.update()
		try:
			yt = YouTube(self.url)
			yt.streams.first().download()
			self.lbl_info["fg"] = "#00AA00"
			self.lbl_info["text"] = "Download Complete!"
			self.window.update()
		except Exception as e:
			self.lbl_info["fg"] = "#FF0000"
			self.lbl_info["text"] = "Download Error: Check URL."
			print(e)

if (__name__ == "__main__"):
	app = GUI()
	app.mainloop()

