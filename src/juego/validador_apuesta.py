import math


class ValidadorApuesta:
    def __init__(self, pinta: int, cantidad: int) -> None:
        self.pinta = pinta
        self.cantidad = cantidad

    @staticmethod
    def verificar_rango_pinta(pinta: int) -> bool:
        return 1 <= pinta <= 6

    @staticmethod
    def verificar_rango_cantidad(cantidad: int) -> bool:
        return cantidad >= 1

    @staticmethod
    def cambio_to_ases(pinta_actual, cantidad_actual: int, pinta_nueva: int) -> tuple[int, bool]:
        if pinta_nueva != 1:
            return cantidad_actual, False

        if cantidad_actual % 2 == 0:
            cantidad_nueva = (cantidad_actual // 2) + 1
        else:
            cantidad_nueva = math.ceil(cantidad_actual / 2)
        return cantidad_nueva, True

    @staticmethod
    def cambio_de_ashes(pinta_actual: int, cantidad_actual: int, pinta_nueva) -> tuple[int, bool]:
        if pinta_actual != 1:
            return cantidad_actual, False

        cantidad_nueva = (cantidad_actual * 2) + 1
        return cantidad_nueva, True

    @staticmethod
    def validar_apuesta(pinta: int, cantidad: int) -> bool:
        # Reglas de rango
        if not ValidadorApuesta.verificar_rango_pinta(pinta) or not ValidadorApuesta.verificar_rango_cantidad(cantidad):
            return False

        # No se puede partir con más de un As
        return pinta != 1 or cantidad <= 1

    @staticmethod
    def validar_aumento_apuesta(pinta_actual: int, cantidad_actual: int, pinta_nueva: int, cantidad_nueva: int) -> bool:
        # Si es la misma pinta
        if pinta_actual == pinta_nueva:
            # Si es igual o mayor -> válido
            # Si la cantidad nueva es menor -> inválido
            return cantidad_nueva >= cantidad_actual
        else:
            # Si la pinta es mayor -> válido
            # Si la pinta es menor -> inválido
            return pinta_nueva > pinta_actual
