Python 3.14.0 (tags/v3.14.0:ebf955d, Oct  7 2025, 10:15:03) [MSC v.1944 64 bit (AMD64)] on win32
Enter "help" below or click "Help" above for more information.
#!/usr/bin/env python3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os

def send_utn_spoofed_email():
    # =============================================
    # 🔐 CONFIGURACIÓN DE CUENTA REAL
    # =============================================
    gmail_user = "piedrozadaniel@gmail.com"      # ✏️ TU GMAIL REAL
    gmail_password = "xuawyofxhwudgrdn"          # ✏️ TU APP PASSWORD
    
    # =============================================
    # 🎭 CONFIGURACIÓN DE SUPLANTACIÓN MEJORADA
    # =============================================
    # ✏️ EDITAR: Versión más CREÍBLE
    display_name = "Rectoría UTN - Departamento Académico"  # ✏️ Más específico
    spoofed_email = "rectoria@utn.edu.mx"                   # ✏️ Email más "oficial"
    target_email = "ram14xd@outlook.com"                    # ✏️ OBJETIVO
    
    # =============================================
    # 📎 CONFIGURACIÓN DE ARCHIVO ADJUNTO
    # =============================================
    # ✏️ EDITAR: Nombre del archivo (hacerlo CREÍBLE)
    attachment_path = "Calendario_Academico_2025_UTN.pdf"
    
    # =============================================
    # 📧 CONTENIDO MEJORADO + CONVINCENTE
    # =============================================
    # ✏️ EDITAR: Asunto específico y urgente
    subject = "Nuevo Calendario Académico 2025 - UTN"
    
    # ✏️ EDITAR: Cuerpo más elaborado y oficial
    body = f"""
Estimado miembro de la comunidad universitaria,

Nos complace informarle que el Calendario Académico 2025 ha sido aprobado
por el Consejo Directivo y se encuentra disponible para su consulta.

PRINCIPALES NOVEDADES:
• Inicio de clases: 3 de marzo 2025
• Período de exámenes parciales: 16-27 de junio 2025  
• Vacaciones de invierno: 14-25 de julio 2025
• Exámenes finales: 24 nov - 5 dic 2025
• Fin de ciclo lectivo: 12 de diciembre 2025

En el archivo adjunto encontrará el calendario completo con todas las fechas 
importantes y actividades institucionales programadas.

PARA VALIDAR ESTA INFORMACIÓN:
Sitio web oficial: https://www.utn.edu.mx/academico
Contacto: {spoofed_email}
Teléfono: +52 55 5628 7000

Cordialmente,
Rectoría - Universidad Tecnológica Nacional
Departamento de Planeación Académica

---
*Mensaje generado automáticamente - No responder*
"""
...     
...     # =============================================
...     # 🔧 CONSTRUCCIÓN DEL EMAIL CON ADJUNTO
...     # =============================================
...     msg = MIMEMultipart()
...     
...     # 🎭 SPOOFING VISUAL mejorado
...     msg['From'] = f'"{display_name}" <{gmail_user}>'  # ✏️ Nombre institucional
...     msg['To'] = target_email
...     msg['Subject'] = subject
...     msg['Reply-To'] = spoofed_email  # ✏️ Respuestas al dominio spoofed
...     
...     msg.attach(MIMEText(body, 'plain'))
...     
...     # =============================================
...     # 📎 CREACIÓN Y ADJUNCIÓN DE ARCHIVO FALSO
...     # =============================================
...     def create_fake_pdf():
...         # ✏️ EDITAR: Contenido del PDF simulado
...         pdf_content = b"%PDF-1.4\n1 0 obj\n<<\n/Type /Catalog\n/Pages 2 0 R\n>>\nendobj\n2 0 obj\n<<\n/Type /Pages\n/Kids [3 0 R]\n/Count 1\n>>\nendobj\n3 0 obj\n<<\n/Type /Page\n/Parent 2 0 R\n/MediaBox [0 0 612 792]\n/Contents 4 0 R\n>>\nendobj\n4 0 obj\n<<\n/Length 44\n>>\nstream\nBT\n/F1 12 Tf\n72 720 Td\n(UTN - Calendario Academico 2025) Tj\nET\nendstream\nendobj\nxref\n0 5\n0000000000 65535 f \n0000000009 00000 n \n0000000058 00000 n \n0000000115 00000 n \n0000000239 00000 n \ntrailer\n<<\n/Size 5\n/Root 1 0 R\n>>\nstartxref\n304\n%%EOF"
...         
...         with open(attachment_path, "wb") as f:
...             f.write(pdf_content)
...         print(f"📄 Archivo adjunto creado: {attachment_path}")
... 
...     # Crear y adjuntar archivo
...     create_fake_pdf()
...     
...     try:
...         with open(attachment_path, "rb") as attachment:
...             part = MIMEBase('application', 'octet-stream')
...             part.set_payload(attachment.read())
...         
...         encoders.encode_base64(part)
        part.add_header(
            'Content-Disposition',
            f'attachment; filename= {attachment_path}',
        )
        msg.attach(part)
        print(f"📎 Archivo adjuntado: {attachment_path}")
        
    except Exception as e:
        print(f"❌ Error al adjuntar archivo: {e}")
        return

    # =============================================
    # 🚀 ENVÍO DEL CORREO SPOOFED MEJORADO
    # =============================================
    try:
        print("🎯 INICIANDO ATAQUE DE SPOOFING AVANZADO...")
        print("=" * 55)
        
        print("🚀 Conectando a servidor Gmail...")
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        
        print("🔐 Autenticando con App Password...")
        server.login(gmail_user, gmail_password)
        
        print("📧 Enviando correo spoofed con adjunto...")
        server.sendmail(gmail_user, target_email, msg.as_string())
        server.quit()
        
        # Limpiar archivo temporal
        if os.path.exists(attachment_path):
            os.remove(attachment_path)
            
        print("✅ ¡ATAQUE EXITOSO!")
        print("=" * 55)
        print(f"🎭 REMITENTE VISUAL: {display_name}")
        print(f"📧 REPLY-TO: {spoofed_email}") 
        print(f"🎯 OBJETIVO: {target_email}")
        print(f"📄 ASUNTO: {subject}")
        print(f"📎 ADJUNTO: {attachment_path}")
        print("\n💡 PUNTOS DE CONVINCACIÓN:")
        print("   • Nombre institucional formal")
        print("   • Archivo adjunto 'oficial'") 
        print("   • Información de contacto real")
        print("   • Lenguaje corporativo")
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        if os.path.exists(attachment_path):
            os.remove(attachment_path)

if __name__ == "__main__":
    print("🎓 DEMOSTRACIÓN: Email Spoofing Avanzado - UTN")
    print("🔍 Análisis + Explotación + Técnicas de Convincación")
