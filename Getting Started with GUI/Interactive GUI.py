from tkinter import *


class InteractiveGUI:
    LABEL_TEXT = [
        "This is our first GUI!",
        "Actually, this is our second GUI.",
        "We made it more interesting...",
        "...by making this label interactive.",
        "Go on, click on it again."
    ]

    def __init__(self, master):
        self.master = master
        master.title("An Interactive GUI")

        self.label_index = 0
        self.label_text = StringVar()
        self.label_text.set(self.LABEL_TEXT[self.label_index])
        self.label = Label(master, textvariable=self.label_text)
        self.label.bind("<Button-1>", self.cycle_label_text)
        self.label.grid(columnspan=3, sticky=W + E)

        self.greet_button = Button(master, text="GREET!", command=self.greet)
        self.greet_button.grid(row=1)

        self.close_button = Button(master, text="CLOSE", command=master.quit)
        self.close_button.grid(row=1, column=1)

    def greet(self):
        self.label = Label(self.master, text="GREETINGS!!!")
        self.label.grid(columnspan=6, sticky=W + E)

    def cycle_label_text(self, event):
        self.label_index += 1
        self.label_index %= len(self.LABEL_TEXT)
        self.label_text.set(self.LABEL_TEXT[self.label_index])


root = Tk()
my_gui = InteractiveGUI(root)
root.mainloop()