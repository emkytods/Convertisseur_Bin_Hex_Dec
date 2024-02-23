import tkinter as tk
from tkinter import messagebox

class Validator:
    @staticmethod
    def is_decimal(input_str):
        return all(char.isdigit() for char in input_str)

    @staticmethod
    def is_binary(input_str):
        return all(bit in '01' for bit in input_str)

    @staticmethod
    def is_hexadecimal(input_str):
        return all(char in '0123456789ABCDEFabcdef' for char in input_str)

class Converter:
    @staticmethod
    def decimal_to_binary(decimal):
        return bin(decimal)

    @staticmethod
    def decimal_to_hexadecimal(decimal):
        return hex(decimal)

    @staticmethod
    def binary_to_decimal(binary):
        return int(binary, 2)

    @staticmethod
    def binary_to_hexadecimal(binary):
        decimal = Converter.binary_to_decimal(binary)
        return hex(decimal)

    @staticmethod
    def hexadecimal_to_binary(hexadecimal):
        decimal = int(hexadecimal, 16)
        return bin(decimal)

    @staticmethod
    def hexadecimal_to_decimal(hexadecimal):
        return int(hexadecimal, 16)

def clear_entry():
    entry.delete(0, tk.END)

def center_window(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry('{}x{}+{}+{}'.format(width, height, x, y))

calculator_window_reference = None

def show_calculator():
    global calculator_window_reference

    if calculator_window_reference is not None:
        calculator_window_reference.destroy()

    calculator_window = tk.Toplevel(root)
    calculator_window.title("Clavier visuel")

    calculator_window_reference = calculator_window

    root_width = root.winfo_width()
    root_height = root.winfo_height()

    root_x = root.winfo_x()
    root_y = root.winfo_y()
    calculator_x = root_x - calculator_window.winfo_reqwidth() + 50
    calculator_y = root_y + (root_height - calculator_window.winfo_reqheight()) // 2 + 30

    calculator_window.geometry(f"+{calculator_x}+{calculator_y}")

    calculator_window.bind("<F11>", lambda event: "break")
    calculator_window.attributes('-toolwindow', True)
    calculator_window.resizable(False, False)
    calculator_window.attributes("-topmost", True)

    for i in range(16):
        value = i if i < 10 else chr(ord('A') + i - 10)
        button = tk.Button(calculator_window, text=str(value), command=lambda val=value: insert_character(val), padx=6)
        button.grid(row=i // 4, column=i % 4, padx=4, pady=4)

def insert_character(char):
    entry.insert(tk.END, str(char))

def convert():
    index = options.curselection()
    if index:
        choice = options.get(index)
        value = entry.get()

        if value == "":
            messagebox.showerror(" ", "Veuillez entrer une valeur à convertir.")
            return

        if choice == "1. Convertir décimal en binaire":
            try:
                decimal = int(value)
                result.set(Converter.decimal_to_binary(decimal))
            except ValueError:
                messagebox.showerror(" ", "Veuillez entrer un nombre décimal valide.")
        elif choice == "2. Convertir décimal en hexadécimal":
            try:
                decimal = int(value)
                result.set(Converter.decimal_to_hexadecimal(decimal))
            except ValueError: 
                messagebox.showerror(" ", "Veuillez entrer un nombre décimal valide.")
        elif choice == "3. Convertir binaire en décimal":
            if Validator.is_binary(value):
                result.set(Converter.binary_to_decimal(value))
            else:
                messagebox.showerror(" ", "Veuillez entrer une série de chiffres 0 ou 1.")
        elif choice == "4. Convertir binaire en hexadécimal":
            if Validator.is_binary(value):
                result.set(Converter.binary_to_hexadecimal(value))
            else:
                messagebox.showerror(" ", "Veuillez entrer une série de chiffres 0 ou 1.")
        elif choice == "5. Convertir hexadécimal en binaire":
            if Validator.is_hexadecimal(value):
                result.set(Converter.hexadecimal_to_binary(value))
            else:
                messagebox.showerror(" ", "Veuillez entrer une série de chiffres hexadécimaux (0-9, A-F).")
        elif choice == "6. Convertir hexadécimal en décimal":
            if Validator.is_hexadecimal(value):
                result.set(Converter.hexadecimal_to_decimal(value))
            else:
                messagebox.showerror(" ", "Veuillez entrer une série de chiffres hexadécimaux (0-9, A-F).")
        
        root.after_idle(resize_window)

def resize_window():
    root.update_idletasks()
    root.geometry(f"{root.winfo_reqwidth()}x{root.winfo_reqheight()}")

root = tk.Tk()
root.title("Convertisseur de nombres")

root.attributes("-topmost", True)

options = tk.Listbox(root, selectmode=tk.SINGLE, height=6, width=34)
options.insert(1, "1. Convertir décimal en binaire")
options.insert(2, "2. Convertir décimal en hexadécimal")
options.insert(3, "3. Convertir binaire en décimal")
options.insert(4, "4. Convertir binaire en hexadécimal")
options.insert(5, "5. Convertir hexadécimal en binaire")
options.insert(6, "6. Convertir hexadécimal en décimal")
options.grid(row=0, column=0, padx=10, pady=10, columnspan=3, sticky="ew")

entry_frame = tk.Frame(root)
entry_frame.grid(row=1, column=0, padx=5, pady=10, columnspan=3, sticky="ew")

entry = tk.Entry(entry_frame)
entry.pack(side=tk.LEFT, expand=True, fill=tk.X)

calculator_button = tk.Button(entry_frame, text="📝", command=show_calculator)
calculator_button.pack(side=tk.LEFT, padx=(5, 2))

clear_button = tk.Button(entry_frame, text="Effacer", command=clear_entry)
clear_button.pack(side=tk.RIGHT, padx=(2, 5))

convert_button = tk.Button(root, text="Convertir", command=convert, width=20, height=2)
convert_button.grid(row=2, column=0, columnspan=3, padx=5, pady=10)

result_frame = tk.Frame(root, bg="#f0f0f0", relief=tk.GROOVE, borderwidth=2, bd=2)
result_frame.grid(row=3, column=0, columnspan=3, padx=10, pady=5, sticky="ew")

result = tk.StringVar(root)
result_label = tk.Label(result_frame, textvariable=result, bg="#f0f0f0", padx=10, pady=10)
result_label.pack()

def bind_enter(event):
    convert()
root.bind('<Return>', bind_enter)

root.bind("<F11>", lambda event: "break")
root.attributes('-toolwindow', True)

root.resizable(False, False)

center_window(root)

root.mainloop()
