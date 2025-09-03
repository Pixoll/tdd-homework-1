from unittest.mock import MagicMock
from pytest_mock import MockerFixture

from src.gestor_partida import GestorPartida


def test_juego_completo(mocker: MockerFixture) -> None:
    """Simula una ronda completa entre dos jugadores paso a paso hasta un ganador."""

    jugadores = ["a", "b"]
    valores_jugador1 = [2, 2, 3, 4, 5]  # jugador a
    valores_jugador2 = [3, 3, 4, 5, 6]  # jugador b

    mock_randint = MagicMock(side_effect=valores_jugador1 + valores_jugador2)
    mocker.patch("src.dado.randint", mock_randint)

    partida = GestorPartida(jugadores)
    partida.establecer_jugador_inicial(jugadores[0])
    partida.iniciar_ronda()

    # turno 1: a
    partida.registrar_apuesta(pinta=2, cantidad=2)
    assert partida.apuesta_actual.pinta == 2
    assert partida.apuesta_actual.cantidad == 2

    # turno 2: b
    perdedor = partida.resolver_duda(usar_ases=True)
    assert perdedor == "a"
    assert partida.obtener_cantidad_dados_jugador("a") == 4

    # turno 3: a
    partida.avanzar_turno()
    partida.registrar_apuesta(pinta=3, cantidad=2)
    assert partida.apuesta_actual.pinta == 3
    assert partida.apuesta_actual.cantidad == 2

    # turno 4: b
    partida.avanzar_turno()
    ganador_calzar = partida.resolver_calzar(usar_ases=True)
    assert ganador_calzar == "a"
    assert partida.obtener_cantidad_dados_jugador("a") == 3

    # turno 5: a
    partida.avanzar_turno()
    partida.registrar_apuesta(pinta=4, cantidad=2)

    # turno 6: b
    partida.avanzar_turno()
    perdedor = partida.resolver_duda(usar_ases=True)
    assert perdedor == "b"
    assert partida.obtener_cantidad_dados_jugador("b") == 4

    # turno 7: a
    partida.avanzar_turno()
    partida.registrar_apuesta(pinta=5, cantidad=2)

    # turno 8: b
    partida.avanzar_turno()
    ganador_calzar = partida.resolver_calzar(usar_ases=True)
    assert ganador_calzar == "a"
    assert partida.obtener_cantidad_dados_jugador("a") == 2

    # turno 9: a
    partida.avanzar_turno()
    partida.registrar_apuesta(pinta=6, cantidad=2)

    # turno 10: b
    partida.avanzar_turno()
    perdedor = partida.resolver_duda(usar_ases=True)
    assert perdedor == "b"
    assert partida.obtener_cantidad_dados_jugador("b") == 3

    # turno 11: a
    partida.avanzar_turno()
    partida.registrar_apuesta(pinta=3, cantidad=3)

    # turno 12: b
    partida.avanzar_turno()
    perdedor = partida.resolver_duda(usar_ases=True)
    assert perdedor == "b"
    assert partida.obtener_cantidad_dados_jugador("b") == 2

    # turno 13: a
    partida.avanzar_turno()
    partida.registrar_apuesta(pinta=2, cantidad=3)

    # turno 14: b
    partida.avanzar_turno()
    perdedor = partida.resolver_duda(usar_ases=True)
    assert perdedor == "b"
    assert partida.obtener_cantidad_dados_jugador("b") == 1

    # turno 15: a
    partida.avanzar_turno()
    partida.registrar_apuesta(pinta=4, cantidad=3)

    # turno 16: b
    partida.avanzar_turno()
    perdedor = partida.resolver_duda(usar_ases=True)
    assert perdedor == "b"
    assert partida.obtener_cantidad_dados_jugador("b") == 0

    assert partida.juego_terminado
    assert partida.ganador == "a"
