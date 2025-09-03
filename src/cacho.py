from collections.abc import Sequence

from .dado import Dado


class Cacho:
    """Representa un conjunto de dados usados en el juego."""

    def __init__(self) -> None:
        """Inicializa el cacho con cinco dados."""
        self._dados = [Dado() for _ in range(5)]

    def tirar_dados(self) -> list[int]:
        """Lanza todos los dados y devuelve sus valores."""
        return [dado.tirar() for dado in self._dados]

    def remover_dado(self) -> None:
        """Elimina un dado del cacho."""
        self._dados.pop()

    def agregar_dado(self, dado: Dado | None = None) -> None:
        """Agrega un dado al cacho (nuevo o dado existente)."""
        self._dados.append(dado or Dado())

    @property
    def cantidad_dados(self) -> int:
        """Número actual de dados en el cacho."""
        return len(self._dados)

    @property
    def valores_dados(self) -> Sequence[int]:
        """Valores de los dados en el cacho."""
        return [dado.valor for dado in self._dados]
