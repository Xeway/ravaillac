import os
from tkinter import filedialog, StringVar
import customtkinter
import ravaillac


def open_file():
    global file_path
    tmp = file_path
    file_path = filedialog.askopenfilename()
    if not file_path and tmp:
        file_path = tmp

    if file_path and size_limit.get().isdecimal():
        selected_file.configure(text=file_path)
        confirm_split_button.configure(state="normal")
    else:
        if file_path:
            selected_file.configure(text=file_path)
        else:
            selected_file.configure(text="No file selected.")

        if confirm_split_button.cget("state") == "normal":
            confirm_split_button.configure(state="disabled")


def size_limit_modified(*_):
    if file_path and size_limit.get().isdecimal():
        confirm_split_button.configure(state="normal")
    elif confirm_split_button.cget("state") == "normal":
        confirm_split_button.configure(state="disabled")
    return True


def confirm_split_file():
    sl = size_limit.get()
    if file_path and sl.isdecimal():
        split_file_status.configure(text="Ongoing operation...")
        result_path = ravaillac.split_file(file_path, int(sl))
        if result_path:
            split_file_status.configure(text_color="green")
            split_file_status.configure(text=f"Operation succeeded. Result path: {result_path}")
        else:
            split_file_status.configure(text_color="red")
            split_file_status.configure(text="Operation failed.")


root = customtkinter.CTk()

root.geometry("500x370")
root.title("Ravaillac")

size_limit = StringVar()
size_limit.trace_add("write", size_limit_modified)
file_path = None
directory_path = None

tabview = customtkinter.CTkTabview(root, width=450, height=346)
tabview.pack()
split_tab = tabview.add("Split a file")
merge_tab = tabview.add("Merge fragments")

label_file_path = customtkinter.CTkLabel(master=split_tab, text="Choose a file to split")
label_file_path.pack(pady=10)
button_file_path = customtkinter.CTkButton(master=split_tab,
                                           text="Open",
                                           fg_color="purple3",
                                           hover_color="purple4",
                                           command=open_file)
button_file_path.pack()
selected_file = customtkinter.CTkLabel(master=split_tab,
                                       text="No file selected.",
                                       text_color="gray50")
selected_file.pack()

label_size_limit = customtkinter.CTkLabel(master=split_tab, text="Choose fragments' size limit (in bytes)")
label_size_limit.pack(pady=10)
size_limit_entry = customtkinter.CTkEntry(master=split_tab,
                                          width=200,
                                          textvariable=size_limit,
                                          validate="key",
                                          placeholder_text="1GB = 1000MB = 1000000000B")
size_limit_entry.pack()

confirm_split_button = customtkinter.CTkButton(master=split_tab,
                                               text="Confirm",
                                               width=100,
                                               state="disabled",
                                               command=confirm_split_file)
confirm_split_button.pack(pady=20)

split_file_status = customtkinter.CTkLabel(master=split_tab, text="")
split_file_status.pack()


def open_directory():
    global directory_path
    tmp = directory_path
    directory_path = filedialog.askdirectory()
    if not directory_path and tmp:
        directory_path = tmp

    if directory_path and os.listdir(directory_path):
        selected_directory.configure(text=directory_path)
        confirm_merge_button.configure(state="normal")
    else:
        if directory_path and not os.listdir(directory_path):
            selected_directory.configure(text="directory is empty.")
        else:
            selected_directory.configure(text="No directory selected.")

        if confirm_merge_button.cget("state") == "normal":
            confirm_merge_button.configure(state="disabled")


def confirm_merge_directory():
    if directory_path:
        merge_directory_status.configure(text="Ongoing operation...")
        result_path = ravaillac.merge_fragments(directory_path)
        if result_path:
            merge_directory_status.configure(text_color="green")
            merge_directory_status.configure(text=f"Operation succeeded. Result path: {result_path}")
        else:
            merge_directory_status.configure(text_color="red")
            merge_directory_status.configure(text="Operation failed.")


label_directory_path = customtkinter.CTkLabel(master=merge_tab, text="Choose fragments to merge")
label_directory_path.pack(pady=10)
button_directory_path = customtkinter.CTkButton(master=merge_tab,
                                                text="Open",
                                                fg_color="purple3",
                                                hover_color="purple4",
                                                command=open_directory)
button_directory_path.pack()
selected_directory = customtkinter.CTkLabel(master=merge_tab,
                                            text="No directory selected.",
                                            text_color="gray50")
selected_directory.pack()

confirm_merge_button = customtkinter.CTkButton(master=merge_tab,
                                               text="Confirm",
                                               width=100,
                                               state="disabled",
                                               command=confirm_merge_directory)
confirm_merge_button.pack(pady=20)
merge_directory_status = customtkinter.CTkLabel(master=merge_tab, text="")
merge_directory_status.pack()

root.mainloop()
