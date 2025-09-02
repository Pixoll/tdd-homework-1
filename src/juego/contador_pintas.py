from collections.abc import Sequence

from juego.cacho import Cacho


class ContadorPintas:
    def __init__(self, cacho: Cacho):
        self._cacho = cacho

    @property
    def valores_dados(self) -> Sequence[int]:
        return self._cacho.valores_dados

    def contar_pinta(self, pinta: int, usar_ases: bool = True) -> int:
        cantidad = sum(1 for valor in self._cacho.valores_dados if valor == pinta)
        if usar_ases and pinta != 1:
            ases = sum(1 for valor in self._cacho.valores_dados if valor == 1)
            if cantidad == 0:
                # Pinta ausente: máximo 2 ases como comodín
                cantidad += min(ases, 2)
            else:
                # Pinta presente:
                # regla: solo un as se usa si la pinta tiene un único dado
                # y todos los ases si la pinta aparece más de una vez
                if cantidad == 1:
                    cantidad += 1  # solo un as
                else:
                    cantidad += ases  # todos los ases
        return cantidad
