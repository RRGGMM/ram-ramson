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
    display_name = "Rectoria UTN - Departamento Academico"
    spoofed_email = "rectoria@utn.edu.mx"
    target_email = "ram14xd@outlook.com"
    
    # CONFIGURACION DE ARCHIVO ADJUNTO
    attachment_path = "Calendario_Academico_2025_UTN.pdf"
    
    # CONTENIDO MEJORADO + CONVINCENTE
    subject = "Nuevo Calendario Academico 2025 - UTN"
    
    body = f"""
Estimado miembro de la comunidad universitaria,

Nos complace informarle que el Calendario Academico 2025 ha sido aprobado
por el Consejo Directivo y se encuentra disponible para su consulta.

PRINCIPALES NOVEDADES:
• Inicio de clases: 3 de marzo 2025
• Periodo de examenes parciales: 16-27 de junio 2025  
• Vacaciones de invierno: 14-25 de julio 2025
• Examenes finales: 24 nov - 5 dic 2025
• Fin de ciclo lectivo: 12 de diciembre 2025

En el archivo adjunto encontrara el calendario completo con todas las fechas 
importantes y actividades institucionales programadas.

PARA VALIDAR ESTA INFORMACION:
Sitio web oficial: https://www.utn.edu.mx/academico
Contacto: {spoofed_email}
Telefono: +52 55 5628 7000

Cordialmente,
Rectoria - Universidad Tecnologica Nacional
Departamento de Planeacion Academica

---
*Mensaje generado automaticamente - No responder*
"""
    
    # CONSTRUCCION DEL EMAIL CON ADJUNTO
    msg = MIMEMultipart()
    
    # SPOOFING VISUAL mejorado
    msg['From'] = f'"{display_name}" <{gmail_user}>'
    msg['To'] = target_email
    msg['Subject'] = subject
    msg['Reply-To'] = spoofed_email
    
    msg.attach(MIMEText(body, 'plain'))
    
    # CREACION Y ADJUNCION DE ARCHIVO FALSO
    def create_fake_pdf():
        pdf_content = b"%PDF-1.4\n1 0 obj\n<<\n/Type /Catalog\n/Pages 2 0 R\n>>\nendobj\n2 0 obj\n<<\n/Type /Pages\n/Kids [3 0 R]\n/Count 1\n>>\nendobj\n3 0 obj\n<<\n/Type /Page\n/Parent 2 0 R\n/MediaBox [0 0 612 792]\n/Contents 4 0 R\n>>\nendobj\n4 0 obj\n<<\n/Length 44\n>>\nstream\nBT\n/F1 12 Tf\n72 720 Td\n(UTN - Calendario Academico 2025) Tj\nET\nendstream\nendobj\nxref\n0 5\n0000000000 65535 f \n0000000009 00000 n \n0000000058 00000 n \n0000000115 00000 n \n0000000239 00000 n \ntrailer\n<<\n/Size 5\n/Root 1 0 R\n>>\nstartxref\n304\n%%EOF"
        
        with open(attachment_path, "wb") as f:
            f.write(pdf_content)
        print(f"Archivo adjunto creado: {attachment_path}")

    # Crear y adjuntar archivo
    create_fake_pdf()
    
    try:
        with open(attachment_path, "rb") as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
        
        encoders.encode_base64(part)
        part.add_header(
            'Content-Disposition',
            f'attachment; filename= {attachment_path}',
        )
        msg.attach(part)
        print(f"Archivo adjuntado: {attachment_path}")
        
    except Exception as e:
        print(f"Error al adjuntar archivo: {e}")
        return

    # ENVIO DEL CORREO SPOOFED MEJORADO
    try:
        print("INICIANDO ATAQUE DE SPOOFING AVANZADO...")
        print("=" * 55)
        
        print("Conectando a servidor Gmail...")
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        
        print("Autenticando con App Password...")
        server.login(gmail_user, gmail_password)
        
        print("Enviando correo spoofed con adjunto...")
        server.sendmail(gmail_user, target_email, msg.as_string())
        server.quit()
        
        # Limpiar archivo temporal
        if os.path.exists(attachment_path):
            os.remove(attachment_path)
            
        print("ATAQUE EXITOSO!")
        print("=" * 55)
        print(f"REMITENTE VISUAL: {display_name}")
        print(f"REPLY-TO: {spoofed_email}") 
        print(f"OBJETIVO: {target_email}")
        print(f"ASUNTO: {subject}")
        print(f"ADJUNTO: {attachment_path}")
        print("\nPUNTOS DE CONVINCACION:")
        print("   - Nombre institucional formal")
        print("   - Archivo adjunto 'oficial'") 
        print("   - Informacion de contacto real")
        print("   - Lenguaje corporativo")
        
    except Exception as e:
        print(f"ERROR: {e}")
        if os.path.exists(attachment_path):
            os.remove(attachment_path)

def configurar_correo():
    print("\n--- CONFIGURACION DE CORREO ---")
    print("Configuracion actual:")
    print("1. Gmail User: piedrozadaniel@gmail.com")
    print("2. Target Email: ram14xd@outlook.com")
    print("3. Spoofed Email: rectoria@utn.edu.mx")
    print("4. Volver al menu principal")
    
    opcion = input("\nSeleccione opcion (1-4): ")
    return opcion

def mostrar_info():
    print("\n--- INFORMACION DEL SISTEMA ---")
    print("Sistema: Email Spoofing Demonstration")
    print("Version: 1.0")
    print("Python: 3.14.0")
    print("Proposito: Demostracion educativa de tecnicas de spoofing")
    print("\nADVERTENCIA: Este sistema es solo para fines educativos.")
    print("El uso malintencionado de estas tecnicas es ilegal.")

def menu_principal():
    while True:
        print("\n" + "="*50)
        print("SISTEMA DE DEMOSTRACION DE EMAIL SPOOFING")
        print("="*50)
        print("1. Enviar correo de demostracion")
        print("2. Configurar parametros")
        print("3. Informacion del sistema")
        print("4. Salir")
        print("-"*50)
        
        opcion = input("Seleccione una opcion (1-4): ")
        
        if opcion == "1":
            print("\nIniciando demostracion...")
            send_utn_spoofed_email()
            input("\nPresione Enter para continuar...")
            
        elif opcion == "2":
            config_opcion = configurar_correo()
            if config_opcion == "4":
                continue
            else:
                print("\nFuncionalidad de configuracion en desarrollo...")
                input("Presione Enter para continuar...")
                
        elif opcion == "3":
            mostrar_info()
            input("\nPresione Enter para continuar...")
            
        elif opcion == "4":
            print("\nSaliendo del sistema...")
            break
            
        else:
            print("\nOpcion no valida. Por favor, seleccione 1-4.")

if __name__ == "__main__":
    print("DEMOSTRACION: Email Spoofing Avanzado - UTN")
    print("Analisis + Explotacion + Tecnicas de Convincacion")
    menu_principal()