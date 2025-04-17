import sys
import os
from tkinter import Button, Tk, Frame, END, Label


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

ventana = Tk()
ventana.geometry("254x460")
ventana.config(bg="white")
ventana.resizable(0, 0)
ventana.title("Calculadora")

# Variables globales para el funcionamiento de la calculadora
current_input = ""
operation = None
first_number = 0
memory = 0

def button_click(number):
    """Maneja el clic en los botones numéricos"""
    global current_input
    if current_input == "0" and number != ".":
        current_input = str(number)
    else:
        current_input += str(number)
    update_display()

def button_clear():
    """Limpia la pantalla y reinicia las variables"""
    global current_input, operation, first_number
    current_input = ""
    operation = None
    first_number = 0
    update_display("0")

def button_operation(op):
    """Maneja las operaciones matemáticas"""
    global current_input, operation, first_number
    if current_input:
        first_number = float(current_input)
        operation = op
        current_input = ""
        update_display("0")

def button_equal():
    """Realiza el cálculo y muestra el resultado"""
    global current_input, operation, first_number
    if not current_input or not operation:
        return 
    operations = {
        "+": lambda a, b: a + b,
        "-": lambda a, b: a - b,
        "x": lambda a, b: a * b,
        "÷": lambda a, b: a / b if b != 0 else "Error"
    }
    
    second_number = float(current_input)
    result = operations.get(operation)(first_number, second_number)
    
    # Formatear el resultado (evitar decimales innecesarios)
    if isinstance(result, float) and result.is_integer():
        result = int(result)
    
    current_input = str(result)
    operation = None
    update_display()

def button_sign():
    """Cambia el signo del número actual"""
    global current_input
    if current_input:
        if current_input[0] == '-':
            current_input = current_input[1:]
        else:
            current_input = '-' + current_input
        update_display()

def button_percent():
    """Convierte el número actual a porcentaje"""
    global current_input
    if current_input:
        num = float(current_input) / 100
        current_input = str(num)
        update_display()

def button_decimal():
    """Añade punto decimal"""
    global current_input
    if "." not in current_input:
        current_input += "."
        update_display()

def update_display(value=None):
    """Actualiza el display con el valor actual"""
    if value is None:
        value = current_input if current_input else "0"
    display_label.config(text=value)
    

    if len(value) > 10:
        display_label.config(font=("Montserrat", 24))
    else:
        display_label.config(font=("Montserrat", 32))
        
# Función para manejar eventos del teclado
def handle_keypress(event):
    key = event.char
    keysym = event.keysym

    # Teclas numéricas y decimal
    if key in '0123456789':
        button_click(int(key))
    elif key == '.':
        button_decimal()

    # Operaciones básicas
    elif key in '+':
        button_operation("+")
    elif key == '-':
        button_operation("-")
    elif key in 'x*':
        button_operation("x")
    elif key in '/÷':
        button_operation("÷")

    # Teclas especiales
    elif keysym == 'Return' or keysym == 'equal':
        button_equal()
    elif keysym == 'Escape':
        button_clear()
    elif keysym == 'percent':
        button_percent()

# Configurar bindings globales
ventana.bind('<Key>', handle_keypress)
# Opcional: Enfocar la ventana al inicio
ventana.focus_set()

# Frame principal
frame = Frame(ventana, bg="#212020", relief="raised")
frame.grid(column=0, row=0, padx=0, pady=0)

# Display moderno
display_frame = Frame(frame, bg="#212020")
display_frame.grid(columnspan=4, row=0, pady=6, padx=5,ipady=15, sticky="nsew")

display_label = Label(
    display_frame,
    text="0",
    bg="#212020",
    fg="white",
    font=("Montserrat", 32),
    anchor="e",
    padx=10
)
display_label.pack(fill="both", expand=True)

frame_botones = Frame(
    frame,
    bg="#F0F0F3",
    padx=15,
    pady=25,
)
frame_botones.grid(column=0, row=1, columnspan=4, sticky="nsew", ipady=65)

for i in range(4):
    frame.grid_columnconfigure(i, weight=1, uniform="cols")
    frame.grid_rowconfigure(i, weight=1)

class HoverButton(Button):
    def __init__(self, master, **kw):
        Button.__init__(self, master=master, **kw)
        self.defaultBackground = self["background"]
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        self["background"] = self["activebackground"]

    def on_leave(self, e):
        self["background"] = self.defaultBackground

# Botones con funcionalidad
Button_delete = HoverButton(
    frame_botones,
    text="C",
    borderwidth=0,
    height=2,
    width=4,
    font=("Oswald", 12, "bold"),
    relief="raised",
    fg="#898989",
    activebackground="#e0e0e0",
    bg="#fff",
    anchor="center",
    command=button_clear
)
Button_delete.grid(column=0, row=1, pady=6, padx=5)

Button_sign = HoverButton(
    frame_botones,
    text="+/-",
    borderwidth=0,
    height=2,
    width=4,
    font=("Oswald", 12, "bold"),
    relief="raised",
    fg="#898989",
    activebackground="#e0e0e0",
    bg="#fff",
    anchor="center",
    command=button_sign
)
Button_sign.grid(column=1, row=1, pady=6, padx=5)

Button_percent = HoverButton(
    frame_botones,
    text="%",
    borderwidth=0,
    height=2,
    width=4,
    font=("Oswald", 12, "bold"),
    relief="raised",
    fg="#898989",
    activebackground="#e0e0e0",
    bg="#fff",
    anchor="center",
    command=button_percent
)
Button_percent.grid(column=2, row=1, pady=6, padx=5)

Button_div = HoverButton(
    frame_botones,
    text="÷",
    borderwidth=0,
    height=2,
    width=4,
    font=("Oswald", 12, "bold"),
    relief="raised",
    fg="#27AE60",
    activebackground="#b0e0b0",
    bg="#fff",
    anchor="center",
    command=lambda: button_operation("÷")
)
Button_div.grid(column=3, row=1, pady=6, padx=5)

# Botones numéricos
Button_7 = HoverButton(
    frame_botones,
    text="7",
    borderwidth=0,
    height=2,
    width=4,
    font=("Oswald", 12, "bold"),
    relief="raised",
    fg="#728AB7",
    activebackground="#e0e0e0",
    bg="#fff",
    anchor="center",
    command=lambda: button_click(7)
)
Button_7.grid(column=0, row=2, pady=6, padx=5)

Button_8 = HoverButton(
    frame_botones,
    text="8",
    borderwidth=0,
    height=2,
    width=4,
    font=("Oswald", 12, "bold"),
    relief="raised",
    fg="#728AB7",
    activebackground="#e0e0e0",
    bg="#fff",
    anchor="center",
    command=lambda: button_click(8)
)
Button_8.grid(column=1, row=2, pady=6, padx=5)

Button_9 = HoverButton(
    frame_botones,
    text="9",
    borderwidth=0,
    height=2,
    width=4,
    font=("Oswald", 12, "bold"),
    relief="raised",
    fg="#728AB7",
    activebackground="#e0e0e0",
    bg="#fff",
    anchor="center",
    command=lambda: button_click(9)
)
Button_9.grid(column=2, row=2, pady=6, padx=5)

Button_x = HoverButton(
    frame_botones,
    text="×",
    borderwidth=0,
    height=2,
    width=4,
    font=("Oswald", 12, "bold"),
    relief="raised",
    fg="#27AE60",
    activebackground="#b0e0b0",
    bg="#fff",
    anchor="center",
    command=lambda: button_operation("x")
)
Button_x.grid(column=3, row=2, pady=6, padx=5)

Button_4 = HoverButton(
    frame_botones,
    text="4",
    borderwidth=0,
    height=2,
    width=4,
    font=("Oswald", 12, "bold"),
    relief="raised",
    fg="#728AB7",
    activebackground="#e0e0e0",
    bg="#fff",
    anchor="center",
    command=lambda: button_click(4)
)
Button_4.grid(column=0, row=3, pady=6, padx=5)

Button_5 = HoverButton(
    frame_botones,
    text="5",
    borderwidth=0,
    height=2,
    width=4,
    font=("Oswald", 12, "bold"),
    relief="raised",
    fg="#728AB7",
    activebackground="#e0e0e0",
    bg="#fff",
    anchor="center",
    command=lambda: button_click(5)
)
Button_5.grid(column=1, row=3, pady=6, padx=5)

Button_6 = HoverButton(
    frame_botones,
    text="6",
    borderwidth=0,
    height=2,
    width=4,
    font=("Oswald", 12, "bold"),
    relief="raised",
    fg="#728AB7",
    activebackground="#e0e0e0",
    bg="#fff",
    anchor="center",
    command=lambda: button_click(6)
)
Button_6.grid(column=2, row=3, pady=6, padx=5)

Button_minus = HoverButton(
    frame_botones,
    text="-",
    borderwidth=0,
    height=2,
    width=4,
    font=("Oswald", 12, "bold"),
    relief="raised",
    fg="#27AE60",
    activebackground="#b0e0b0",
    bg="#fff",
    anchor="center",
    command=lambda: button_operation("-")
)
Button_minus.grid(column=3, row=3, pady=6, padx=5)

Button_1 = HoverButton(
    frame_botones,
    text="1",
    borderwidth=0,
    height=2,
    width=4,
    font=("Oswald", 12, "bold"),
    relief="raised",
    fg="#728AB7",
    activebackground="#e0e0e0",
    bg="#fff",
    anchor="center",
    command=lambda: button_click(1)
)
Button_1.grid(column=0, row=4, pady=6, padx=5)

Button_2 = HoverButton(
    frame_botones,
    text="2",
    borderwidth=0,
    height=2,
    width=4,
    font=("Oswald", 12, "bold"),
    relief="raised",
    fg="#728AB7",
    activebackground="#e0e0e0",
    bg="#fff",
    anchor="center",
    command=lambda: button_click(2)
)
Button_2.grid(column=1, row=4, pady=6, padx=5)

Button_3 = HoverButton(
    frame_botones,
    text="3",
    borderwidth=0,
    height=2,
    width=4,
    font=("Oswald", 12, "bold"),
    relief="raised",
    fg="#728AB7",
    activebackground="#e0e0e0",
    bg="#fff",
    anchor="center",
    command=lambda: button_click(3)
)
Button_3.grid(column=2, row=4, pady=6, padx=5)

Button_plus = HoverButton(
    frame_botones,
    text="+",
    borderwidth=0,
    height=2,
    width=4,
    font=("Oswald", 12, "bold"),
    relief="raised",
    fg="#27AE60",
    activebackground="#b0e0b0",
    bg="#fff",
    anchor="center",
    command=lambda: button_operation("+")
)
Button_plus.grid(column=3, row=4, pady=6, padx=5)

# Botón 0
btn_wide = HoverButton(
    frame_botones,
    text="0",
    borderwidth=0,
    height=2,
    font=("Oswald", 12, "bold"),
    relief="raised",
    fg="#728AB7",
    activebackground="#e0e0e0",
    bg="#fff",
    anchor="center",
    command=lambda: button_click(0)
)
btn_wide.grid(column=0, row=5, columnspan=2, pady=6, padx=5, sticky="ew")

# Botón punto decimal
Button_decimal = HoverButton(
    frame_botones,
    text=".",
    borderwidth=0,
    height=2,
    width=4,
    font=("Oswald", 12, "bold"),
    relief="raised",
    fg="#728AB7",
    activebackground="#e0e0e0",
    bg="#fff",
    anchor="center",
    command=button_decimal
)
Button_decimal.grid(column=2, row=5, pady=6, padx=5)

# Botón igual
btn_small = HoverButton(
    frame_botones,
    text="=",
    borderwidth=0,
    height=2,
    width=4, 
    font=("Oswald", 12, "bold"),
    relief="raised",
    fg="#fff",
    activebackground="#1E8449",
    bg="#27AE60",
    anchor="center",
    command=button_equal
)
btn_small.grid(column=3, row=5, pady=6, padx=5)  

ventana.mainloop()