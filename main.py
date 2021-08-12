import tkinter
from tkinter import *
from PIL import Image, ImageTk
import os
import time
import csv


root = Tk()
images = []
i = 0

for filename in os.listdir("images"):
   images.append(filename)

img = ImageTk.PhotoImage(Image.open("images\\" + images[0]))
panel = tkinter.Label(root, image=img)
panel.pack(side="bottom", fill="both", expand="yes")


if (os.path.isfile('picture.csv')):
    with open('picture.csv', newline='') as csvfile:
        read = csv.DictReader(csvfile)
        for row in read:
            if row['pic_name'] in images:
                images.remove(row['pic_name'])

root.title(str(i + 1) + "/" + str(len(images)) + " Images")

def callbackGood(e):
    global i
    picture_writer.writerow({'pic_name': str(images[i]), 'result': 1})
    i = i + 1
    img2 = ImageTk.PhotoImage(Image.open("images\\" + images[i]))
    panel.configure(image=img2)
    panel.image = img2
    root.title(str(i + 1) + "/" + str(len(images)) + " Images")

def callbackDelete(e):
    global i
    os.rename("images\\" + images[i], "images\\removed\\" + images[i])
    i = i + 1
    img2 = ImageTk.PhotoImage(Image.open("images\\" + images[i]))
    panel.configure(image=img2)
    panel.image = img2
    root.title(str(i + 1) + "/" + str(len(images)) + " Images")


def callbackBad(e):
    global i
    picture_writer.writerow({'pic_name': str(images[i]), 'result': 0})
    i = i + 1
    img2 = ImageTk.PhotoImage(Image.open("images\\" + images[i]))
    panel.configure(image=img2)
    panel.image = img2
    root.title(str(i + 1) + "/" + str(len(images)) + " Images")

      
with open('picture.csv', mode='w', newline='') as picture:
    fieldnames = ['pic_name', 'result']
    picture_writer = csv.DictWriter(picture, fieldnames=fieldnames)

    root.bind("<Up>", callbackDelete)
    root.bind("<Left>", callbackGood)
    root.bind("<Right>", callbackBad)
    root.mainloop()

