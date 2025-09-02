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
    def cambio_a_ases(cantidad_actual: int) -> int:
        return (cantidad_actual // 2) + 1 if cantidad_actual % 2 == 0 else math.ceil(cantidad_actual / 2)

    @staticmethod
    def cambio_desde_ases(cantidad_actual: int) -> int:
        return (cantidad_actual * 2) + 1

    @staticmethod
    def validar_apuesta_general(pinta: int, cantidad: int) -> bool:
        return ValidadorApuesta.verificar_rango_pinta(pinta) and ValidadorApuesta.verificar_rango_cantidad(cantidad)

    @staticmethod
    def validar_primera_apuesta(pinta: int, cantidad: int, jugador_tiene_un_dado: bool) -> bool:
        if pinta == 1 and not jugador_tiene_un_dado:
            return False
        return ValidadorApuesta.validar_apuesta_general(pinta, cantidad)

    @staticmethod
    def validar_aumento_apuesta(pinta_actual: int, cantidad_actual: int, pinta_nueva: int, cantidad_nueva: int) -> bool:
        # cambios especiales
        if pinta_nueva == 1 and pinta_actual != 1:
            return cantidad_nueva >= ValidadorApuesta.cambio_a_ases(cantidad_actual)

        if pinta_actual == 1 and pinta_nueva != 1:
            return cantidad_nueva >= ValidadorApuesta.cambio_desde_ases(cantidad_actual)

        return cantidad_nueva > cantidad_actual or (cantidad_nueva == cantidad_actual and pinta_nueva > pinta_actual)
