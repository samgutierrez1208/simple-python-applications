import tkinter as tk


class SimpleCalculator:
    """A basic calculator with digits and four operations."""

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Simple Calculator")

        self.expression = ""
        self.text = tk.StringVar()
        entry = tk.Entry(
            root,
            textvariable=self.text,
            font=("Arial", 16),
            bd=10,
            insertwidth=2,
            width=14,
            borderwidth=4,
            relief=tk.RIDGE,
            justify="right",
        )
        entry.grid(row=0, column=0, columnspan=4, ipady=8, pady=10)

        buttons = [
            "7",
            "8",
            "9",
            "/",
            "4",
            "5",
            "6",
            "*",
            "1",
            "2",
            "3",
            "-",
            "0",
            "C",
            "=",
            "+",
        ]

        row = 1
        col = 0
        for char in buttons:
            tk.Button(
                root,
                text=char,
                padx=16,
                pady=16,
                font=("Arial", 14),
                command=lambda c=char: self.on_button_click(c),
            ).grid(row=row, column=col, sticky="nsew")
            col += 1
            if col > 3:
                col = 0
                row += 1

        for i in range(4):
            root.grid_columnconfigure(i, weight=1)
        for i in range(1, 5):
            root.grid_rowconfigure(i, weight=1)

    def on_button_click(self, char: str) -> None:
        if char == "C":
            self.expression = ""
        elif char == "=":
            try:
                self.expression = str(eval(self.expression))
            except Exception:
                self.expression = "Error"
        else:
            self.expression += char
        self.text.set(self.expression)


def main() -> None:
    root = tk.Tk()
    SimpleCalculator(root)
    root.mainloop()


if __name__ == "__main__":
    main()
