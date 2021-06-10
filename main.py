import tkinter
from tkinter import *
from PIL import Image, ImageTk


root = Tk()

img = Image.open("images\city.png")

imgD = ImageTk.PhotoImage(img)

label = tkinter.Label(image=imgD)
label.image = imgD
label.place(x=0,y=0)


width, height = img.size
size = str(width) + "x" + str(height + 50)

button1 = Button(text="Good")
button1.place(x=0, y=height+25)

button1 = Button(text="Bad")
button1.place(x=75, y=height+25)

root.geometry(size)
root.mainloop()

