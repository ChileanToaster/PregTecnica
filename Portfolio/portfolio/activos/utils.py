# Funciones utilitarias para activos

from decimal import Decimal, ROUND_HALF_DOWN

def calc_pesos_activos(cantidades : dict, precios : dict, valor_total : float) -> dict:
    """
    Calcula los pesos de los activos en un portafolio dadas las cantidades y precios de los activos, junto con el valor total del portafolio.
    
    Args:
        cantidades (dict): Diccionario con los activos y sus cantidades.
        precios (dict): Diccionario con los activos y sus precios.
        valor_total (float): Valor total del portafolio.
        
    Returns:
        dict: Pesos de cada activo en el portafolio.
    """
    pesos = {}
    
    # Si el valor total es cero o negativo, no hay nada que calcular
    if valor_total <= 0:
        return pesos

    for activo, cantidad in cantidades.items():
        if activo in precios:
            pesos[activo] = Decimal((precios[activo] * cantidad) / valor_total).quantize(Decimal('0.0001'), rounding=ROUND_HALF_DOWN)
    
    return pesos