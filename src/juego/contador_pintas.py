from collections.abc import Sequence

from .cacho import Cacho


class ContadorPintas:
    def __init__(self, cachos: list[Cacho]):
        self._cachos = cachos

    @property
    def valores_dados(self) -> Sequence[int]:
        valores: list[int] = []
        for c in self._cachos:
            for v in c.valores_dados:
                valores.append(v)
        return valores

    def contar_pinta(self, pinta: int, usar_ases: bool = True) -> int:
        if usar_ases and pinta != 1:
            return sum(1 for v in self.valores_dados if v == pinta or v == 1)
        else:
            return sum(1 for v in self.valores_dados if v == pinta)
