from collections.abc import Sequence

from .dado import Dado


class Cacho:
    def __init__(self, dados: list[Dado] | None = None) -> None:
        self._dados = dados or [Dado() for _ in range(5)]

    def tirar_dados(self) -> list[int]:
        return [dado.tirar() for dado in self._dados]

    def remover_dado(self) -> None:
        self._dados.pop()

    def agregar_dado(self, dado: Dado | None = None) -> None:
        self._dados.append(dado or Dado())

    @property
    def cantidad_dados(self) -> int:
        return len(self._dados)

    @property
    def valores_dados(self) -> Sequence[int]:
        return [dado.valor for dado in self._dados]
