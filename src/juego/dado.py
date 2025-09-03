from random import randint


class Dado:
    """Representa un dado de seis caras con nombres para cada pinta."""

    _PINTAS: dict[int, str] = {
        1: "As",
        2: "Tonto",
        3: "Tren",
        4: "Cuadra",
        5: "Quina",
        6: "Sexto",
    }

    _valor: int | None

    def __init__(self) -> None:
        """Inicializa el dado sin valor asignado."""
        self._valor = None

    def tirar(self) -> int:
        """Lanza el dado y devuelve el valor obtenido."""
        self._valor = randint(1, 6)
        return self._valor

    @property
    def valor(self) -> int | None:
        """Valor numérico actual del dado (o None si no se ha lanzado)."""
        return self._valor

    @property
    def pinta(self) -> str | None:
        """Nombre de la pinta según el valor actual (o None si no se ha lanzado)."""
        return self._PINTAS[self._valor] if self._valor is not None else None
