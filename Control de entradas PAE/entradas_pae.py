import tkinter as tk
from datetime import datetime
import pandas as pd
from playsound3 import playsound
    
# crea la ventana principal
root = tk.Tk()
root.title("Verificacion de entrada")
root.geometry("{}x{}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
root.resizable(False, False)

root.attributes('-topmost', True)
root.attributes('-fullscreen', True)
root.focus_force()

# barra superior de color segun respuesta
barra = tk.Canvas(root, height=36, bg="blue")
barra.pack(fill=tk.X)
barra.grid(row=0, column=0, columnspan=2, sticky="news")

# lista predefinida de identificaciones validas
ids_secundaria = pd.read_excel('ids_secundaria.xlsx', dtype=str)
ids_primaria = pd.read_excel('ids_primaria.xlsx', dtype=str)
historial_path_secundaria = 'vhistorial_secundaria.xlsx'
historial_path_primaria = 'vhistorial_primaria.xlsx'
actual_historial_path = 'vhistorial_secundaria.xlsx'
valid_ids = ids_secundaria
historial = pd.read_excel(actual_historial_path)
count_text = "Estudiantes secundaria"
num_strings = valid_ids['ID'].count()
num_actual = historial['ID'].count()


def clicked(event):
    global ids_secundaria, ids_primaria, historial_path_secundaria, historial_path_primaria, actual_historial_path, valid_ids, historial, count_text, num_strings, num_actual
    
    if count_text == "Estudiantes secundaria":
        count_text = "Estudiantes primaria"
        valid_ids = ids_primaria
        actual_historial_path = historial_path_primaria
        num_strings = valid_ids['ID'].count()
        historial = pd.read_excel(actual_historial_path)
        num_actual = historial['ID'].count()
        
    elif count_text == "Estudiantes primaria":
        count_text = "Estudiantes secundaria"
        valid_ids = ids_secundaria
        actual_historial_path = historial_path_secundaria
        num_strings = valid_ids['ID'].count()
        historial = pd.read_excel(actual_historial_path)
        num_actual = historial['ID'].count()
    barra.itemconfig(cont, text=f"{count_text}: {num_actual}/{num_strings}", fill="white")
    return

buttonBG = barra.create_rectangle(root.winfo_screenwidth()-305, 7, root.winfo_screenwidth()-345, 32, fill="white", outline="light grey")
#buttonTXT = barra.create_text(root.winfo_screenwidth()-315, 20, text="click", fill="gray")
barra.tag_bind(buttonBG, "<Button-1>", clicked) ## when the square is clicked runs function "clicked".
#barra.tag_bind(buttonTXT, "<Button-1>", clicked) ## same, but for the text.

status_id= barra.create_text(
    5, 20,
    text="Estado: Standby",
    font=("Arial", 16, "bold"),
    fill="white",
    anchor="w"
)

with open('cierre.txt', "r") as file:
    close_pass = [line.strip() for line in file]
    
with open('rein.txt', "r") as file:
    rein_pass = [line.strip() for line in file]

cont = barra.create_text(
    root.winfo_screenwidth()-15, 20,
    text=f"{count_text}: {num_actual}/{num_strings}",
    font=("Arial", 14, "bold"),
    fill="white",
    anchor="e"
)

def verify_entry():
    global ids_secundaria, ids_primaria, historial_path_secundaria, historial_path_primaria, actual_historial_path, valid_ids, historial, count_text, num_strings, num_actual
    historial = pd.read_excel(actual_historial_path)
    student_id = text_id.get("1.0", tk.END).strip()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    fecha = datetime.now().strftime("%Y-%m-%d")
    hora = datetime.now().strftime("%H:%M:%S")
    semana = datetime.now().strftime("%V")

    if not student_id:
        historial = pd.read_excel(actual_historial_path)
        num_actual = historial['ID'].count()
        status_label.config(text="Ninguna ID escaneada todavia.")
        barra.itemconfig(status_id, text="Estado: Standby", fill="white")
        barra.itemconfig(cont, text=f"{count_text}: {num_actual}/{num_strings}", fill="white")
        barra.configure(bg='blue')
        return

    if student_id in valid_ids['ID'].values:
        historial = pd.read_excel(actual_historial_path)
        num_actual = historial['ID'].count()
        row_index = valid_ids.index[valid_ids['ID'] == student_id].tolist()
        nombre = valid_ids._get_value(row_index[0], 'Nombre')
        apellido = valid_ids._get_value(row_index[0], 'Apellido')
        grado = valid_ids._get_value(row_index[0], 'Grado')
        if student_id in historial['ID'].values:
            historial = pd.read_excel(actual_historial_path)
            num_actual = historial['ID'].count()
            status_label.config(text=f"{student_id} - {nombre} {apellido} {grado} ya ha entrado hoy.")
            barra.itemconfig(status_id, text="Estado: Ya ingresado", fill="white")
            barra.itemconfig(cont, text=f"{count_text}: {num_actual}/{num_strings}", fill="white")
            barra.configure(bg='red')
        else:
            historial = pd.read_excel(actual_historial_path)
            num_actual = historial['ID'].count()
            status_label.config(text=f"{student_id} - {nombre} {apellido} {grado} permitido")
            barra.itemconfig(status_id, text="Estado: Permitido", fill="white")
            barra.itemconfig(cont, text=f"{count_text}: {num_actual}/{num_strings}", fill="white")
            barra.configure(bg='green')

    else:
        historial = pd.read_excel(actual_historial_path)
        num_actual = historial['ID'].count()
        status_label.config(text=f"ID inválido: {student_id}")
        barra.itemconfig(status_id, text="Estado: ID inválido", fill="white")
        barra.itemconfig(cont, text=f"{count_text}: {num_actual}/{num_strings}", fill="white")
        barra.configure(bg='red')

    if student_id in close_pass:
        root.destroy()
        
    if student_id in rein_pass:
        historial = pd.read_excel(actual_historial_path)
        num_actual = historial['ID'].count()
        try:
            # lee el  archivo existente
            historial_semanal = pd.read_excel('Estadisticas de entrada.xlsx')
        except FileNotFoundError:
            # si el archivo no existe crea un nuevo dataframe
            historial_semanal = pd.DataFrame(columns=['Semana', 'Fecha', 'Primaria', 'Secundaria'])
        # anexa nueva informacion
        historial_diario = pd.read_excel(actual_historial_path)
        
        hp = pd.read_excel('vhistorial_primaria.xlsx')
        hs = pd.read_excel('vhistorial_secundaria.xlsx')
        
        new_data = {
            'Semana': [int(semana)],
            'Fecha': [fecha],
            'Primaria': [f"{hp['ID'].count()}/{ids_primaria['ID'].count()}"],
            'Secundaria': [f"{hs['ID'].count()}/{ids_secundaria['ID'].count()}"],
        }
        new_df = pd.DataFrame(new_data)
        
        historial_semanal = pd.concat([historial_semanal, new_df], ignore_index=True)
        # lo escribe al archivo excel
        historial_semanal.to_excel('Estadisticas de entrada.xlsx', index=False)
        status_label.config(text="El recuento de entradas ha sido restablecido.")
        #limpia el hisotiral diario
        historial_diario = pd.DataFrame(columns=historial_diario.columns)
        historial_diario.to_excel(historial_path_primaria, index=False)
        historial_diario.to_excel(historial_path_secundaria, index=False)
        num_actual=0
        barra.itemconfig(status_id, text="Estado: Standby", fill="white")
        barra.itemconfig(cont, text=f"{count_text}: {num_actual}/{num_strings}", fill="white")
        barra.configure(bg='blue')

    # limpia la entrada de texto despues de la verificacion
    text_id.delete("1.0", tk.END)

    # agregar entrada al historial
    if student_id not in valid_ids['ID'].values and student_id not in rein_pass:
        status = "ID inválido"
        history_text.insert(tk.END, f"{now} - ID: {student_id} - {status}\n")
        playsound('Microsoft Windows 98 Error.mp3', block=False)
    elif student_id in historial['ID'].values:
        status = "Ingreso no permitido, ya entró hoy"
        history_text.insert(tk.END, f"{now} - ID: {student_id} ({nombre} {apellido} {grado}) - {status}\n")
        playsound('Microsoft Windows 98 Error.mp3', block=False)
    else:
        status = "Ingreso permitido"
        history_text.insert(tk.END, f"{now} - ID: {student_id} ({nombre} {apellido} {grado}) - {status}\n")

    history_text.see(tk.END)

    # añade al historial
    try:
        # lee el  archivo existente
        historial_diario = pd.read_excel(actual_historial_path)
    except FileNotFoundError:
        # si el archivo no existe crea un nuevo dataframe
        historial_diario = pd.DataFrame(columns=['Fecha', 'Hora', 'ID', 'Nombre', 'Apellido', 'Grado'])

    # crea nueva informacion para anexar al historial
    new_data = {
        'Fecha': [fecha],
        'Hora' : [hora],
        'ID': [student_id],
        'Nombre': [nombre],
        'Apellido': [apellido],
        'Grado': [grado]
    }

    new_df = pd.DataFrame(new_data)
    
    if student_id in valid_ids['ID'].values and student_id not in historial['ID'].values:
        # anexa nueva informacion
        historial_diario = pd.concat([historial_diario, new_df], ignore_index=True)
        # lo escribe al archivo excel
        historial_diario.to_excel(actual_historial_path, index=False)
        
    historial = pd.read_excel(actual_historial_path)
    num_actual = historial['ID'].count()
    barra.itemconfig(cont, text=f"{count_text}: {num_actual}/{num_strings}", fill="white")


# etiqueta para mostrar la identificacion escaneada
id_label = tk.Label(root, text="ID escaneada:", font=("Arial", 16), fg="grey")
id_label.grid(row=2, column=0, columnspan=2, sticky="ew")

# entrada de texto para id
text_id = tk.Text(root, width=20, height=1, font=("Arial", 14))
text_id.grid(row=3, column=0, columnspan=2, sticky="ew", padx=300)

# etiqueta de estado para respuesta a tiempo real
status_label = tk.Label(root, text="Esperando ID", font=("Arial", 22), fg="black")
status_label.grid(row=1, column=0, columnspan=2, sticky="ew")

# historial de entradas
history_text = tk.Text(root, width=40, height=10, font=("Arial", 13), wrap=tk.WORD)
history_text.grid(row=4, column=0, columnspan=2, sticky="nsew", padx=10, pady=0)

# activa la verificacion tras el escaneo con el lector de codigo de barras
text_id.bind("<KeyRelease-Return>", lambda event: verify_entry())

# selecciona la entrada de texto automaticamente
text_id.focus_set()

creat = tk.Label(root, text="Aplicación desarrollada por Gabriela Linares y Alan Monroy. Estudiantes de 11C — IELP 2026", font=("Arial", 12), fg="light grey")
creat.grid(row=5, column=0, columnspan=2, sticky="ew", pady=10)

root.grid_rowconfigure(0, weight=0)
root.grid_rowconfigure(1, weight=2)
root.grid_rowconfigure(2, weight=0)
root.grid_rowconfigure(3, weight=1)
root.grid_rowconfigure(4, weight=2)
root.grid_rowconfigure(5, weight=0)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

root.mainloop()