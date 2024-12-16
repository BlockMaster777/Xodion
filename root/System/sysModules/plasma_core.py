# coding=utf-8
""""

Plasma OS Visual

Plasma OS core module

Made by Plasm inc.

"""
import os
import shutil


def ls(path: str) -> list[str]:
	"""
	List of all objects in directory
	:param path: Directory path to look
	:return: List with objects inside
	"""
	return os.listdir(path)


def cr(path: str) -> None:
	"""
	Create file (NOT DIRECTORY)

	FileExistsError - File is already exists
	ValueError - Invalid file name
	:param path: Path to create FILE
	"""
	if os.path.exists(path):
		raise FileExistsError("File is already exists")

	elif not "." in path:
		raise ValueError("Invalid file name")

	with open(path, "x", encoding="utf-8"):
		pass


def gt(path: str, to: str = "", back: bool = False, ignore_ex: bool = False) -> str:
	"""
	Merge, edit paths

	OSError - cant go beyond root directory
	FileNotFoundError - directory does not exist
	:param ignore_ex: Ignore existing of file. Needs to merge paths
	:param path: Path where to start
	:param to: Directory name to go in
	:param back: Go back in file system
	:return: Returns new path
	"""
	if os.path.exists(path + "\\" + to) and not ignore_ex and not back:
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
	Make directory (NOT FILE)

	FileExistsError - directory with that name already exists
	:param path: Path where to create directory
	"""
	if not os.path.exists(path):
		os.mkdir(path)

	elif os.path.exists(path):
		raise FileExistsError("This directory already exists")


def delete(path: str) -> None:
	"""
	Delete object

	FileNotFoundError - object to delete doesn't exist
	:param path: Path to object to delete
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
	Move file/directory

	FileNotFoundError - Object to move not found/There is no final path
	FileExistsError - The endpoint already has such an object
	:param from_path: Path to object to move
	:param to_path: Path where to move object
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
	Copy object

	FileNotFoundError - Object to move not found/There is no final path
	FileExistsError - The endpoint already has such an object
	:param from_path: Path to object to copy
	:param to_path: Path where to copy object
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
	Rename object
	:param path: Path to object to rename
	:param name: New name (Only name, not path)
	"""
	if not os.path.exists(path):
		raise FileNotFoundError("File not found")
	else:
		os.rename(path, path[0: path.rfind("\\")] + "\\" + name)
