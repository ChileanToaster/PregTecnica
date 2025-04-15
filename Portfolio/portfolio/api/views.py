from rest_framework.response import Response
from rest_framework.decorators import api_view
from datetime import datetime, timedelta

from activos.models import PrecioActivo
from activos.utils import calc_pesos_activos
from portafolios.models import ActivoPortafolio, Portafolio
from portafolios.utils import calc_valor_total

@api_view(['GET'])
def get_peso_and_valor_total(request):
    """
    Endpoint para obtener pesos de activos y valores totales de portafolios entre dos fechas.
    Se espera recibir dos fechas en el formato YYYY-MM-DD como parámetros de consulta.
    """

    fecha_inicio = request.query_params.get('fecha_inicio')
    fecha_fin = request.query_params.get('fecha_fin')

    if not fecha_inicio or not fecha_fin:
        return Response({"error": "Se requieren las fechas de inicio y fin."}, status=400)

    # Asegurarse que las fechas están en el formato correcto
    try:
        fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d').date()
        fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d').date()
    except ValueError:
        return Response({"error": "Formato de fecha inválido. Use YYYY-MM-DD."}, status=400)

    # Asegurarse que la fecha de inicio es anterior o igual a la fecha de fin
    if fecha_inicio > fecha_fin:
        return Response({"error": "La fecha de inicio debe ser anterior a la fecha de fin."}, status=400) 

    # Datos a retornar
    data = {}
    
    lista_fechas = [fecha_inicio + timedelta(days=i) for i in range((fecha_fin - fecha_inicio).days + 1)]

    # Conseguir los precios de los activos entre las fechas
    precios = PrecioActivo.objects.filter(
        fecha__range=[fecha_inicio, fecha_fin]
    ).order_by('fecha')

    for portafolio in Portafolio.objects.all():
        data_portafolio = {
            "datos": []
        }

        # Conseguir los activos del portafolio y sus cantidades como diccionario
        activos_portafolio = ActivoPortafolio.objects.filter(portafolio=portafolio)
        activos_portafolio = activos_portafolio.values('activo__nombre', 'cantidad')
        activos_portafolio = {item['activo__nombre']: float(item['cantidad']) for item in activos_portafolio}

        for fecha in lista_fechas:
            # Conseguir el valor de cada activo en esa fecha y transformarlo en diccionario
            precios_activos = precios.filter(fecha=fecha)
            precios_activos = precios_activos.values('activo__nombre', 'precio')
            precios_activos = {item['activo__nombre']: float(item['precio']) for item in precios_activos}

            valor_total = calc_valor_total(activos_portafolio, precios_activos)

            pesos_activos = calc_pesos_activos(activos_portafolio, precios_activos, float(valor_total))

            # Agregar los pesos y el valor total al json de datos del portafolio
            data_portafolio["datos"].append({
                "fecha": fecha,
                "valor_total": valor_total,
                "pesos": pesos_activos,
            })

        # Agregar los datos del portafolio al json de datos
        data[portafolio.nombre] = data_portafolio

    return Response(data)