import tkinter as tk
from tkinter import messagebox
import string
import random
from datetime import datetime

class PasswordGenerator:
    def __init__(self, length=16, num=3, punctuation=True, digits=True, letters=True, excludes=None):
        self.length = length
        self.num = num
        self.punctuation = punctuation
        self.digits = digits
        self.letters = letters
        self.excludes = excludes

        if not self.letters and not self.digits and not self.punctuation:
            messagebox.showerror("Error", "At least one item must be true")
            return

    def pwgen(self):
        random_source = ""
        password = ""

        if self.letters:
            random_source += string.ascii_letters
            password += random.choice(string.ascii_lowercase) + random.choice(string.ascii_uppercase)

        if self.digits:
            random_source += string.digits
            password += random.choice(string.digits)

        if self.punctuation:
            punctuation = [x for x in string.punctuation]

            if self.excludes is not None:
                for i in self.excludes:
                    punctuation.remove(i)

            random_source += ''.join(map(str, punctuation))
            password += random.choice(''.join(map(str, punctuation)))

        for i in range(self.length - len(password)):
            password += random.choice(random_source)

        password_list = list(password)
        random.SystemRandom().shuffle(password_list)
        password = ''.join(password_list)

        return password

    def create(self):
        current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"passwords_{current_datetime}.txt"
        with open(filename, "w") as f:
            for i in range(self.num):
                password = self.pwgen()
                f.write(password + "\n")
        messagebox.showinfo("Success", f"Passwords saved to {filename}")

def check_password_strength(password: str) -> int:
    score = 0
    # Check if the password contains at least one character from each required character class
    if any(c.isupper() for c in password):
        score += 1
    if any(c.islower() for c in password):
        score += 1
    if any(c.isdigit() for c in password):
        score += 1
    if any(c in string.punctuation for c in password):
        score += 1
    
    # Check if the password is long enough
    if len(password) >= 8:
        score += 1
    if len(password) >= 12:
        score += 1
    if len(password) >= 16:
        score += 1
    if len(password) >= 20:
        score += 1
  
    return score

def check_password(password: str, common_passwords: set) -> str:
    # Check if the password is too common
    if password in common_passwords:
        return "Password is too common. Your password strength is 0."

    # Check the password strength
    score = check_password_strength(password)
    if score == 0:
        return "Password is too weak."
    elif score <= 2:
        return "Password is not strong enough."
    else:
        return "Password is strong."

def get_common_passwords(file_path: str) -> set:
    """Reads the list of common passwords from a file and returns a set."""
    try:
        with open(file_path, "r") as f:
            return set(f.read().splitlines())
    except FileNotFoundError:
        messagebox.showwarning("Warning", f"Common password file not found at {file_path}.")
        return set()

class PasswordToolsGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Tools")
        self.root.geometry("800x200")
        self.numbers_checked = tk.BooleanVar()
        self.special_chars_checked = tk.BooleanVar()
        self.letters_checked = tk.BooleanVar()

        # Color Scheme
        self.bg_color = "white"
        self.font_color = "#000000"
        self.entry_bg_color = "#ffffff"

        self.root.config(bg=self.bg_color)

        # Password Generator Frame
        self.generator_frame = tk.LabelFrame(root, text="Password Generator", bg=self.bg_color, fg=self.font_color)
        self.generator_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.setup_password_generator_ui()

        # Password Strength Checker Frame
        self.strength_frame = tk.LabelFrame(root, text="Password Strength Checker", bg=self.bg_color, fg=self.font_color)
        self.strength_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        self.setup_password_strength_ui()

    def setup_password_generator_ui(self):
        tk.Label(self.generator_frame, text="Password Length:", bg=self.bg_color, fg=self.font_color).grid(row=0, column=0, padx=5, pady=5)
        self.length_entry = tk.Entry(self.generator_frame, bg=self.entry_bg_color, fg=self.font_color)
        self.length_entry.grid(row=0, column=1, padx=5, pady=5)
        self.length_entry.insert(0, "16")

        tk.Label(self.generator_frame, text="Number of Passwords:", bg=self.bg_color, fg=self.font_color).grid(row=1, column=0, padx=5, pady=5)
        self.num_entry = tk.Entry(self.generator_frame, bg=self.entry_bg_color, fg=self.font_color)
        self.num_entry.grid(row=1, column=1, padx=5, pady=5)
        self.num_entry.insert(0, "3")

        self.generate_button = tk.Button(self.generator_frame, text="Generate Passwords", command=self.generate_passwords)
        self.generate_button.grid(row=2, column=0, columnspan=2, pady=10)

    def setup_password_strength_ui(self):
        tk.Label(self.strength_frame, text="Enter Password:", bg=self.bg_color, fg=self.font_color).grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.password_entry = tk.Entry(self.strength_frame, show="*", bg=self.entry_bg_color, fg=self.font_color)
        self.password_entry.grid(row=0, column=1, padx=5, pady=5, sticky='we')

        self.check_strength_button = tk.Button(self.strength_frame, text="Check Strength", command=self.check_strength)
        self.check_strength_button.grid(row=1, column=1, pady=10, padx=(0, 5), sticky='e')

        self.show_password_button = tk.Button(self.strength_frame, text="👁", command=self.show_password)
        self.show_password_button.grid(row=0, column=2, pady=10, padx=(0, 5), sticky='w')

        self.clear_button = tk.Button(self.strength_frame, text="Clear", command=self.clear_password)
        self.clear_button.grid(row=1, column=2, pady=10, sticky='w')

    def generate_passwords(self):
        try:
            length = int(self.length_entry.get())
            num = int(self.num_entry.get())
            password_generator = PasswordGenerator(length=length, num=num)
            password_generator.create()
        except ValueError:
            messagebox.showerror("Error", "Invalid input for length or number of passwords.")

    def check_strength(self):
        password = self.password_entry.get()
        common_passwords = get_common_passwords("common.txt")
        result = check_password(password, common_passwords)
        messagebox.showinfo("Password Strength", result)

    def show_password(self):
        self.password_entry.config(show="")

    def clear_password(self):
        self.password_entry.delete(0, tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordToolsGUI(root)
    app.root.option_add('*Font', 'Times 12')
    root.mainloop()
