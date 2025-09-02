from random import randint


class Dado:
    _PINTAS: dict[int, str] = {
        1: "As",
        2: "Tonto",
        3: "Tren",
        4: "Cuadra",
        5: "Quina",
        6: "Sexto",
    }

    def __init__(self, valor: int | None = None) -> None:
        self._valor: int | None = valor

    def tirar(self) -> int:
        self._valor = randint(1, 6)
        return self._valor

    @property
    def valor(self) -> int | None:
        return self._valor

    @property
    def pinta(self) -> str | None:
        return self._PINTAS[self._valor] if self._valor is not None else None
