from random import randint

class Dado:
    def __init__(self, valor: int | None = None) -> None:
        self._valor: int | None = valor

    def tirar(self) -> int:
        if self._valor is None:
            self._valor = randint(1, 6)
        return self._valor

    @property
    def valor(self) -> int | None:
        return self._valor
