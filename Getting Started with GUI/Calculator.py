from tkinter import *

class Calculator:

    def __init__(self, master):
        self.master = master
        master.title("Calculator")
        master.geometry("325x175")

        self.total = 0
        self.entered_number = 0

        self.total_label_text = IntVar()
        self.total_label_text.set(self.total)
        self.total_label = Label(master, textvariable=self.total_label_text)

        self.label = Label(master, text="Total : ")

        vcmd = master.register(self.validate)
        self.entry = Entry(master, validate="key", validatecommand=(vcmd, '%P'))
        self.entry.place(height=100)

        self.add_button = Button(master, text="+", command=lambda: self.update("add"), height=2, width=7)
        self.subtract_button = Button(master, text="-", command=lambda: self.update("subtract"), height=2, width=7)
        self.multiply_button = Button(master, text="*", command=lambda: self.update("multiply"), height=2, width=7)
        self.divide_button = Button(master, text="/", command=lambda: self.update("divide"), height=2, width=7)
        self.modulo_button = Button(master, text="%", command=lambda: self.update("modulo"), height=2, width=7)
        self.reset_button = Button(master, text="Reset", command=lambda: self.update("reset"), height=2, width=7)

        # Layout

        self.label.grid(row=0, column=0, sticky=W)
        self.total_label.grid(row=0, column=1, columnspan=2, sticky=E)

        self.entry.grid(row=1, column=0, columnspan=4, sticky=W+E, ipadx=100, ipady=5)

        self.add_button.grid(row=2, column=0)
        self.subtract_button.grid(row=2, column=1)
        self.multiply_button.grid(row=3, column=0)
        self.divide_button.grid(row=3, column=1)
        self.modulo_button.grid(row=4, column=0)
        self.reset_button.grid(row=5, column=1, sticky=W+E)

    def validate(self, new_text):
        if not new_text:
            self.entered_number = 0
            return True

        try:
            self.entered_number = int(new_text)
            return True
        except ValueError:
            return False

    def update(self, method):
        if method == "add":
            self.total += self.entered_number
        elif method == "subtract":
            self.total -= self.entered_number
        elif method == "multiply":
            self.total *= self.entered_number
        elif method == "divide":
            self.total /= self.entered_number
        elif method == "modulo":
            self.total %= self.entered_number
        else:
            self.total = 0

        self.total_label_text.set(self.total)
        self.entry.delete(0,END)


root = Tk()
my_gui = Calculator(root)
root.mainloop()