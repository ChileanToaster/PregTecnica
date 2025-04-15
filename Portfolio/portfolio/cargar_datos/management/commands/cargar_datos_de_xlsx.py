from django.core.management.base import BaseCommand, CommandError
from activos.services import activo_get_or_create, precio_activo_get_or_create
from portafolios.services import portafolio_get_or_create
import pandas as pd
from pathlib import Path
from decimal import Decimal, ROUND_HALF_UP

class Command(BaseCommand):
    help = 'Carga el historial de precios de activos em un archivo Excel con formato establecido a la base de datos. Además, crea los portafolios'
    output_transaction = True

    def add_arguments(self, parser):
        parser.add_argument('--archivo', type=str, help='Opcional, se usa cargar_datos/datos/datos.xlsx por defecto. Ruta del archivo Excel (.xlsx) a cargar')

    def handle(self, *args, **options):
        # Obtener el archivo de Excel de los argumentos
        archivo = options['archivo']

        # Si no se proporciona un archivo, usar el por defecto
        if not archivo:
            archivo = Path(__file__).resolve().parent.parent.parent / "datos" / "datos.xlsx"

        try:
            # Leer el archivo Excel como dataframe
            df_weights = pd.read_excel(archivo, sheet_name='weights')
            df_precios = pd.read_excel(archivo, sheet_name='Precios')
        except Exception as e:
            raise CommandError(f'Error al leer el archivo Excel: {e}')

    # Creación de activos e historial de precios

        lista_activos = []
        # Crear activos en la base de datos si no existen
        for activo in df_precios.columns.values[1:]:
            try:
                act = activo_get_or_create(activo)
                # Agregar el activo a la lista de activos para crear historial de precios posteriormente
                if act not in lista_activos:
                    lista_activos.append(act)
            except Exception as e:
                raise CommandError(f'Error al crear el activo {activo}: {e}')
        
        # Crear historial de precios de activos en la base de datos
        for index, row in df_precios.iterrows():
            fecha = row['Dates'].strftime('%Y-%m-%d')
            for activo in lista_activos:
                precio = row[activo.nombre]
                # Redondear el número a 6 decimales
                precio = Decimal(precio).quantize(Decimal("0.000001"), rounding=ROUND_HALF_UP)
                try:
                    precio_activo_get_or_create(activo, fecha, precio)
                except Exception as e:
                    raise CommandError(f'Error al crear el precio del activo {activo} en la fecha {fecha}: {e}')
                
    # Creación de portafolios

        for portafolio in df_weights.columns.values[2:]:
            try:
                # Crear el portafolio en la base de datos
                portafolio_get_or_create(portafolio)
            except Exception as e:
                raise CommandError(f'Error al crear el portafolio {portafolio}: {e}')
