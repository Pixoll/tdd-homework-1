import random
from src.juego.validador_apuesta import ValidadorApuesta
from src.juego.cacho import Cacho
from src.juego.dado import Dado

class GestorPartidas:
    def __init__(self, jugadores: list[str]) -> None:
        if not jugadores:
            raise ValueError("Debe haber al menos un jugador")

        self.jugadores = jugadores
        self.cachos = [Cacho() for _ in jugadores]
        self.num_dados = sum(cacho.cantidad_dados for cacho in self.cachos)
        self._turno_actual: int | None = None