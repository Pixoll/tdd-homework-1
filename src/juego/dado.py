from random import randint


class Dado:
    def __init__(self) -> None:
        self._valor: int | None = None

    def tirar(self) -> int:
        value = randint(1, 6)
        self._valor = value
        return value

    @property
    def valor(self) -> int | None:
        return self._valor
