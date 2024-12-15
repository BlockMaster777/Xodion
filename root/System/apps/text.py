# coding=utf-8
""""

-PlasmaText-

by Plasm inc.

"""
import re
import tkinter
from tkinter import *
from tkinter.filedialog import askopenfile
from tkinter.filedialog import asksaveasfile

prText = ""


def main_start(path: str, is_new: bool) -> None:
	"""
	Main ppa function
	:param is_new:
	:type is_new:
	:param path:
	:type path:
	"""
	text_ed_win = tkinter.Tk()
	text_ed_win.geometry("700x500")
	text_ed_win.title("PlasmaText")
	text_ed_win.attributes("-topmost", True)
	text_ed_win.iconbitmap("root/System/icons/plasmtext.ico")
	prText = ""

	BGc = "#160b34"
	TEXTc = "#7fd788"
	COMMENTc = "#2e528b"
	STRc = "#d8f061"
	SPECc = "#7000e0"
	font = "Consolas 13"

	repl = [["""(^| )(and|as|assert|break|class|continue|def|del|elif|else|except|False|finally|for|from|global|import
			|if|in|is|lambda|None|nonlocal|not|or|pass|raise|return|True|try|while|with|yield|_|case|match|type)($| )""",
	         SPECc], ['".*?"', STRc], ['\".*?\"', STRc], ['#.*?$', COMMENTc], ]

	editarea = Text(text_ed_win, background=BGc, foreground=TEXTc, insertbackground="#ffffff", relief=FLAT,
	                borderwidth=2, font=font)

	editarea.pack(fill=BOTH, expand=1)


	def changes(*event) -> None:
		""""
		Changes
		"""
		global prText
		if editarea.get("1.0", END) == prText:
			return

		for tag in editarea.tag_names():
			editarea.tag_remove(tag, "1.0", "end")

		i = 0
		for pattern, color in repl:
			for start, end in search_re(pattern, editarea.get("1.0", END)):
				editarea.tag_add(str(i), start, end)
				editarea.tag_config(str(i), foreground=color)

				i += 1

		prText = editarea.get("1.0", END)


	def search_re(pattern, text):
		"""
		Search with re
		:param pattern:
		:param text:
		:return:
		"""
		matches = []
		text = text.splitlines()

		for i, line in enumerate(text):
			for ma in re.finditer(pattern, line):
				matches.append((f"{i + 1}.{ma.start()}", f"{i + 1}.{ma.end()}"))

		return matches


	def open_with(path: str) -> None:
		"""
		Needs to open files from Plasma VS
		"""
		with open(path, encoding="utf-8") as f:
			editarea.delete(1.0, END)
			for i in f.readlines():
				editarea.insert(END, i)
		changes()


	def open_file(*event) -> None:
		"""
		Open file dialog
		"""
		try:
			file = askopenfile()
			editarea.delete(1.0, END)
			for i in file:
				editarea.insert(END, i)
		except BaseException:
			pass
		changes()


	def save_file(*event) -> None:
		"""
		Save file dialog
		"""
		file = asksaveasfile(defaultextension=".txt")
		file.write(editarea.get(1.0, END))


	editarea.bind("<KeyPress>", changes)
	editarea.bind("<KeyRelease>", changes)
	editarea.bind("<Control-o>", open_file)
	editarea.bind("<Control-s>", save_file)

	if not is_new:
		open_with(path)

# def run(*event) -> None:
# 	"""
# 	Run the code
# 	:param event:
# 	"""
# 	with open("run.py", "w", encoding="utf-8") as f:
# 		f.write(editarea.get("1.0", END))
#
# 	os.system('start cmd /K "python run.py"')

#
