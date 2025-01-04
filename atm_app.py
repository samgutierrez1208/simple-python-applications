import tkinter as tk
from tkinter import ttk
from datetime import datetime


class ATMApp:
    def __init__(self, root):
        # Main window configuration
        self.root = root
        self.root.title("ATM Application")
        self.root.geometry("400x600")
        self.root.resizable(False, False)

        # Account variables
        self.balance = 0
        self.transaction_history = []

        # Create GUI elements
        self.create_start_screen()

    def create_start_screen(self):
        """Initial screen to set the current balance."""
        self.clear_screen()
        start_frame = tk.Frame(self.root, bg="#F8F9FA")
        start_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(
            start_frame,
            text="Set Current Balance",
            font=("Helvetica", 18, "bold"),
            bg="#007BFF",
            fg="white",
            pady=10,
        ).pack(fill=tk.X)

        tk.Label(
            start_frame,
            text="Enter your initial balance:",
            font=("Helvetica", 14),
            bg="#F8F9FA",
        ).pack(pady=20)

        self.start_balance_entry = ttk.Entry(start_frame, font=("Helvetica", 14))
        self.start_balance_entry.pack(pady=10)

        set_balance_button = ttk.Button(
            start_frame, text="Set Balance", command=self.set_balance
        )
        set_balance_button.pack(pady=10)

        footer_label = tk.Label(
            start_frame,
            text="AZD",
            font=("Helvetica", 10, "italic"),
            bg="#007BFF",
            fg="white",
            pady=5,
        )
        footer_label.pack(side=tk.BOTTOM, fill=tk.X)

    def set_balance(self):
        """Set the initial balance and switch to the transaction screen."""
        try:
            balance = float(self.start_balance_entry.get())
            if balance < 0:
                raise ValueError("Balance cannot be negative.")
            self.balance = balance
            self.create_transaction_screen()
        except ValueError:
            self.start_balance_entry.delete(0, tk.END)
            self.start_balance_entry.insert(0, "Invalid value")

    def create_transaction_screen(self):
        """Main transaction interface."""
        self.clear_screen()
        transaction_frame = tk.Frame(self.root, bg="#F8F9FA")
        transaction_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(
            transaction_frame,
            text="ATM System",
            font=("Helvetica", 18, "bold"),
            bg="#007BFF",
            fg="white",
            pady=10,
        ).pack(fill=tk.X)

        # Balance display
        balance_frame = tk.Frame(transaction_frame, bg="#F8F9FA")
        balance_frame.pack(pady=10)
        tk.Label(
            balance_frame, text="Current Balance:", font=("Helvetica", 14), bg="#F8F9FA"
        ).grid(row=0, column=0, padx=5)
        self.balance_label = tk.Label(
            balance_frame,
            text=f"${self.balance:.2f}",
            font=("Helvetica", 14, "bold"),
            fg="#28A745",
            bg="#F8F9FA",
        )
        self.balance_label.grid(row=0, column=1)

        # Entry and action buttons
        action_frame = tk.Frame(transaction_frame, bg="#F8F9FA")
        action_frame.pack(pady=10, fill=tk.X)

        self.amount_entry = ttk.Entry(action_frame, font=("Helvetica", 12))
        self.amount_entry.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)

        deposit_button = ttk.Button(
            action_frame, text="Deposit", command=self.deposit
        )
        deposit_button.pack(side=tk.LEFT, padx=5)

        withdraw_button = ttk.Button(
            action_frame, text="Withdraw", command=self.withdraw
        )
        withdraw_button.pack(side=tk.LEFT, padx=5)

        # Action status
        status_frame = tk.Frame(transaction_frame, bg="#F8F9FA")
        status_frame.pack(pady=10, fill=tk.X)
        self.status_label = tk.Label(
            status_frame,
            text="Ready for transactions.",
            font=("Helvetica", 12, "italic"),
            fg="#6C757D",
            bg="#F8F9FA",
        )
        self.status_label.pack()

        # History and Exit buttons
        control_frame = tk.Frame(transaction_frame, bg="#F8F9FA")
        control_frame.pack(pady=20, fill=tk.X)

        history_button = ttk.Button(
            control_frame, text="History", command=self.create_history_screen
        )
        history_button.pack(side=tk.LEFT, padx=5, expand=True)

        exit_button = ttk.Button(
            control_frame, text="Exit", command=self.root.quit
        )
        exit_button.pack(side=tk.LEFT, padx=5, expand=True)

        footer_label = tk.Label(
            transaction_frame,
            text="AZD",
            font=("Helvetica", 10, "italic"),
            bg="#007BFF",
            fg="white",
            pady=5,
        )
        footer_label.pack(side=tk.BOTTOM, fill=tk.X)

    def create_history_screen(self):
        """Screen to display transaction history."""
        self.clear_screen()
        history_frame = tk.Frame(self.root, bg="#F8F9FA")
        history_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(
            history_frame,
            text="Transaction History",
            font=("Helvetica", 18, "bold"),
            bg="#007BFF",
            fg="white",
            pady=10,
        ).pack(fill=tk.X)

        history_text = tk.Text(
            history_frame,
            wrap=tk.WORD,
            font=("Helvetica", 12),
            state=tk.DISABLED,
            height=15,
        )
        history_text.pack(fill=tk.BOTH, padx=10, pady=10)

        # Populate the history
        history_text.config(state=tk.NORMAL)
        history_text.delete(1.0, tk.END)
        if self.transaction_history:
            history_text.insert(tk.END, "\n".join(self.transaction_history))
        else:
            history_text.insert(tk.END, "No transactions yet.")
        history_text.config(state=tk.DISABLED)

        # Back button
        back_button = ttk.Button(
            history_frame, text="Back", command=self.create_transaction_screen
        )
        back_button.pack(pady=10)

    def deposit(self):
        """Deposit action."""
        try:
            amount = float(self.amount_entry.get())
            if amount <= 0:
                self.status_label.config(text="Enter a positive amount to deposit.")
            else:
                self.balance += amount
                self.update_balance()
                self.log_transaction("Deposit", amount)
                self.status_label.config(text=f"Deposited ${amount:.2f} successfully.")
        except ValueError:
            self.status_label.config(text="Invalid input. Please enter a numeric value.")

    def withdraw(self):
        """Withdraw action."""
        try:
            amount = float(self.amount_entry.get())
            if amount <= 0:
                self.status_label.config(text="Enter a positive amount to withdraw.")
            elif amount > self.balance:
                self.status_label.config(text="Insufficient funds.")
            else:
                self.balance -= amount
                self.update_balance()
                self.log_transaction("Withdraw", amount)
                self.status_label.config(text=f"Withdrawn ${amount:.2f} successfully.")
        except ValueError:
            self.status_label.config(text="Invalid input. Please enter a numeric value.")

    def update_balance(self):
        """Update the balance display."""
        self.balance_label.config(text=f"${self.balance:.2f}")

    def log_transaction(self, transaction_type, amount):
        """Log the transaction with a timestamp."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.transaction_history.append(f"{timestamp} - {transaction_type}: ${amount:.2f}")

    def clear_screen(self):
        """Clear the root window for a new screen."""
        for widget in self.root.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = ATMApp(root)
    root.mainloop()
