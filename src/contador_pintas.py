from collections.abc import Sequence

from .cacho import Cacho


class ContadorPintas:
    """Cuenta las pintas de los dados en varios cachos."""

    def __init__(self, cachos: list[Cacho]):
        """Inicializa el contador con una lista de cachos."""
        self._cachos = cachos

    @property
    def valores_dados(self) -> Sequence[int]:
        """Devuelve los valores de todos los dados en juego."""
        valores: list[int] = []
        for c in self._cachos:
            for v in c.valores_dados:
                valores.append(v)
        return valores

    def contar_pinta(self, pinta: int, usar_ases: bool = True) -> int:
        """Cuenta cuántas veces aparece una pinta, opcionalmente usando ases como comodines."""
        if usar_ases and pinta != 1:
            return sum(1 for v in self.valores_dados if v == pinta or v == 1)
        else:
            return sum(1 for v in self.valores_dados if v == pinta)
