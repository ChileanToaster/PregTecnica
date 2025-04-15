from django.core.management.base import BaseCommand, CommandError
from activos.services import activo_get, precio_activo_get
from portafolios.services import portafolio_get, activo_portafolio_get, activo_portafolio_create, activo_portafolio_modify
from portafolios.models import ActivoPortafolio
import pandas as pd
from pathlib import Path
from decimal import Decimal, ROUND_HALF_DOWN

class Command(BaseCommand):

    help = 'Dado un valor inicial de portafolios, calcula las cantidades de cada activo en cada uno de los portafolios y los guarda como ActivoPortafolio'

    def add_arguments(self, parser):
        parser.add_argument('valor_inicial', type=float, help='Valor inicial de los portafolios')
        parser.add_argument('--archivo', type=str, help='Ruta del archivo CSV que contiene los portafolios y activos')

    def handle(self, *args, **options):

        # Obtener el valor inicial de los portafolios
        valor_inicial = options['valor_inicial']
        if valor_inicial < 0:
            raise CommandError('El valor inicial no puede ser negativo.')
        # Obtener el archivo Excel de los argumentos
        archivo = options['archivo']

        # Si no se proporciona un archivo, usar el por defecto
        if not archivo:
            archivo = Path(__file__).resolve().parent.parent.parent / "datos" / "datos.xlsx"

        try:
            # Leer el archivo Excel como dataframe
            df_weights = pd.read_excel(archivo, sheet_name='weights')

        except Exception as e:
            raise CommandError(f'Error al leer el archivo Excel: {e}')
        
        # Rescatar la fecha donde se midieron los pesos
        fecha = df_weights['Fecha'][0].strftime('%Y-%m-%d')

        # Obtener la lista de portafolios
        portafolios = df_weights.columns.values[2:].tolist()

        # Iterar sobre cada fila del dataframe
        for index, row in df_weights.iterrows():
            # Obtener el portafolio y su peso
            for portafolio in portafolios:
                peso = row[portafolio]
                # Obtener el portafolio de la base de datos
                try:
                    portafolio_db = portafolio_get(portafolio)
                except Exception as e:
                    raise CommandError(f'Error al obtener el portafolio {portafolio}: {e}')

                activo = row['activos']
                # Obtener el activo y su precio de la base de datos
                try:
                    activo_db = activo_get(activo)
                except Exception as e:
                    raise CommandError(f'Error al obtener el activo {activo}: {e}')
                try:
                    precioactivo_db = precio_activo_get(activo_db, fecha)
                except Exception as e:
                    raise CommandError(f'Error al obtener el precio del activo {activo_db} en la fecha {fecha}: {e}')
                
                # Calcular la cantidad de activos en el portafolio
                cantidad = (peso * valor_inicial) / float(precioactivo_db.precio)
                # Redondear la cantidad a 5 decimales
                cantidad = Decimal(cantidad).quantize(Decimal("0.00001"), rounding=ROUND_HALF_DOWN)
                
                # Si el par activo-portafolio ya existe, actualizar la cantidad
                if ActivoPortafolio.objects.filter(portafolio=portafolio_db, activo=activo_db).exists():
                    activo_portafolio = activo_portafolio_get(portafolio=portafolio_db, activo=activo_db)
                    # Actualizar la cantidad
                    activo_portafolio_modify(portafolio=portafolio_db, activo=activo_db, nueva_cantidad=cantidad)
                # Si no, crear el par en la base de datos
                else:
                    try:
                        activo_portafolio_create(portafolio=portafolio_db, activo=activo_db, cantidad=cantidad)
                    except Exception as e:
                        raise CommandError(f'Error al crear el par activo-portafolio {activo} - {portafolio}: {e}')

        # Imprimir las cantidades de activos en cada portafolio
        for portafolio in portafolios:
            try:
                portafolio_db = portafolio_get(portafolio)
            except Exception as e:
                raise CommandError(f'Error al obtener el portafolio {portafolio}: {e}')

            activos_portafolio = ActivoPortafolio.objects.filter(portafolio=portafolio_db)
            self.stdout.write(self.style.SUCCESS(f'\nPortafolio: {portafolio}\n'))
            for activo_portafolio in activos_portafolio:
                self.stdout.write(self.style.SUCCESS(f'Activo: {activo_portafolio.activo}, Cantidad: {activo_portafolio.cantidad}'))