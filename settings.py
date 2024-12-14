# coding=utf-8
""""
Settings module
"""
def save_settings(setting: str, val: int or str) -> None:
	""""
	Save settings in settings.properties
	:param val:
	:param setting:
	"""
	with open("root/System/settings.properties", encoding="utf-8") as f:
		lines = f.readlines()
		for i, line in enumerate(lines):
			if line.startswith(setting + '='):
				lines[i] = f"{setting}={val}\n"
				break

	with open("root/System/settings.properties", "w", encoding="utf-8") as f:
		f.writelines(lines)


def get_setting(setting: str) -> str:
	""""
	Get setting in settings.properties
	:param setting:
	"""
	with open("root/System/settings.properties", encoding="utf-8") as f:
		lines = f.readlines()
		for i, line in enumerate(lines):
			line_s = line.split("=")
			if line_s[0] == setting:
				return line_s[1].rstrip()
