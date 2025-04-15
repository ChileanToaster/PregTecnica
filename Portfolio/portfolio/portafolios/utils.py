# Funciones utilitarias para los portafolios

from decimal import Decimal, ROUND_HALF_DOWN

def calc_valor_total(cantidades : dict, precios : dict) -> float:
    """
    Calcula el valor total de un portafolio dadas las cantidades de activos y sus precios.
    
    Args:
        cantidades (dict): Diccionario con los activos y sus cantidades.
        precios (dict): Diccionario con los activos y sus precios.
        
    Returns:
        float: Valor total del portafolio entre las fechas dadas.
    """
    valor_total = 0.0
    for activo, cantidad in cantidades.items():
        if activo in precios:
            valor_total += cantidad * precios[activo]
    return Decimal(valor_total).quantize(Decimal('1'), rounding=ROUND_HALF_DOWN)