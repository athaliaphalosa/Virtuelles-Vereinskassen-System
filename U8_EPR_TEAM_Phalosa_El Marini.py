
__author__ = "8515942, Phalosa, 8499763, El Marini"

import tkinter as tk
from tkinter import messagebox
from tkinter import font
import csv

class Administration:
    def __init__(self, admin, account, main_window):
        self.admin = admin
        self.account = account
        self.main_window = main_window
        self.admin_frame = tk.Frame(admin)
        self.admin_frame.pack(padx=10, pady=10, fill="x", expand=True)

    def admin_option(self):
        self.option_frame = tk.Toplevel(self.admin_frame)
        self.option_frame.title = "Administrator"

        option = font.Font(family="helvetica", size=25, weight=font.BOLD)
        option = tk.Label(self.option_frame, text="Hello Admin, now you can choose what you want to do here 😊", font=option)
        option.pack(padx=20, pady=20, fill="both", expand=True)

        back = tk.Button(self.option_frame, text="Back to Main Menu Log In", font=("times new roman", 20, "normal"), command=self.back_to_main)
        back.pack(padx=10, pady=10, side="bottom", fill="x")

        club = font.Font(family="times new roman", size=20, weight=font.NORMAL)
        club_create = tk.Button(self.option_frame, text="Create Club", font=club, width=20, height=10, bg="blue", command=self.create_club)
        club_create.pack(side="left", padx=20, pady=10, fill="x", expand=True)

        file = font.Font(family="times new roman", size=20, weight=font.NORMAL)
        look_file = tk.Button(self.option_frame, text="See current status club in csv file", font=file, width=20, height=10, bg="blue", command=self.view_clubs)
        look_file.pack(side="left", padx=20, pady=10, fill="x", expand=True)

    def create_club(self):
        create_window = tk.Toplevel(self.option_frame)
        create_window.title = "Create Club"

        club_label = tk.Label(create_window, text="Write down the name club!", font=("times new roman", 25, "normal"))
        club_label.pack(padx=20, pady=10)
        club_entry = tk.Entry(create_window, bg="lightblue", font=("helvetice", 20))
        club_entry.pack(padx=20, pady=10)

        def submit():
            club_name = club_entry.get().strip()
            if club_name:
                if club_name not in self.account:
                    self.account[club_name] = {}
                    self.save_csv(club_name)
                    messagebox.showinfo("Success", f"Club {club_name} created successfully!")
                    create_window.destroy()
                else:
                    messagebox.showerror("Error", "Club already exists!")
            else:
                messagebox.showerror("Error", "Club cannot be empty!")

        club_but = tk.Button(create_window, text="Create", font=("times new roman", 20, "normal"), command=submit)
        club_but.pack(padx=10, pady=10, side="left")

        back = tk.Button(create_window, text="Back to Main Menu", font=("times new roman", 20, "normal"), command=self.back_to_main)
        back.pack(padx=10, pady=10, side="right")

    def save_csv(self, club_name):
        try:
            file_name = "club.csv"  # Use a single file for storing all clubs
            with open(file_name, mode="a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([club_name])  # Save the club name
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save club: {e}")

    def view_clubs(self):
        try:
            # Read the CSV file containing the club names
            with open("club.csv", mode="r") as file:
                reader = csv.reader(file)
                clubs = [row[0] for row in reader if row]  # Extract club names from each row

            if clubs:
                messagebox.showinfo("Clubs", "\n".join(clubs))  # Show the list of clubs
            else:
                messagebox.showinfo("No Clubs", "No clubs found. Please create a club!")

        except FileNotFoundError:
            messagebox.showerror("Error", "No clubs found. Please create a club!")

    def back_to_main(self):
        self.option_frame.destroy()
        self.main_window.show_main_menu()


class Cashier:
    def __init__(self, cashier, club_name, main_window):
        self.cashier = cashier
        self.club_name = club_name
        self.file_name = f"{club_name}.csv"
        self.main_window = main_window

    def cashier_option(self):
        cashier_window = tk.Toplevel(self.cashier)
        cashier_window.title = f"Cashier - {self.club_name}"

        tk.Label(cashier_window, text=f"Manage Club: {self.club_name}", font=("helvetica", 30, "bold", "italic")).pack(pady=10)

        transaction_but = tk.Button(cashier_window, text="New Transaction", font=("times new roman", 20, "bold"), command=lambda: self.transaction_window(cashier_window))
        transaction_but.pack(pady=10)

        history_but = tk.Button(cashier_window, text="View Transaction History", font=("times new roman", 20, "bold"), command=lambda: self.show_transaction_history(cashier_window))
        history_but.pack(pady=10)

        back = tk.Button(cashier_window, text="Back to Main Menu", font=("times new roman", 20, "normal"), command=lambda: self.back_to_main(cashier_window))
        back.pack(pady=10)

    def transaction_window(self, trans):
        trans.withdraw()
        transaction_window = tk.Toplevel(trans)
        transaction_window.title = f"New Transaction - {self.club_name}"

        tk.Label(transaction_window, text="Transaction Type", font=("helvetica", 30, "bold", "italic")).pack(pady=10)
        transaction_type = tk.StringVar(value="Einzahlung")
        tk.Radiobutton(transaction_window, text="Deposit", variable=transaction_type, value="Deposit").pack()
        tk.Radiobutton(transaction_window, text="Pay Out", variable=transaction_type, value="Pay Out").pack()

        tk.Label(transaction_window, text="Amount (€)", font=("helvetica", 15)).pack(pady=5)
        amount_entry = tk.Entry(transaction_window)
        amount_entry.pack(pady=5)

        tk.Label(transaction_window, text="Description", font=("helvetica", 15, "bold")).pack(pady=10)
        description_entry = tk.Entry(transaction_window)
        description_entry.pack(pady=5)

        def submit_transaction():
            transaction_type_val = transaction_type.get()
            amount_val = amount_entry.get().strip()
            description_val = description_entry.get().strip()
            if amount_val.isdigit() and description_val:
                with open(self.file_name, "a", newline="") as file:
                    writer = csv.writer(file)
                    writer.writerow([transaction_type_val, amount_val, description_val])
                messagebox.showinfo("Success", "Transaction added successfully!")
                transaction_window.destroy()
                trans.deiconify()
            else:
                messagebox.showerror("Error", "Please provide valid input!")

        tk.Button(transaction_window, text="Submit", command=submit_transaction).pack(pady=10)
        tk.Button(transaction_window, text="Cancel", command=lambda: (transaction_window.destroy(), trans.deiconify())).pack(pady=10)

    def show_transaction_history(self, parent):
        try:
            with open(self.file_name, "r") as file:
                reader = csv.reader(file)
                transactions = list(reader)
            if transactions:
                history_window = tk.Toplevel(parent)
                history_window.title(f"Transaction History - {self.club_name}")
                for transaction in transactions:
                    tk.Label(history_window, text=" | ".join(transaction), font=("helvetica", 12)).pack()
            else:
                messagebox.showinfo("No History", "No transactions available for this club.")
        except FileNotFoundError:
            messagebox.showerror("Error", "No transaction file found for this club.")

    def back_to_main(self, cashier_window):
        cashier_window.destroy()
        self.main_window.show_main_menu()


class FinanceOfficer:
    def __init__(self, officer, club_name, main_window):
        self.officer = officer
        self.club_name = club_name
        self.file_name = f"{club_name}.csv"
        self.main_window = main_window

    def officer_option(self):
        officer_window = tk.Toplevel(self.officer)
        officer_window.title = f"Finance Officer - {self.club_name}"

        tk.Label(officer_window, text=f"Manage Club: {self.club_name}", font=("helvetica", 30, "bold", "italic")).pack(pady=10)

        history_but = tk.Button(officer_window, text="View Transaction History", font=("times new roman", 20, "bold"), command=lambda: self.show_transaction_history(officer_window))
        history_but.pack(pady=10)

        back = tk.Button(officer_window, text="Back to Main Menu", font=("times new roman", 20, "normal"), command=lambda: self.back_to_main(officer_window))
        back.pack(pady=10)

    def show_transaction_history(self, parent):
        try:
            with open(self.file_name, "r") as file:
                reader = csv.reader(file)
                transactions = list(reader)
            if transactions:
                history_window = tk.Toplevel(parent)
                history_window.title(f"Transaction History - {self.club_name}")
                for transaction in transactions:
                    tk.Label(history_window, text=" | ".join(transaction), font=("helvetica", 12)).pack()
            else:
                messagebox.showinfo("No History", "No transactions available for this club.")
        except FileNotFoundError:
            messagebox.showerror("Error", "No transaction file found for this club.")

    def back_to_main(self, officer_window):
        officer_window.destroy()
        self.main_window.show_main_menu()


class Apps(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("800x400")
        self.resizable(False, False)
        self.title("Vereinskassen System")
        self.configure(bg="white")
        self.account = {}
        self.show_main_menu()

    def show_main_menu(self):
        title = font.Font(self, family="times new roman", size=30, slant=font.ITALIC)
        self.hello = tk.Label(self, text="Welcome to the Cash Club \nAre you Adminstrator / Cashier / Finance Officer? \nChoose one Role, then you need to log in first!", font=title, fg="red")
        self.hello.pack(padx=10, pady=10, fill="both", expand=True)

        self.input_frame = tk.Frame(self)
        self.input_frame.pack(padx=10, pady=10, fill="x", expand=True)

        admin = font.Font(family="times new roman", size=15, weight=font.BOLD)
        admin_but = tk.Button(self.input_frame, text="Administrator", font=admin, width=20, height=10, command=lambda: self.entry("Administrator"))
        admin_but.pack(side="left", padx=20, pady=1, fill="x", expand=True)

        cashier = font.Font(family="times new roman", size=15, weight=font.BOLD)
        cashier_but = tk.Button(self.input_frame, text="Cashier", font=cashier, width=20, height=10, command=lambda: self.entry("Cashier"))
        cashier_but.pack(side="left", padx=20, pady=1, fill="x", expand=True)

        officer = font.Font(family="times new roman", size=15, weight=font.BOLD)
        officer_but = tk.Button(self.input_frame, text="Finance Officer", font=officer, width=20, height=10, command=lambda: self.entry("Finance Officer"))
        officer_but.pack(side="left", padx=20, pady=1, fill="x", expand=True)

    def entry(self, role):
        login_window = tk.Toplevel(self)
        login_window.title = f"{role} Log In"
        tk.Label(login_window, text=f"Please enter your {role} password:", font=("times new roman", 25)).pack(padx=10, pady=10)
        entry = tk.Entry(login_window, show="*")
        entry.pack(padx=10, pady=10)

        def login():
            password = entry.get()
            if role == "Administrator" and password == "admin123":
                admin = Administration(self, self.account, self)
                admin.admin_option()
                login_window.destroy()
            elif role == "Cashier" and password == "cashier123":
                cashier = Cashier(self, "Club A", self)
                cashier.cashier_option()
                login_window.destroy()
            elif role == "Finance Officer" and password == "officer123":
                officer = FinanceOfficer(self, "Club A", self)
                officer.officer_option()
                login_window.destroy()
            else:
                messagebox.showerror("Error", "Invalid password!")

        tk.Button(login_window, text="Log In", command=login).pack(pady=10)
        tk.Button(login_window, text="Back", command=login_window.destroy).pack(pady=10)


if __name__ == "__main__":
    app = Apps()
    app.mainloop()
