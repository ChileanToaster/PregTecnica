from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['GET'])
def get_peso_and_valor_total(request):
    """
    Endpoint para obtener pesos de activos y valores totales de portafolios entre dos fechas.
    Se espera recibir dos fechas en el formato YYYY-MM-DD como parámetros de consulta.
    """
    # Datos de ejemplo
    data = {
        "pesos": {
            "activo_a": 0.5,
            "activo_b": 0.3,
            "activo_c": 0.2
        },
        "valores_totales": {
            "portafolio_!": 10000,
            "portafolio_2": 20000,
        }
    }
    
    return Response(data)