from pytube import YouTube
import tkinter as tk
from tkinter import ttk


class GUI:
	def __init__(self):
		self.url = ""
		# Create components
		self.window = tk.Tk()
		self.menu_bar = tk.Menu(master=self.window)
		self.file_menu = tk.Menu(self.menu_bar, tearoff=False)
		self.edit_menu = tk.Menu(self.menu_bar, tearoff=False)
		self.help_menu = tk.Menu(self.menu_bar, tearoff=False)
		self.prefs_menu = tk.Menu(self.file_menu, tearoff=0)
		self.frame_main = tk.Frame(master=self.window)
		self.lbl_title = tk.Label(master=self.frame_main,
							text="Youtube Downloader")
		self.lbl_info = tk.Label(master=self.frame_main,
						   text="Downloads highest quality\nprogressive stream available.")
		self.btn_get = tk.Button(master=self.frame_main,
						   text="Get", command=self._on_download_button_clicked)
		self.fld_url = tk.Entry(master=self.frame_main)

		# Window setup
		self.window.title("TubeDL")
		self.window.geometry("320x150")

		# Menu bar setup
		self.window.configure(menu=self.menu_bar)
		self.menu_bar.add_cascade(
			label="File",
			menu=self.file_menu,
			underline=0,
		)
		self.menu_bar.add_cascade(
			label="Edit",
			menu=self.edit_menu,
			underline=0
		)
		self.menu_bar.add_cascade(
			label="Help",
			menu=self.help_menu,
			underline=0
		)

		# File menu
		self.file_menu.add_cascade(
			label="Preferences",
			underline=0
		)
		self.file_menu.add_command(
			label="Exit",
			command=self.window.destroy,
			underline=1
		)

		# Edit menu

		# Help menu
		self.help_menu.add_command(
			label="About",
			command=self._on_about_pressed
		)
		
		# Prefs sub-menu
		self.prefs_menu.add_command(label="Keyboard Shortcuts")
		self.prefs_menu.add_command(label="Color Themes")

		# Layout
		
		self.frame_main.grid(row=1, column=1)
		self.lbl_title.grid(row=2, column=1)
		self.lbl_info.grid(row=3, column=1)
		self.btn_get.grid(row=2, column=0)
		self.fld_url.grid(row=2, column=1)

	
	def _key_handler(self, event):
		match event.keycode:
			case 9:
				self.window.destroy()
			case 36:
				self._on_download_button_clicked()
			case _:
				print("Key Unhandled")
		print(event.char, event.keysym, event.keycode)
	

	def start(self):
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

	def _on_about_pressed(self):
		pass

	def _on_preferences_pressed(self):
		pass


if (__name__ == "__main__"):
	app = GUI()
	app.window.bind("<Key>", app._key_handler)
	app.start()

