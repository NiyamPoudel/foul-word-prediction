from tkinter import Tk
from tkinter.messagebox import Message 
from _tkinter import TclError

root = Tk() 
root.withdraw()
try:
    root.after(20000, root.destroy) 
    Message(title="Foul Word Detected", message="The following foul words have been detected: Dick.", master=root).show()
except TclError:
    pass
