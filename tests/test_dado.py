from src.juego.dado import Dado


def test_tirar_dado() -> None:
    dado = Dado()
    valor = dado.tirar()
    assert 1 <= valor <= 6
    assert 1 <= dado.valor <= 6
    assert valor == dado.valor


def test_tirar_dado_pinta() -> None:
    dado = Dado(1)
    assert dado.pinta == "As"
    dado = Dado(2)
    assert dado.pinta == "Tonto"
    dado = Dado(3)
    assert dado.pinta == "Tren"
    dado = Dado(4)
    assert dado.pinta == "Cuadra"
    dado = Dado(5)
    assert dado.pinta == "Quina"
    dado = Dado(6)
    assert dado.pinta == "Sexto"
