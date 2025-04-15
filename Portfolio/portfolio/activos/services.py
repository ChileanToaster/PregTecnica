from activos.models import Activo, PrecioActivo

def activo_create(nombre: str) -> Activo:
    """
    Crea un nuevo activo con el nombre dado, si ya existe arroja error.
    """
    activo = Activo(nombre=nombre)
    activo.full_clean()
    activo.save()

    return activo

def activo_get(nombre: str) -> Activo:
    """
    Obtiene un activo por su nombre, si no existe arroja error.
    """
    try:
        activo = Activo.objects.get(nombre=nombre)
    except Activo.DoesNotExist:
        raise ValueError(f'El activo {nombre} no existe.')

    return activo

def activo_get_or_create(nombre: str) -> Activo:
    """
    Obtiene un activo por su nombre, si no existe lo crea.
    """
    try:
        activo = Activo.objects.get(nombre=nombre)
    except Activo.DoesNotExist:
        activo = activo_create(nombre)

    return activo

def precio_activo_create(activo: Activo, fecha: str, precio: float) -> PrecioActivo:
    """
    Crea un nuevo registro del precio para el activo en la fecha dada, si ya existe arroja error.
    """
    precio_activo = PrecioActivo(activo=activo, fecha=fecha, precio=precio)
    precio_activo.full_clean()
    precio_activo.save()

    return precio_activo

def precio_activo_get(activo: Activo, fecha: str) -> PrecioActivo:
    """
    Obtiene el precio de un activo en una fecha dada, si no existe arroja error.
    """
    try:
        precio_activo = PrecioActivo.objects.get(activo=activo, fecha=fecha)
    except PrecioActivo.DoesNotExist:
        raise ValueError(f'El precio del activo {activo.nombre} en la fecha {fecha} no existe.')

    return precio_activo

def precio_activo_get_or_create(activo: Activo, fecha: str, precio: float) -> PrecioActivo:
    """
    Obtiene el precio de un activo en una fecha dada, si no existe lo crea.
    """
    try:
        precio_activo = PrecioActivo.objects.get(activo=activo, fecha=fecha)
    except PrecioActivo.DoesNotExist:
        precio_activo = precio_activo_create(activo, fecha, precio)

    return precio_activo