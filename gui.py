from tkinter import filedialog
import customtkinter


def open_file():
    file_path = filedialog.askopenfilename()
    print(file_path)


customtkinter.set_appearance_mode("dark")

root = customtkinter.CTk()

root.geometry("500x600")
root.title("Ravaillac")

tabview = customtkinter.CTkTabview(root, width=450, height=580)
tabview.pack()
split_tab = tabview.add("Split a file")
merge_tab = tabview.add("Merge fragments")

label = customtkinter.CTkLabel(master=split_tab, text="Choose a file to split")
label.pack()
button = customtkinter.CTkButton(master=split_tab, text="Open", command=open_file)
button.pack()

root.mainloop()
