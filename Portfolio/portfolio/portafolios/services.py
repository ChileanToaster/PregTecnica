from portafolios.models import Portafolio, ActivoPortafolio
from activos.models import Activo

def portfolio_create(nombre: str) -> Portafolio:
    """
    Crea un nuevo portafolio con el nombre dado, si ya existe arroja error.
    """

    portafolio = Portafolio(nombre=nombre)
    portafolio.full_clean()
    portafolio.save()

    return portafolio

def portafolio_get(nombre: str) -> Portafolio:
    """
    Obtiene un portafolio por su nombre, si no existe arroja error.
    """
    try:
        portafolio = Portafolio.objects.get(nombre=nombre)
    except Portafolio.DoesNotExist:
        raise ValueError(f'El portafolio {nombre} no existe.')

    return portafolio

def portafolio_get_or_create(nombre: str) -> Portafolio:
    """
    Obtiene un portafolio por su nombre, si no existe lo crea.
    """
    try:
        portafolio = Portafolio.objects.get(nombre=nombre)
    except Portafolio.DoesNotExist:
        portafolio = portfolio_create(nombre)

    return portafolio

def activo_portafolio_create(portafolio: Portafolio, activo: Activo, cantidad: float) -> ActivoPortafolio:
    """
    Crea un nuevo activo en el portafolio con la cantidad dada, si ya existe arroja error.
    """
    activo_portafolio = ActivoPortafolio(portafolio=portafolio, activo=activo, cantidad=cantidad)
    activo_portafolio.full_clean()
    activo_portafolio.save()

    return activo_portafolio

def activo_portafolio_get(portafolio: Portafolio, activo: Activo) -> ActivoPortafolio:
    """
    Obtiene un activo del portafolio por su nombre, si no existe arroja error.
    """
    try:
        activo_portafolio = ActivoPortafolio.objects.get(portafolio=portafolio, activo=activo)
    except ActivoPortafolio.DoesNotExist:
        raise ValueError(f'El activo {activo.nombre} no existe en el portafolio {portafolio.nombre}.')

    return activo_portafolio

def activo_portafolio_get_or_create(portafolio: Portafolio, activo: Activo, cantidad: float) -> ActivoPortafolio:
    """
    Obtiene un activo del portafolio por su nombre, si no existe lo crea.
    """
    try:
        activo_portafolio = ActivoPortafolio.objects.get(portafolio=portafolio, activo=activo)
    except ActivoPortafolio.DoesNotExist:
        activo_portafolio = activo_portafolio_create(portafolio, activo, cantidad)

    return activo_portafolio