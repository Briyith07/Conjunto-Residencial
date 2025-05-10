from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os


def generar_factura_pdf():

    print(f"📝 Error")  # Depuración
    # Ruta absoluta de la carpeta de facturas
    factura_dir = os.path.abspath(os.path.join("static", "facturas", "reservas"))
    os.makedirs(factura_dir, exist_ok=True)  # Asegura que la carpeta exista

    # Nombre del archivo PDF
    filename = f"factura_Reserva_.pdf"
    filepath = os.path.join(factura_dir, filename)

    print(f"📝 Guardando factura en: {filepath}")  # Depuración

    try:
        # Crear el PDF
        c = canvas.Canvas(filepath, pagesize=letter)
        width, height = letter

        c.setFont("Helvetica-Bold", 18)
        c.drawString(80, height - 60,"Hola")

        titulo = f"Factura Reserva"
        c.setFont("Helvetica-Bold", 14)
        c.drawString(130, height - 80, titulo)

        c.showPage()
        c.save()

        print(f"✅ Factura generada correctamente en: {filepath}")  # Depuración
        return filepath

    except Exception as e:
        print(f"❌ Error al generar el PDF: {e}")
        return None

from datetime import date
import os
from datetime import datetime, date, timedelta
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from models.facturacion import Factura, ConfiguracionFactura
from models.usuario import Usuarios
from models.roles import Roles
from app import db, create_app

app = create_app()


def generar_facturas_hasta_hoy():
    with app.app_context():  # Activa el contexto de la aplicación
        año_actual = date.today().year
        mes_actual = date.today().month

        # Obtener la configuración de facturación
        configuracion = ConfiguracionFactura.query.first()
        dia_habil_pago = configuracion.dia_habil_pago if configuracion else 10  

        # Obtener el rol de Residente
        rol_residente = Roles.query.filter_by(nombre="Residente").first()
        if not rol_residente:
            print("No se encontró el rol 'Residente'. No se generarán facturas.")
            return

        # Obtener todos los usuarios con el rol Residente
        usuarios_residentes = Usuarios.query.filter_by(id_rol=rol_residente.id).all()

        nuevas_facturas = []

        for usuario in usuarios_residentes:
            for mes in range(1, mes_actual + 1):
                fecha_max_pago = date(año_actual, mes, min(dia_habil_pago, 28))  

                # Evitar facturas duplicadas
                factura_existente = Factura.query.filter_by(usuario_id=usuario.id, mes=mes, year=año_actual).first()
                if factura_existente:
                    continue  

                # Crear la factura
                factura = Factura(
                    usuario_id=usuario.id,
                    mes=mes,
                    year=año_actual,
                    fecha_emision=date.today(),
                    fecha_max_pago=fecha_max_pago,
                    valor=configuracion.tarifa if configuracion else 150000.00,  
                    estado="Pendiente"
                )

                nuevas_facturas.append(factura)

        # Guardar en la base de datos
        if nuevas_facturas:
            db.session.bulk_save_objects(nuevas_facturas)
            db.session.commit()
            print(f"{len(nuevas_facturas)} facturas generadas correctamente para residentes.")
        else:
            print("No se generaron nuevas facturas, ya existen todas.")

# Ejecutar la función dentro del contexto de Flask
if __name__ == "__main__":
    generar_facturas_hasta_hoy()

#generar_factura_pdf()

