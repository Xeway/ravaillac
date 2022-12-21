import os
from tkinter import filedialog, StringVar
import customtkinter
import ravaillac


def open_file():
    global file_path
    file_path = filedialog.askopenfilename()
    selected_file.configure(text=file_path)
    if file_path and size_limit.get().isdecimal():
        confirm_split_button.configure(state="normal")
    elif confirm_split_button.cget("state") == "normal":
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


customtkinter.set_appearance_mode("dark")

root = customtkinter.CTk()

root.geometry("500x600")
root.title("Ravaillac")

size_limit = StringVar()
size_limit.trace_add("write", size_limit_modified)
file_path = None
folder_path = None

tabview = customtkinter.CTkTabview(root, width=450, height=580)
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


def open_folder():
    global folder_path
    folder_path = filedialog.askdirectory()

    if folder_path and os.listdir(folder_path):
        selected_folder.configure(text=folder_path)
        confirm_merge_button.configure(state="normal")
    else:
        if folder_path and not os.listdir(folder_path):
            selected_folder.configure(text="Folder is empty.")
        else:
            selected_folder.configure(text="No folder selected.")

        if confirm_merge_button.cget("state") == "normal":
            confirm_merge_button.configure(state="disabled")


def confirm_merge_folder():
    if folder_path:
        merge_folder_status.configure(text="Ongoing operation...")
        result_path = ravaillac.merge_fragments(folder_path)
        if result_path:
            merge_folder_status.configure(text_color="green")
            merge_folder_status.configure(text=f"Operation succeeded. Result path: {result_path}")
        else:
            merge_folder_status.configure(text_color="red")
            merge_folder_status.configure(text="Operation failed.")


label_folder_path = customtkinter.CTkLabel(master=merge_tab, text="Choose fragments to merge")
label_folder_path.pack(pady=10)
button_folder_path = customtkinter.CTkButton(master=merge_tab,
                                             text="Open",
                                             fg_color="purple3",
                                             hover_color="purple4",
                                             command=open_folder)
button_folder_path.pack()
selected_folder = customtkinter.CTkLabel(master=merge_tab,
                                         text="No folder selected.",
                                         text_color="gray50")
selected_folder.pack()

confirm_merge_button = customtkinter.CTkButton(master=merge_tab,
                                               text="Confirm",
                                               width=100,
                                               state="disabled",
                                               command=confirm_merge_folder)
confirm_merge_button.pack(pady=20)
merge_folder_status = customtkinter.CTkLabel(master=merge_tab, text="")
merge_folder_status.pack()

root.mainloop()
