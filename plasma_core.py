# coding=utf-8
""""
Plasma OS core
"""
import os
import shutil


def ls(path: str) -> list[str]:
	"""
	ls func
	:param path:
	:return:
	"""
	return os.listdir(path)


def cr(path: str) -> None:
	"""
	cr func
	:param path:
	"""
	if os.path.exists(path):
		raise FileExistsError("File is already exists")

	elif not "." in path:
		raise ValueError("Invalid file name")

	with open(path, "x", encoding="utf-8"):
		pass



def gt(path:str, to: str="", back: bool = False, ignore_ex: bool = False) -> str:
	"""
	gt func
	:param ignore_ex:
	:param path:
	:param to:
	:param back:
	:return:
	"""
	if os.path.exists(path + "\\" + to) and (not ignore_ex) and not back:
		return path + "\\" + to

	if ignore_ex and not back:
		return path + "\\" + to

	elif back and path != "root":
		return path[0: path.rfind("\\")]

	elif back and path == "root":
		raise OSError("Cannot go beyond root directory")

	elif not os.path.exists(path):
		raise FileNotFoundError("Directory does not exist")


def mdir(path: str) -> None:
	"""
	mdir func
	:param path:
	"""
	if not os.path.exists(path):
		os.mkdir(path)

	elif os.path.exists(path):
		raise FileExistsError("This directory already exists")


def delete(path: str) -> None:
	"""
	del func
	:param path:
	"""
	if os.path.exists(path):
		if os.path.isfile(path):
			os.remove(path)
		else:
			shutil.rmtree(path)

	elif not os.path.exists(path):
		raise FileNotFoundError("This object does not exist")


def mv(from_path: str, to_path: str) -> None:
	"""
	mv func
	:param from_path:
	:param to_path:
	"""
	if not os.path.exists(from_path):
		raise FileNotFoundError("File not found")

	elif os.path.exists(to_path):
		raise FileExistsError("The endpoint already has such a file")

	elif not os.path.exists(to_path[0: to_path.rfind("\\")]):
		raise FileNotFoundError("There is no final path")

	else:
		shutil.move(from_path, to_path)


def copy(from_path: str, to_path: str) -> None:
	"""
	copy func
	:param from_path:
	:param to_path:
	"""
	if not os.path.exists(from_path):
		raise FileNotFoundError("File not found")

	elif os.path.exists(to_path):
		raise FileExistsError("The endpoint already has such a file")

	elif not os.path.exists(to_path[0: to_path.rfind("\\")]):
		raise FileNotFoundError("There is no final path")

	else:
		shutil.copy(from_path[1], to_path[2])


def ren(path: str, name: str) -> None:
	"""
	ren func
	:param path:
	:param name:
	"""
	if not os.path.exists(path):
		raise FileNotFoundError("File not found")
	else:
		os.rename(path, path[0: path.rfind("\\")] + "\\" + name)
