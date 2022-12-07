import tkinter as tk
from tkinter import filedialog

def openFile():
    file_path = filedialog.askopenfilename()
    print(file_path)


root = tk.Tk()

root.geometry("500x600")
root.title("Ravaillac")

label = tk.Label(root, text="Choose a file to split")
label.pack()
button = tk.Button(text="Open", command=openFile)
button.pack()

root.mainloop()