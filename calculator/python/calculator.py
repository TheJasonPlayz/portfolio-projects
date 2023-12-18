import tkinter as tk
from tkinter import ttk
import math
import re

decimal = r".*\.0$"


class CalcButton(tk.Button):
    def __init__(self, obj, text, row, column):
        super().__init__(obj, text=text,
                         command=lambda: update_display(text), width=5, height=5)
        self.grid(row=row, column=column, sticky="nsew", padx=2, pady=2)


def format(prev: str, string: str):
    if prev == "None":
        prev = ""
    if string in "1234567890.":
        return prev + string
    elif string in "+-/x":
        return f"{prev} {string} "
    elif string in ["1/x", "sq(x)", "sqrt(x)", "+/-"]:
        return calculate_last(string, prev)
        pass
    else:
        pass


def setOrNone(string: str):
    if re.search(decimal, string) is not None:
        s = slice(0, len(string) - 2)
        string = string[s]
    print("String to display:", string)
    display_text.set(string)
    if display_text.get() == "None":
        display_text.set("")


def update_display(string: str):
    setOrNone(format(display_text.get(), string))


def calculate_last(op, string):
    ops = string.split(" ")
    target = ops[-1]
    target = float(target)
    match op:
        case '1/x':
            target = 1 / target
        case 'sq(x)':
            target = pow(target, 2)
        case 'sqrt(x)':
            target = math.sqrt(target)
        case '+/-':
            target = -target
    ops[-1] = str(target)
    return " ".join(ops)


def calculate_backend(op, op1, op2):
    calc = 0
    op1 = float(op1)
    op2 = float(op2)
    match op:
        case "+":
            calc = op1 + op2
        case "-":
            calc = op1 - op2
        case "x":
            calc = op1 * op2
        case "/":
            calc = op1 / op2
    return calc


def calculate(calc_string: str):
    ops = calc_string.split(" ")
    while len(ops) >= 3:
        while "x" in ops or "/" in ops:
            op_i = 0
            try:
                op_i = ops.index("x")
            except Exception:
                op_i = ops.index("/")
            ops[op_i] = calculate_backend(ops[op_i], ops[op_i-1], ops[op_i+1])
            del ops[op_i-1]
            del ops[op_i]
        if len(ops) >= 3:
            ops[1] = calculate_backend(ops[1], ops[0], ops[2])
            del ops[0]
            del ops[1]
    ops[0] = str(ops[0])

    setOrNone(ops[0])


root = tk.Tk()
root.title("Calculator")
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=1)

display_text = tk.StringVar()
display = tk.Frame(root, height=50)
display.grid(column=0, row=0, sticky="nsew")
display_label = tk.Label(
    display, textvariable=display_text, bg="#f3f3f3")
display_label.place(relheight=1, relwidth=1)

buttons = tk.Frame(root, bg="#f3f3f3")
buttons.grid(column=0, row=1, sticky="nsew")
for i in range(4):
    for j in range(4):
        buttons.rowconfigure(i, weight=1)
        buttons.columnconfigure(j, weight=1)

div_by_1_button = CalcButton(buttons, "1/x", 0, 0)
square_button = CalcButton(buttons, "sq(x)", 0, 1)
square_root_button = CalcButton(buttons, "sqrt(x)", 0, 2)
div_button = CalcButton(buttons, "/", 0, 3)

seven_button = CalcButton(buttons, "7", 1, 0)
eight_button = CalcButton(buttons, "8", 1, 1)
nine_button = CalcButton(buttons, "9", 1, 2)
mult_button = CalcButton(buttons, "x", 1, 3)

four_button = CalcButton(buttons, "4", 2, 0)
five_button = CalcButton(buttons, "5", 2, 1)
six_button = CalcButton(buttons, "6", 2, 2)
sub_button = CalcButton(buttons, "-", 2, 3)

one_button = CalcButton(buttons, "1", 3, 0)
two_button = CalcButton(buttons, "2", 3, 1)
three_button = CalcButton(buttons, "3", 3, 2)
add_button = CalcButton(buttons, "+", 3, 3)

negate_button = CalcButton(buttons, "+/-", 4, 0)
zero_button = CalcButton(buttons, "0", 4, 1)
decimal_button = CalcButton(buttons, ".", 4, 2)
calculate_button = ttk.Button(
    buttons, text="=", style="winButton.TButton", command=lambda: calculate(display_text.get()))
calculate_button.grid(row=4, column=3, padx=2, pady=2)

