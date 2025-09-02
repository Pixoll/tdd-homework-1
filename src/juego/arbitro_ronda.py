from math import ceil

from .contador_pintas import ContadorPintas


class ArbitroRonda:
    def __init__(self, contador: ContadorPintas) -> None:
        self.contador = contador

    @property
    def total_dados_en_juego(self) -> int:
        return len(self.contador.valores_dados)

    def dudar(self, cantidad_apostada: int, pinta: int, usar_ases: bool) -> bool:
        cantidad_real = self.contador.contar_pinta(pinta, usar_ases)
        return cantidad_real < cantidad_apostada

    def puede_calzar(self, cantidad_apostada: int, dados_jugador: int) -> bool:
        return dados_jugador == 1 or cantidad_apostada >= ceil(self.total_dados_en_juego / 2)

    def calzar(self, cantidad_apostada: int, pinta: int, usar_ases: bool) -> bool:
        cantidad_real = self.contador.contar_pinta(pinta, usar_ases)
        return cantidad_real == cantidad_apostada
