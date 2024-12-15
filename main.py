# coding=utf-8
""""

Plasma OS Visual

Made by Plasm inc.

"""
import ctypes
import subprocess
import tkinter as tk
from datetime import datetime
from tkinter import colorchooser

import pygame

from plasma_core import *
from root.System.apps.text import main_start as text_main_start
from settings import *

ctypes.windll.shcore.SetProcessDpiAwareness(True)

root = tk.Tk()
root.title("Plasma")
root.geometry("1000x500")
root.attributes("-fullscreen", True)
root.iconbitmap("root/System/icons/plasma.ico")

font = "Arial 10"
lang = get_setting("lang")

panel = tk.Frame(root)
panel.pack(side='bottom', fill="x")


def shd():
	pygame.mixer.init()
	pygame.mixer.music.load("root\\System\\sounds\\tada.wav")
	pygame.mixer.music.play()
	quit()


def update_time():
	"""
	Time updater
	"""
	current_time = datetime.now().strftime('%H:%M:%S')
	time.config(text=current_time)
	root.after(1000, update_time)


time = tk.Label(panel, font=font)
time.pack(padx=10, side="right")
update_time()


def parameters() -> None:
	"""
	Param window
	"""
	global lang

	window_par = tk.Toplevel(root)
	window_par.title(("Параметры" if lang == "ru" else "Parameters"))
	window_par.geometry("300x100")
	window_par.resizable(False, False)
	window_par.attributes("-topmost", True)
	window_par.iconbitmap("root/System/icons/settings.ico")


	def choice_color() -> None:
		"""
		Choice color
		"""
		color: tuple = colorchooser.askcolor(title=("Выбор цвета" if lang == "ru" else "Choice color"))
		save_settings("bg_color", color[1])
		root.configure(bg=color[1])


	def choice_lang() -> None:
		"""""
		Choice language
		"""
		global lang

		if lang == "en":
			lang = "ru"
		if lang == "ru":
			lang = "en"
		save_settings("lang", lang)


	tk.Label(window_par, text=("Задний фон" if lang == "ru" else "Background"), font=font).place(x=10, y=5)
	tk.Button(window_par, font=font, text=("Выбор цвета" if lang == "ru" else "Choice color"),
	          command=choice_color).place(x=10, y=30)
	tk.Label(window_par, text=("Язык" if lang == "ru" else "Language"), font=font).place(x=100, y=5)
	tk.Label(window_par, text=("Перезапустите для применения" if lang == "ru" else "Restart to apply"),
	         font=font).place(x=100, y=55)
	tk.Button(window_par, font=font, text=("English" if lang == "ru" else "Русский"), command=choice_lang).place(x=100,
	                                                                                                             y=30)


def info() -> None:
	"""
	Info window
	"""
	global lang
	inf_win = tk.Toplevel(root)
	inf_win.title(("Информация" if lang == "ru" else "Information"))
	inf_win.geometry("300x50")
	inf_win.resizable(False, False)
	inf_win.attributes("-topmost", True)
	inf_win.iconbitmap("root/System/icons/info.ico")
	tk.Label(inf_win, font=font, text=(
		"Plasma OS Visual V 2.6.5\nОт Plasm Inc." if lang == "ru" else "Plasma OS Visual\nV 2.6.5\nBy Plasm Inc.")).pack()


#
# def pd():
# 	pygame.mixer.init()
# 	pygame.mixer.music.load("root\\System\\sounds\\PapiniDochki.wav")
# 	pygame.mixer.music.play()

def explorer() -> None:
	"""
	Explorer window
	"""
	exp_win = tk.Toplevel(root)
	exp_win.title(("Проводник" if lang == "ru" else "Explorer"))
	exp_win.attributes("-topmost", True)
	exp_win.resizable(False, False)
	exp_win.geometry('400x250')
	exp_win.iconbitmap("root/System/icons/explorer.ico")

	new_file_name = tk.StringVar(exp_win, "", 'new_name')
	current_path = tk.StringVar(exp_win, "root", 'current_path')


	def path_change(*event):
		"""
		Path changer
		:param event:
		"""
		directory = ls(current_path.get())
		dir_list.delete(0, tk.END)

		for file in directory:
			dir_list.insert(0, file)


	def rename():
		"""
		rename func
		"""


		def newname():
			ren(ren_file.get(), ren_new_name.get())
			path_change(ren_file.get())


		ren_win = tk.Toplevel(exp_win)
		ren_win.title("Переименовать" if lang == "ru" else "Rename")

		ren_new_name = tk.StringVar(ren_win, "", 'ren_new_name')
		ren_file = tk.StringVar(ren_win, "", 'path')
		ren_path_label = tk.Label(ren_win, font=font, text=(
			"Введите путь файла для переименования" if lang == "ru" else "Enter the file path for rename"))
		ren_path_label.pack()
		ren_entry_file = tk.Entry(ren_win, textvariable=ren_file)
		ren_entry_file.pack()
		ren_label_name = tk.Label(ren_win, font=font,
		                          text=("Введите новое название" if lang == "ru" else "Enter the new name"))
		ren_label_name.pack()
		ren_entry_name = tk.Entry(ren_win, textvariable=ren_new_name)
		ren_entry_name.pack()
		ren_button = tk.Button(ren_win, font=font, text=("Переименовать" if lang == "ru" else "Rename"),
		                       command=newname)
		ren_button.pack()


	def change_path_by_click(*event):
		"""
		Changes path by clicking on element
		:param event:
		"""
		picked = dir_list.get(dir_list.curselection()[0])
		path = gt(current_path.get(), picked)


		def touch(file_path: str) -> None:
			"""
			Open/Run file
			:param file_path:
			:type file_path:
			"""
			if os.path.isfile(file_path):
				if file_path.endswith(".pea"):
					subprocess.run(file_path)
				elif file_path.endswith(".lnk"):
					with open(file_path, encoding="utf-8") as f:
						touch(f.readlines()[0].rstrip())
				else:
					text_main_start(file_path, False)
			else:
				current_path.set(file_path)


		touch(path)


	def go_back(*event):
		"""
		Goes back in files
		:param event:
		"""
		try:
			new_path = gt(current_path.get(), back=True)
			current_path.set(new_path)
		except OSError:
			pass


	def window_new_file_or_folder():
		"""
		Window to create new file
		"""
		# global new_win
		new_win = tk.Toplevel(exp_win)
		new_win.geometry("250x100")
		new_win.resizable(False, False)
		new_win.attributes("-topmost", True)
		new_win.title(("Новый объект" if lang == "ru" else "New object"))


		def new_file_or_folder():
			"""
			Func that makes a new object
			"""
			if "." in new_file_name.get():
				cr(gt(current_path.get(), new_file_name.get(), ignore_ex=True))
			else:
				mdir(gt(current_path.get(), new_file_name.get(), ignore_ex=True))

			new_win.destroy()
			path_change()


		tk.Label(new_win, text=("Введите название" if lang == "ru" else "Enter name")).place(x=10, y=5)
		tk.Entry(new_win, textvariable=new_file_name).place(x=10, y=30)
		tk.Button(new_win, text=("Создать" if lang == "ru" else "Create"), command=new_file_or_folder).place(x=10, y=60)


	def dir_popup(event=None) -> None:
		"""
		Popup menu
		:param event:
		"""
		dir_menu.post(event.x_root, event.y_root)


	dir_menu = tk.Menu(tearoff=0)
	dir_menu.add_command(label=("Переименовать" if lang == "ru" else "Rename"), command=rename)
	dir_menu.add_command(label=("Создать" if lang == "ru" else "Create"), command=window_new_file_or_folder)
	dir_menu.add_command(label=("Назад" if lang == "ru" else "Back"), command=go_back)

	current_path.trace('w', path_change)

	tk.Button(exp_win, text=("Назад" if lang == "ru" else "Back"), command=go_back).place(x=5, y=5)

	tk.Entry(exp_win, textvariable=current_path).place(x=65, y=10)

	dir_list = tk.Listbox(exp_win)
	dir_list.place(x=5, y=40)

	dir_list.bind('<Double-1>', change_path_by_click)
	dir_list.bind('<Return>', change_path_by_click)
	dir_list.bind('<Button-3>', dir_popup)

	path_change("root")


def popup(event=None) -> None:
	"""
	Popup menu
	:param event:
	"""
	menu.post(event.x_root, event.y_root)


menu = tk.Menu(tearoff=0)
menu.add_command(label=("Параметры" if lang == "ru" else "Parameters"), command=parameters)
menu.add_command(label=("Информация" if lang == "ru" else "Information"), command=info)
menu.add_command(label=("Завершение работы" if lang == "ru" else "Shutdown"), command=shd)
menu.add_command(label=("Проводник" if lang == "ru" else "Explorer"), command=explorer)

# Создание кнопок на панели управления
buttons = [tk.Button(panel, font=font, text=("Параметры" if lang == "ru" else "Parameters"), command=parameters),
           tk.Button(panel, font=font, text=("Информация" if lang == "ru" else "Information"), command=info),
           tk.Button(panel, font=font, text=("Завершение работы" if lang == "ru" else "Shutdown"), command=shd),
           tk.Button(panel, font=font, text=("Проводник" if lang == "ru" else "Explorer"), command=explorer)]

for button in buttons:
	button.pack(side="left", anchor="sw")

root.bind("<Button-3>", popup)


def sys_start() -> None:
	"""
	Main
	"""
	global lang
	color = get_setting("bg_color")
	lang = get_setting("lang")
	root.configure(bg=color)
	root.mainloop()


def main():
	pygame.mixer.init()
	pygame.mixer.music.load("root\\System\\sounds\\start.wav")
	pygame.mixer.music.play()
	sys_start()


if __name__ == '__main__':
	main()
