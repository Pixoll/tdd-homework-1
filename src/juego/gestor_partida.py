import random
from src.juego.cacho import Cacho

class GestorPartidas:
    def __init__(self, jugadores: list[str]) -> None:
        if not jugadores:
            raise ValueError("Debe haber al menos un jugador")

        self.jugadores = jugadores
        self.cachos = [Cacho() for _ in jugadores]
        self._turno_actual: int | None = None
    
    @property
    def num_dados(self) -> int:
        return sum(cacho.cantidad_dados for cacho in self.cachos)

    def determinar_inicial(self) -> str:
        jugador = random.choice(self.jugadores)
        self._turno_actual = self.jugadores.index(jugador)
        return jugador

    def get_siguiente(self) -> str:
        if self._turno_actual is None:
            raise RuntimeError("Debes llamar primero a determinar_inicial()")
        self._turno_actual = (self._turno_actual + 1) % len(self.jugadores)
        return self.jugadores[self._turno_actual]

    def jugadores_con_un_dado(self) -> list[str]:
        return [
            nombre
            for nombre, cacho in zip(self.jugadores, self.cachos)
            if cacho.cantidad_dados == 1
        ]