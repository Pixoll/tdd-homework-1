from enum import StrEnum

from .contador_pintas import ContadorPintas


class ResultadoDuda(StrEnum):
    CALZAR = "calzar"
    GANA = "gana"
    PIERDE = "pierde"


class ArbitroRonda:
    def __init__(self, contador: ContadorPintas) -> None:
        self.contador = contador

    def dudar(self, cantidad_apostada: int, pinta: int) -> ResultadoDuda:
        # Contar la cantidad real sin aplicar límite de comodín (usar_ases=True)
        cantidad_real = sum(1 for valor in self.contador.valores_dados if valor == pinta or valor == 1)

        if cantidad_real == cantidad_apostada:
            return ResultadoDuda.CALZAR  # Exacto
        elif cantidad_real < cantidad_apostada:
            return ResultadoDuda.GANA  # Duda correcta
        else:
            return ResultadoDuda.PIERDE  # Duda incorrecta
