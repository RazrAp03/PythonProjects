import tkinter as tk
from tkinter import ttk

# Define the Calculator class
class Calculator:
    def __init__(self):
        self.expression = ""
        self.root = tk.Tk()
        self.root.title("Calculator")
        self.root.geometry("300x400")
        
        # Create display
        self.display = ttk.Entry(self.root, font=('Arial', 18))
        self.display.grid(row=0, column=0, columnspan=4, sticky='nsew')
        
        # Create buttons
        buttons = [
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            '0', '.', '=', '+'
        ]
        
        row_val = 1
        col_val = 0
        for button in buttons:
            ttk.Button(self.root, text=button, command=lambda b=button: self.on_button_click(b)).grid(row=row_val, column=col_val, sticky='nsew')
            col_val += 1
            if col_val > 3:
                col_val = 0
                row_val += 1
        
        ttk.Button(self.root, text='C', command=self.clear).grid(row=row_val, column=0, columnspan=4, sticky='nsew')
        
        # Configure grid weights
        for i in range(5):
            self.root.rowconfigure(i, weight=1)
            self.root.columnconfigure(i, weight=1)
        
        self.root.mainloop()

    def on_button_click(self, char):
        if char == '=':
            self.expression = str(eval(self.expression))
        else:
            self.expression += str(char)
        
        self.update_display()
    
    def clear(self):
        self.expression = ""
        self.update_display()
    
    def update_display(self):
        self.display.delete(0, tk.END)
        self.display.insert(0, self.expression)

# Create an instance of the Calculator class and start the application
calculator = Calculator()
