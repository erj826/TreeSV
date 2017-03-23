"""
author: Eric Jacobson
e-mail: erj826@bu.edu

date: 1 March 2017

GUI for TreeSV Application
"""

import tkinter as tk
import time


def gen_csv():
    user_entry = directory_field.get()
    var1 = tk.StringVar()
    lbl2 = tk.Label(top, anchor='center', textvariable=var1,
               font=('Helvetica', 12), bg=def_bg,
               padx='1', pady='1'
               )
    var1.set('Generating your CSV for ' + user_entry + '...')
    lbl2.pack()

#Creating Popup Window
top = tk.Tk()

#Background Color and Default Size
def_bg = '#ffb3b3'
top['bg'] = def_bg
top.resizable(width=False, height=False)
top.geometry('{}x{}'.format(600, 300))
top.title('TreeSV')

#Top Label
var = tk.StringVar()
lbl = tk.Label(top, anchor='center', textvariable=var,
               font=('Helvetica', 24), bg=def_bg,
               padx='2', pady='50'
               )
var.set('Please enter a directory name:')
lbl.pack()

#Text Field
directory_field = tk.Entry(top, bd='0', width='40',
                           font=('Helvetica', 14)
                           )
directory_field.pack()

#Author Label
author = tk.Label(top, text='A Project by Eric Jacobson',
                  bg=def_bg, anchor='n',font=('Helvetica', 11))
author.place(rely=1.0, relx=1.0, x=0, y=0, anchor='se')

#Submit Button
sub = tk.Button(top, text="Submit", command =gen_csv, bg = def_bg)
sub.pack()





#Run Window
top.mainloop()

