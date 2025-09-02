class ContadorPintas:
    def __init__(self, dados):
        self.dados = dados

    def contar_pinta(self, pinta: int, usar_ases: bool = True) -> int:
        cantidad = sum(1 for d in self.dados if d.valor == pinta)
        if usar_ases and pinta != 1:
            ases = sum(1 for d in self.dados if d.valor == 1)
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
