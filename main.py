# coding=utf-8
""""

Plasma OS Visual

Main file

Made by Plasm inc.

"""
# Imports
import ctypes
import subprocess
import sys
import tkinter as tk
from datetime import datetime
from tkinter import colorchooser

import pygame

from root.System.apps.text import main_start as text_main_start
from root.System.sysModules.plasma_core import *
from root.System.sysModules.settings import *

# Quality
ctypes.windll.shcore.SetProcessDpiAwareness(True)

# Main window
root = tk.Tk()
root.title("Plasma")
root.geometry("1000x500")
root.attributes("-fullscreen", True)
root.iconbitmap("root/System/img/icons/new/plasma.ico")

# Constants
font = "Arial 10"
lang = get_setting("lang")
Version = "2.10"

# Down panel
panel = tk.Frame(root)
panel.pack(side='bottom', fill="x")


def update_time():
    """
    Time updater
    """
    current_time = datetime.now().strftime('%H:%M:%S')
    time.config(text=current_time)
    root.after(1000, update_time)


# Time label
time = tk.Label(panel, font=font)
time.pack(padx=10, side="right")
update_time()


def error(text: str) -> None:
    """
    Dialog window with tada sound
    :param text: text to show user
    """
    err_win = tk.Toplevel(root)
    err_win.title(("Предупреждение" if lang == "ru" else "Warning"))
    err_win.geometry(f"500x120+{(root.winfo_screenwidth() // 2) - 500 // 2}+{(root.winfo_screenheight() // 2) - 120 // 2}")
    err_win.resizable(False, False)
    err_win.attributes("-topmost", True)
    err_win.iconbitmap("root/System/img/icons/new/warning.ico")
    
    # Sound
    pygame.mixer.init()
    pygame.mixer.music.load("root/System/sounds/tada.wav")
    pygame.mixer.music.play()
    
    # Elements
    tk.Label(err_win, text=text, font="Arial 15").place(x=10, y=10)
    tk.Button(err_win, text=("ОК" if lang == "ru" else "OK"), font=font, command=err_win.destroy).place(x=10, y=70)


def parameters() -> None:
    """
    Param window
    """
    global lang
    
    par_win = tk.Toplevel(root)
    par_win.title(("Параметры" if lang == "ru" else "Parameters"))
    par_win.geometry("400x200")
    par_win.resizable(False, False)
    par_win.attributes("-topmost", True)
    par_win.iconbitmap("root/System/img/icons/new/settings.ico")
    
    
    def choice_color() -> None:
        """
        Choice color function for bg
        """
        color: tuple = colorchooser.askcolor(title=("Выбор цвета" if lang == "ru" else "Choice color"))
        save_settings("bg_color", color[1])
        root.configure(bg=color[1])
    
    
    def choice_lang() -> None:
        """""
        Choice language function
        """
        global lang
        if lang == "en":
            lang = "ru"
        elif lang == "ru":
            lang = "en"
        save_settings("lang", lang)
        error(("Перезапустите ОС для применения!" if lang == "ru" else "Restart OS to apply!"))
    
    
    # Param window elements
    tk.Label(par_win, text=("Задний фон" if lang == "ru" else "Background"), font=font).place(x=10, y=5)
    tk.Button(par_win, font=font, text=("Выбор цвета" if lang == "ru" else "Choice color"), command=choice_color).place(x=10, y=30)
    tk.Label(par_win, text=("Язык" if lang == "ru" else "Language"), font=font).place(x=100, y=5)
    tk.Button(par_win, font=font, text=("English" if lang == "ru" else "Русский"), command=choice_lang).place(x=100, y=30)
    
    # Info elements
    tk.Label(par_win, font="Arial 13", text=(f"Plasma OS Visual V {Version}" if lang == "ru" else f"Plasma OS Visual V {Version}")).place(x=10, y=120)
    tk.Label(par_win, font="Arial 13", text=("От Plasm Inc." if lang == "ru" else "By Plasm Inc.")).place(x=10, y=150)


def explorer() -> None:
    """
    Explorer window
    """
    exp_win = tk.Toplevel(root)
    exp_win.title(("Проводник" if lang == "ru" else "Explorer"))
    exp_win.attributes("-topmost", True)
    exp_win.resizable(False, False)
    exp_win.geometry('400x245')
    exp_win.iconbitmap("root/System/img/icons/new/explorer.ico")
    
    # Tk variables
    new_file_name = tk.StringVar(exp_win, "", 'new_name')
    current_path = tk.StringVar(exp_win, "root", 'current_path')
    
    
    def update_path(*event):
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
        rename function
        """
        
        
        def newname():
            """
            Function to rename element
            """
            if ren_new_name == "":
                error("Please enter new name")
            elif ren_file == "":
                error("Please enter file path")
            else:
                ren(ren_file.get(), ren_new_name.get())
                update_path()
                ren_win.destroy()
        
        
        ren_win = tk.Toplevel(exp_win)
        ren_win.title("Переименовать" if lang == "ru" else "Rename")
        ren_win.attributes("-topmost", True)
        ren_win.resizable(False, False)
        ren_win.geometry('300x170')
        ren_win.iconbitmap("root/System/img/icons/new/edit.ico")
        
        # Rename window elements
        ren_new_name = tk.StringVar(ren_win, "", 'ren_new_name')
        ren_file = tk.StringVar(ren_win, gt(current_path.get(), dir_list.get(dir_list.curselection()[0])) if len(dir_list.curselection()) > 0 else "", 'path')
        tk.Label(ren_win, font=font, text=("Введите путь файла для переименования" if lang == "ru" else "Enter the file path for rename")).place(x=10, y=10)
        tk.Entry(ren_win, textvariable=ren_file).place(x=10, y=40)
        tk.Label(ren_win, font=font, text=("Введите новое название" if lang == "ru" else "Enter the new name")).place(x=10, y=70)
        tk.Entry(ren_win, textvariable=ren_new_name).place(x=10, y=100)
        tk.Button(ren_win, font=font, text=("Переименовать" if lang == "ru" else "Rename"), command=newname).place(x=10, y=130)
    
    
    def del_obj():
        """
        Delete window function
        """
        
        
        def del_el():
            """
            Function to rename element
            """
            if del_file_path.get() == "":
                error("Please enter file path")
            else:
                delete(del_file_path.get())
                update_path()
                del_win.destroy()
        
        
        del_win = tk.Toplevel(exp_win)
        del_win.title("Удалить" if lang == "ru" else "Delete")
        del_win.attributes("-topmost", True)
        del_win.resizable(False, False)
        del_win.geometry('300x170')
        del_win.iconbitmap("root/System/img/icons/new/edit.ico")
        
        # Delete window elements
        del_file_path = tk.StringVar(del_win, gt(current_path.get(), dir_list.get(dir_list.curselection()[0])) if len(dir_list.curselection()) > 0 else "", 'path')
        tk.Label(del_win, font=font, text=("Введите путь файла для удаления" if lang == "ru" else "Enter the file path for delete")).place(x=10, y=10)
        tk.Entry(del_win, textvariable=del_file_path).place(x=10, y=40)
        tk.Button(del_win, font=font, text=("Удалить" if lang == "ru" else "Delete"), command=del_el).place(x=10, y=130)
    
    
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
            :param file_path: path to file to touch
            :type file_path: str
            """
            if os.path.isfile(file_path):
                if file_path.endswith(".pea"):
                    subprocess.Popen(file_path)
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
        Goes back in file system
        Cant go outside root directory
        :param event:
        """
        try:
            new_path = gt(current_path.get(), back=True)
            current_path.set(new_path)
        except OSError:  # OSError - cant go outside root directory
            error(("Невозможно выйти за пределы root" if lang == "ru" else "Cant go beyond root directory"))
            pass
    
    
    def window_new_file_or_folder():
        """
        Window to create new file or directory
        """
        new_win = tk.Toplevel(exp_win)
        new_win.geometry("250x100")
        new_win.resizable(False, False)
        new_win.attributes("-topmost", True)
        new_win.title(("Новый объект" if lang == "ru" else "New object"))
        new_win.iconbitmap("root/System/img/icons/new/add.ico")
        
        
        def new_file_or_folder():
            """
            Function to make a new object
            """
            if "." in new_file_name.get():
                cr(gt(current_path.get(), new_file_name.get(), ignore_ex=True))
            else:
                mdir(gt(current_path.get(), new_file_name.get(), ignore_ex=True))
            
            new_win.destroy()
            update_path()
        
        
        # Create new window elements
        tk.Label(new_win, text=("Введите название" if lang == "ru" else "Enter name")).place(x=10, y=5)
        tk.Entry(new_win, textvariable=new_file_name).place(x=10, y=30)
        tk.Button(new_win, text=("Создать" if lang == "ru" else "Create"), command=new_file_or_folder).place(x=10, y=60)
    
    
    def dir_popup(event=None) -> None:
        """
        Explorer only popup menu
        :param event:
        """
        dir_menu.post(event.x_root, event.y_root)
    
    
    # Explorer only popup menu elements
    dir_menu = tk.Menu(tearoff=0)
    dir_menu.add_command(label=("Создать" if lang == "ru" else "Create"), command=window_new_file_or_folder)
    dir_menu.add_command(label=("Переименовать" if lang == "ru" else "Rename"), command=rename)
    dir_menu.add_command(label=("Удалить" if lang == "ru" else "Delete"), command=del_obj)
    dir_menu.add_command(label=("Обновить" if lang == "ru" else "Update"), command=update_path)
    dir_menu.add_command(label=("Назад" if lang == "ru" else "Back"), command=go_back)
    
    # Trace path entry changes
    current_path.trace('w', update_path)
    
    # Explorer elements
    tk.Button(exp_win, text=("Назад" if lang == "ru" else "Back"), command=go_back).place(x=5, y=5)
    
    tk.Entry(exp_win, textvariable=current_path, width=55).place(x=55, y=10)
    
    dir_list = tk.Listbox(exp_win, width=64, selectbackground="#9933FF", height=12)
    dir_list.place(x=5, y=40)
    
    # Hotkey binds
    dir_list.bind('<Double-1>', change_path_by_click)
    dir_list.bind('<Return>', change_path_by_click)
    dir_list.bind('<Button-3>', dir_popup)
    
    update_path()


def term() -> None:
    """
    Run term.pea
    """
    subprocess.Popen("root/System/apps/term.pea", cwd=os.path.dirname(os.path.abspath(__file__)), creationflags=subprocess.CREATE_NEW_CONSOLE)  # TODO make it topmost


def popup(event=None) -> None:
    """
    Main popup menu
    :param event:
    """
    menu.post(event.x_root, event.y_root)


# Main popup menu elements
menu = tk.Menu(tearoff=0)
menu.add_command(label=("Параметры" if lang == "ru" else "Parameters"), command=parameters)
menu.add_command(label=("Завершение работы" if lang == "ru" else "Shutdown"), command=sys.exit)
menu.add_command(label=("Проводник" if lang == "ru" else "Explorer"), command=explorer)
menu.add_command(label=("Командная строка" if lang == "ru" else "Terminal"), command=term)

# Down panel buttons
buttons = [tk.Button(panel, font=font, text=("Параметры" if lang == "ru" else "Parameters"), command=parameters),
           tk.Button(panel, font=font, text=("Завершение работы" if lang == "ru" else "Shutdown"), command=sys.exit),
           tk.Button(panel, font=font, text=("Проводник" if lang == "ru" else "Explorer"), command=explorer),
           tk.Button(panel, font=font, text=("Командная строка" if lang == "ru" else "Terminal"), command=term)]

for button in buttons:
    button.pack(side="left", anchor="sw")

# Main popup menu bind
root.bind("<Button-3>", popup)


def sys_start() -> None:
    """
    Start system and set settings
    """
    global lang
    color = get_setting("bg_color")
    lang = get_setting("lang")
    root.configure(bg=color)
    root.mainloop()


def main():
    """
    Start sys_start and play startup sound
    """
    pygame.mixer.init()
    pygame.mixer.music.load("root/System/sounds/start.wav")
    pygame.mixer.music.play()
    sys_start()


# Main run
if __name__ == '__main__':
    main()
