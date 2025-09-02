from src.juego.contador_pintas import ContadorPintas

class ArbitroRonda:
    def __init__(self, contador: ContadorPintas) -> None:
        self.contador = contador

    def dudar(self, cantidad_apostada: int, pinta: int) -> str:
        # Contar la cantidad real sin aplicar límite de comodín (usar_ases=True)
        cantidad_real = sum(1 for d in self.contador.dados if d.valor == pinta or d.valor == 1)

        if cantidad_real == cantidad_apostada:
            return "calzar"  # Exacto
        elif cantidad_real < cantidad_apostada:
            return "jugador_gana"  # Duda correcta
        else:
            return "jugador_pierde"  # Duda incorrecta
