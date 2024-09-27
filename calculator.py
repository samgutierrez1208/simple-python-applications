import tkinter as tk
import math

class ScientificCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Scientific Calculator")
        self.root.geometry("350x500")
        self.root.configure(background="lightgray")

        self.expression = ""
        self.entry_text = tk.StringVar()
        self.entry = tk.Entry(root, textvariable=self.entry_text, font=('Arial', 16), bd=10, insertwidth=2, width=18, borderwidth=4, relief=tk.RIDGE)
        self.entry.grid(row=0, column=0, columnspan=5, ipady=8, pady=10)

        numbers = ['7', '8', '9', '4', '5', '6', '1', '2', '3', '0', '.']
        operators = ['/', '*', '-', '+', '=']
        functions = ['sqrt', 'pow', 'log', 'sin', 'cos', 'tan', 'cot', 'pi', 'exp']
        clear_button = ['C']

        number_bg = "#d4d4d4"
        operator_bg = "#c4c4c4"
        function_bg = "#b0b0b0"
        clear_bg = "#ffb3b3"
        
        button_order = [
            ['7', '8', '9', '/', 'C'],
            ['4', '5', '6', '*', 'sqrt'],
            ['1', '2', '3', '-', 'pow'],
            ['0', '.', '=', '+', 'log'],
            ['sin', 'cos', 'tan', 'cot', 'pi'],
            ['exp']
        ]

        row_val = 1
        col_val = 0
        for row in button_order:
            for button in row:
                if button in numbers:
                    button_color = number_bg
                elif button in operators:
                    button_color = operator_bg
                elif button in functions:
                    button_color = function_bg
                else:
                    button_color = clear_bg
                
                tk.Button(root, text=button, padx=10, pady=10, font=('Arial', 15), 
                          bg=button_color, fg="black", bd=3, relief=tk.RAISED,
                          command=lambda b=button: self.on_button_click(b)).grid(row=row_val, column=col_val, ipadx=2, ipady=2, sticky="nsew")
                col_val += 1
            col_val = 0
            row_val += 1

        for i in range(5):
            self.root.grid_columnconfigure(i, weight=1)
        for i in range(6):
            self.root.grid_rowconfigure(i, weight=1)

        self.azd_label = tk.Label(root, text="AZD", font=('Arial', 12, 'bold'), bg="lightgray", fg="black")
        self.azd_label.grid(row=6, column=1, columnspan=5, pady=10)

    def on_button_click(self, button):
        if button == "C":
            self.expression = ""
        elif button == "=":
            try:
                self.expression = self.expression.replace('sqrt', 'math.sqrt') \
                                                  .replace('pow', 'math.pow') \
                                                  .replace('log', 'math.log') \
                                                  .replace('sin', 'math.sin') \
                                                  .replace('cos', 'math.cos') \
                                                  .replace('tan', 'math.tan') \
                                                  .replace('cot', '1/math.tan') \
                                                  .replace('pi', 'math.pi') \
                                                  .replace('exp', 'math.exp')
                result = str(eval(self.expression, {"__builtins__": None}, {"math": math}))
                self.expression = result
            except Exception as e:
                self.expression = "Error"
        else:
            self.expression += button
        
        self.entry_text.set(self.expression)

if __name__ == "__main__":
    root = tk.Tk()
    calc_app = ScientificCalculator(root)
    root.mainloop()
    