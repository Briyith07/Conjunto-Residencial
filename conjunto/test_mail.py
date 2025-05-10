import smtplib
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Obtener datos del .env
MAIL_SERVER = os.getenv("MAIL_SERVER")
MAIL_PORT = int(os.getenv("MAIL_PORT"))
MAIL_USERNAME = os.getenv("MAIL_USERNAME")
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")

try:
    print(f"Conectando a {MAIL_SERVER}:{MAIL_PORT}...")
    server = smtplib.SMTP(MAIL_SERVER, MAIL_PORT)
    server.starttls()  # Iniciar conexión segura
    server.login(MAIL_USERNAME, MAIL_PASSWORD)
    print("✅ Conexión exitosa y autenticación correcta.")
    server.quit()
except Exception as e:
    print(f"❌ Error al conectar o autenticar: {e}")
