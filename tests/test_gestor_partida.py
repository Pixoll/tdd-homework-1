import pytest
from src.juego.dado import Dado
from src.juego.cacho import Cacho
from src.juego.gestor_partida import GestorPartidas

def test_crear_partida_no_jugadores():
    jugadores = []
    with pytest.raises(ValueError) as exc_info:
        GestorPartidas(jugadores)
    assert str(exc_info.value) == "Debe haber al menos un jugador"

def test_crear_partida():
    jugadores = ["Ana", "Pedro", "Juan"]
    gestor = GestorPartidas(jugadores)
    assert len(gestor.jugadores) == 3
    assert gestor.jugadores == ["Ana", "Pedro", "Juan"]
    assert len(gestor.cachos) == 3
    assert all(isinstance(c, Cacho) for c in gestor.cachos)
    assert gestor.num_dados == 15

def test_crear_partida_varios():
    jugadores = ["Ana", "Pedro", "Juan", "Manolo", "Federico"]
    gestor = GestorPartidas(jugadores)
    assert len(gestor.jugadores) == 5
    assert gestor.jugadores == ["Ana", "Pedro", "Juan", "Manolo", "Federico"]
    assert len(gestor.cachos) == 5
    assert all(isinstance(c, Cacho) for c in gestor.cachos)
    assert gestor.num_dados == 25