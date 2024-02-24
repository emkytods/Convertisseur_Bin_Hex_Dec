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
    x = (window.winfo_screenwidth() - width) // 2
    y = (window.winfo_screenheight() - height) // 2
    window.geometry(f'+{x}+{y}')

calculator_window_reference = None
history_window_reference = None
clear_history_button = None

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

    calculator_window.geometry(f'+{calculator_x}+{calculator_y}')

    calculator_window.bind("<F11>", lambda event: "break")
    calculator_window.attributes('-toolwindow', True)
    calculator_window.resizable(False, False)
    calculator_window.attributes("-topmost", True)

    for i in range(16):
        value = i if i < 10 else chr(ord('A') + i - 10)
        button = tk.Button(calculator_window, text=str(value), command=lambda val=value: insert_character(val), padx=6)
        button.grid(row=i // 4, column=i % 4, padx=4, pady=4)

    delete_button = tk.Button(calculator_window, text="      ◀︎", command=delete_character)
    delete_button.grid(row=4, column=0, columnspan=4, padx=4, pady=4)

def delete_character():
    current_text = entry.get()
    if current_text:
        updated_text = current_text[:-1]
        entry.delete(0, tk.END)
        entry.insert(tk.END, updated_text)

def insert_character(char):
    entry.insert(tk.END, str(char))

def check_result_length(result_value):
    if len(result_value) >= 30:
        messagebox.showinfo(" ", "Le résultat comporte trop de caractères.")
        return False
    return True

def copy_result():
    result_value = result.get()
    if result_value:
        root.clipboard_clear()
        root.clipboard_append(result_value)

def copy_result_without_prefix():
    result_value = result.get()
    if result_value:
        if result_value.startswith("0x"):
            result_value = result_value[2:]
        elif result_value.startswith("0b"):
            result_value = result_value[2:]
        root.clipboard_clear()
        root.clipboard_append(result_value)

def create_clear_history_button(parent_frame):
    global clear_history_button
    clear_history_button = tk.Button(parent_frame, text="Effacer l'historique", command=clear_history)
    clear_history_button.grid(row=2, column=0, columnspan=2, pady=(10, 0), sticky="ew")

def convert():
    result.set("")
    index = options.curselection()

    if not index:
        messagebox.showerror("Erreur", "Veuillez choisir une méthode de conversion.")
        return

    choice = options.get(index)
    value = entry.get()

    if value == "":
        messagebox.showerror(" ", "Veuillez entrer une valeur à convertir.")
        return

    conversion_info = ""
    if choice == "1. Convertir décimal -> binaire":
        try:
            decimal = int(value)
            result_value = Converter.decimal_to_binary(decimal)
            if check_result_length(result_value):
                if len(value) >= 17:
                    messagebox.showerror("Erreur", "La valeur à convertir est trop grande.")
                    return
                result_value = result_value.replace("0b", "")
                result.set(result_value)
                conversion_info = f"Décimal -> binaire : {value} -> {result_value}"
        except ValueError:
            messagebox.showerror(" ", "Veuillez entrer un nombre décimal valide.")
    elif choice == "2. Convertir décimal -> hexadécimal":
        try:
            decimal = int(value)
            result_value = Converter.decimal_to_hexadecimal(decimal)
            if check_result_length(result_value):
                if len(value) >= 20:
                    messagebox.showerror("Erreur", "La valeur à convertir est trop grande.")
                    return
                result_value = result_value.replace("0x", "")
                result.set(result_value)
                conversion_info = f"Décimal -> hexadécimal : {value} -> {result_value}"
        except ValueError:
            messagebox.showerror(" ", "Veuillez entrer un nombre décimal valide.")
    elif choice == "3. Convertir binaire -> décimal":
        if Validator.is_binary(value):
            result_value = str(Converter.binary_to_decimal(value))
            if check_result_length(result_value):
                if len(value) >= 25:
                    messagebox.showerror("Erreur", "La valeur à convertir est trop grande.")
                    return
                result.set(result_value)
                conversion_info = f"Binaire -> décimal : {value} -> {result_value}"
        else:
            messagebox.showerror(" ", "Veuillez entrer une série de chiffres 0 ou 1.")
    elif choice == "4. Convertir binaire -> hexadécimal":
        if Validator.is_binary(value):
            result_value = Converter.binary_to_hexadecimal(value)
            if check_result_length(result_value):
                if len(value) >= 25:
                    messagebox.showerror("Erreur", "La valeur à convertir est trop grande.")
                    return
                result_value = result_value.replace("0x", "")
                result.set(result_value)
                conversion_info = f"Binaire -> hexadécimal : {value} -> {result_value}"
        else:
            messagebox.showerror(" ", "Veuillez entrer une série de chiffres 0 ou 1.")
    elif choice == "5. Convertir hexadécimal -> binaire":
        if Validator.is_hexadecimal(value):
            result_value = Converter.hexadecimal_to_binary(value)
            if check_result_length(result_value):
                if len(value) >= 10:
                    messagebox.showerror("Erreur", "La valeur à convertir est trop grande.")
                    return
                result_value = result_value.replace("0b", "")
                result.set(result_value)
                conversion_info = f"Hexadécimal -> binaire : {value} -> {result_value}"
        else:
            messagebox.showerror(" ", "Veuillez entrer une série de chiffres hexadécimaux (0-9, A-F).")
    elif choice == "6. Convertir hexadécimal -> décimal":
        if Validator.is_hexadecimal(value):
            result_value = str(Converter.hexadecimal_to_decimal(value))
            if check_result_length(result_value):
                if len(value) >= 17:
                    messagebox.showerror("Erreur", "La valeur à convertir est trop grande.")
                    return
                result.set(result_value)
                conversion_info = f"Hexadécimal -> décimal : {value} -> {result_value}"
        else:
            messagebox.showerror(" ", "Veuillez entrer une série de chiffres hexadécimaux (0-9, A-F).")

    if conversion_info:
        history.append(conversion_info)
        if len(history) > 10:
            history.pop(0)

        if history_window_reference:
            update_history_window()

        root.after_idle(resize_window)

def resize_window():
    root.update_idletasks()
    root.geometry(f"{root.winfo_reqwidth()}x{root.winfo_reqheight()}")

def show_history():
    global history_window_reference
    if history_window_reference is None or not history_window_reference.winfo_exists():
        history_window_reference = tk.Toplevel(root)
        history_window_reference.title("Historique des conversions")
        history_window_reference.attributes('-toolwindow', True)
        history_window_reference.attributes("-topmost", True)
        history_window_reference.resizable(False, False)

        history_frame = tk.Frame(history_window_reference)
        history_frame.pack(padx=10, pady=10)

        history_label = tk.Label(history_frame, text="Historique des 10 dernières conversions :", font=("Calibri", 12, "bold"))
        history_label.grid(row=0, column=0, columnspan=2, pady=5)

        history_listbox = tk.Listbox(history_frame, height=10, width=70, font=("Calibri", 11))
        history_listbox.grid(row=1, column=0, columnspan=2)

        for item in reversed(history):
            item = item.replace("0x", "").replace("0b", "")
            history_listbox.insert(tk.END, item)

        create_clear_history_button(history_frame)

        history_window_reference.update_idletasks()
        width = history_window_reference.winfo_reqwidth()
        height = history_window_reference.winfo_reqheight()
        history_window_reference.geometry(f"{width}x{height}")

        root_x = root.winfo_x()
        root_y = root.winfo_y()
        history_x = root_x - 10 + root.winfo_width() + 20
        history_y = root_y
        history_window_reference.geometry(f"+{history_x}+{history_y}")

        history_window_reference.protocol("WM_DELETE_WINDOW", on_history_window_close)

def clear_history():
    global history
    history = []
    update_history_window()

def on_history_window_close():
    global history_window_reference
    if history_window_reference:
        history_window_reference.destroy()
        history_window_reference = None

def update_history_window():
    global history_window_reference
    if history_window_reference:
        history_window_reference.destroy()
        show_history()

root = tk.Tk()
root.title("Convertisseur de nombres")

root.attributes("-topmost", True)

options = tk.Listbox(root, selectmode=tk.SINGLE, height=6, width=34, font=("Calibri", 11), activestyle="none")
options.insert(1, "1. Convertir décimal -> binaire")
options.insert(2, "2. Convertir décimal -> hexadécimal")
options.insert(3, "3. Convertir binaire -> décimal")
options.insert(4, "4. Convertir binaire -> hexadécimal")
options.insert(5, "5. Convertir hexadécimal -> binaire")
options.insert(6, "6. Convertir hexadécimal -> décimal")
options.grid(row=0, column=0, padx=10, pady=10, columnspan=3, sticky="ew")

entry_frame = tk.Frame(root)
entry_frame.grid(row=1, column=0, padx=5, pady=1, columnspan=3, sticky="ew")

entry = tk.Entry(entry_frame)
entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=6)

calculator_button = tk.Button(entry_frame, text=" α ", command=show_calculator)
calculator_button.pack(side=tk.LEFT, padx=(5, 2))

clear_button = tk.Button(entry_frame, text="Effacer", command=clear_entry)
clear_button.pack(side=tk.RIGHT, padx=(2, 5))

convert_button = tk.Button(root, text="Convertir", command=convert, width=33, height=2)
convert_button.grid(row=2, column=0, columnspan=3, padx=5, pady=6)

result_frame = tk.Frame(root, relief=tk.GROOVE, borderwidth=2, bd=2)
result_frame.grid(row=4, column=0, columnspan=3, padx=10, pady=5, sticky="ew")

copy_button = tk.Button(root, text="Copier", command=copy_result_without_prefix)
copy_button.grid(row=5, column=0, columnspan=2, padx=(8, 0), pady=(2, 5), sticky="ew")

history_button = tk.Button(root, text=" Historique ", command=show_history, width=2, height=1)
history_button.grid(row=5, column=2, padx=(8, 11), pady=(2, 5), sticky="ew", rowspan=2)

result = tk.StringVar(root)
result_label = tk.Label(result_frame, textvariable=result, padx=10, pady=10)
result_label.pack()

history = []

def bind_enter(event):
    convert()
root.bind('<Return>', bind_enter)

root.bind("<F11>", lambda event: "break")
root.attributes('-toolwindow', True)

root.resizable(False, False)

center_window(root)

root.mainloop()
