from math import ceil

from .contador_pintas import ContadorPintas


class ArbitroRonda:
    """Arbitra una ronda del juego, validando apuestas y resultados."""

    def __init__(self, contador: ContadorPintas) -> None:
        """Inicializa el árbitro con un contador de pintas."""
        self.contador = contador

    @property
    def total_dados_en_juego(self) -> int:
        """Devuelve el número total de dados en juego."""
        return len(self.contador.valores_dados)

    def dudar(self, cantidad_apostada: int, pinta: int, usar_ases: bool) -> bool:
        """Determina si se puede dudar de una apuesta."""
        cantidad_real = self.contador.contar_pinta(pinta, usar_ases)
        return cantidad_real < cantidad_apostada

    def puede_calzar(self, cantidad_apostada: int, dados_jugador: int) -> bool:
        """Verifica si un jugador está autorizado a calzar la apuesta."""
        return dados_jugador == 1 or cantidad_apostada >= ceil(self.total_dados_en_juego / 2)

    def calzar(self, cantidad_apostada: int, pinta: int, usar_ases: bool) -> bool:
        """Comprueba si la apuesta calzada coincide exactamente con la realidad."""
        cantidad_real = self.contador.contar_pinta(pinta, usar_ases)
        return cantidad_real == cantidad_apostada
