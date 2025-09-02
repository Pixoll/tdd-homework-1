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

def test_determinar_quien_inicia():
    jugadores = ["Ana", "Pedro", "Juan"]
    gestor = GestorPartidas(jugadores)
    iniciador = gestor.determinar_inicial()
    assert iniciador in jugadores
    assert gestor.jugadores[gestor._turno_actual] == iniciador

def test_asigar_correcto_flujo_turnos():
    jugadores = ["Ana", "Pedro", "Juan"]
    gestor = GestorPartidas(jugadores)
    actual = gestor.determinar_inicial()
    siguiente = gestor.get_siguiente()
    assert siguiente != actual
    assert siguiente in jugadores

def test_asigar_incorrecto_flujo_turnos():
    jugadores = ["Ana", "Pedro", "Juan"]
    gestor = GestorPartidas(jugadores)
    with pytest.raises(RuntimeError) as exc_info:
        actual = gestor.get_siguiente()
    assert str(exc_info.value) == "Debes llamar primero a determinar_inicial()"

def test_manejar_flujo_turnos_es_circular():
    jugadores = ["Ana", "Pedro"]
    gestor = GestorPartidas(jugadores)
    actual = gestor.determinar_inicial()
    siguiente = gestor.get_siguiente()
    siguiente2 = gestor.get_siguiente()
    assert siguiente2 == actual

def test_manejar_flujo_turnos_es_circular_varios():
    jugadores = ["Ana", "Pedro", "Juan"]
    gestor = GestorPartidas(jugadores)
    actual = gestor.determinar_inicial()
    siguiente = gestor.get_siguiente()
    siguiente2 = gestor.get_siguiente()
    assert actual!=siguiente
    assert siguiente!=siguiente2
    assert siguiente2!=actual

def test_jugador_queda_un_solo_dado():
    jugadores = ["Ana", "Pedro", "Juan"]
    gestor = GestorPartidas(jugadores)
    gestor.cachos[0]._dados = gestor.cachos[0]._dados[:1]
    jugadores_un_dado = gestor.jugadores_con_un_dado()
    assert len(jugadores_un_dado) == 1
    assert jugadores_un_dado[0] == "Ana"

def test_si_nadie_tiene_un_dado_lista_vacia():
    jugadores = ["Ana", "Pedro", "Juan"]
    gestor = GestorPartidas(jugadores)
    jugadores_un_dado = gestor.jugadores_con_un_dado()
    assert jugadores_un_dado == []