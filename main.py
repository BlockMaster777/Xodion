import tkinter as tk
import os
import winsound

# Создаем главное окно
root = tk.Tk()
root.title("Plasma codename Ars")
root.geometry("1000x500")

# Функция для воспроизведения звука
def play_sound():
    winsound.PlaySound("root\\SysRes\\tada.wav", winsound.SND_FILENAME)
    
# Воспроизводим звук
play_sound()

# Нажатие клавиши F11 для полноэкранного режима
def toggle_fullscreen(event):
    root.attributes("-fullscreen", not root.attributes("-fullscreen"))
root.bind("<F11>", toggle_fullscreen)

# Создание окна параметров
def parameters() -> None:
    """"
    Создание окна параметров
    :return:
    
    """
    windowpar = tk.Toplevel(root)
    windowpar.title("Parameters")


    def red():
        root.configure(bg="red")


    def blue():
        root.configure(bg="blue")


    def green():
        root.configure(bg="green")


    # Добавляем элементы в окно
    butpar = tk.Button(windowpar, text="Red", command=red)
    butpar.pack(anchor="nw")
    butpar1 = tk.Button(windowpar, text="Blue", command=blue)
    butpar1.pack(anchor="nw")
    butpar2 = tk.Button(windowpar, text="Green", command=green)
    butpar2.pack(anchor="nw")
    labpar = tk.Label(windowpar, text="Background")
    labpar.pack(side="right", anchor="nw")

# Explorer
def navigate_folder(folder_path):
    rootna = tk.Toplevel(root)
    rootna.title("Explorer")

    def open_element(element):
        new_element_path = os.path.join(folder_path, element)
        if os.path.isdir(new_element_path):
            navigate_folder(new_element_path)
        else:
            try:
                image_window = tk.Toplevel(root)
                image_window.title("Image Viewer")

                image_label = tk.Label(image_window)
                image_label.pack()

                image = tk.PhotoImage(file=new_element_path)
                image_label.config(image=image)
            except tk.TclError:
                with open(new_element_path, "r") as file:
                    file_content = file.read()
                text_area.delete("1.0", tk.END)
                text_area.insert(tk.END, file_content)

    def create_file():
        file_name = file_name_entry.get()
        file_content = file_content_entry.get("1.0", tk.END)

        new_file_path = os.path.join(folder_path, file_name)
        with open(new_file_path, "w") as new_file:
            new_file.write(file_content)

        navigate_folder(folder_path)

    elements = os.listdir(folder_path)
    for element in elements:
        button = tk.Button(root, text=element, command=lambda e=element: open_element(e))
        button.pack()

    menu_bar = tk.Menu(root)
    root.config(menu=menu_bar)

    file_name_label = tk.Label(root, text="File Name:")
    file_name_label.pack()
    file_name_entry = tk.Entry(root)
    file_name_entry.pack()

    file_content_label = tk.Label(root, text="File Content:")
    file_content_label.pack()
    file_content_entry = tk.Text(root, height=5, width=50)
    file_content_entry.pack()

    create_button = tk.Button(root, text="Create File", command=create_file)
    create_button.pack()

    text_area = tk.Text(root, height=10, width=50)
    text_area.pack()

    if folder_path != "root":
        parent_button = tk.Button(root, text="Back", command=lambda: navigate_folder(os.path.dirname(folder_path)))
        parent_button.pack()

    root.mainloop()
 
# Создание окна информации о системе
def inf():
    wininf = tk.Toplevel(root)
    wininf.title("Information")
    
    # Добавление ресурсов в окно
    labinf = tk.Label(wininf, text="Plasma V2.0")
    labinf.pack()

#Создание кнопок на панели управления
buttons = [tk.Button(root, text="Parameters", command=parameters) , tk.Button(root, text="Information", command=inf) , tk.Button(root, text="Shut down", command=exit)]
for button in buttons:
    button.pack(side="left", anchor="sw")

def explorer():
    navigate_folder("root")

#Кнопка пля показа папок
rootbutton = tk.Button(root, text='Explorer', command=explorer)
rootbutton.place(x=10, y=40)

# Запускаем главный цикл обработки событий
root.mainloop()
