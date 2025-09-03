from unittest.mock import MagicMock

import pytest
from pytest_mock import MockerFixture

from src.gestor_partida import GestorPartida, ModoObligo


def test_no_se_puede_crear_con_un_jugador() -> None:
    """Verifica que no se puede iniciar una partida con un solo jugador."""
    with pytest.raises(ValueError):
        GestorPartida(["a"])


def test_jugadores_creados_con_cinco_dados() -> None:
    """Verifica que los jugadores se crean con cinco dados cada uno."""
    jugadores = ["a", "b"]
    partida = GestorPartida(["a", "b"])
    assert partida.jugadores == jugadores
    assert partida.cantidad_dados == 10
    assert all(partida.obtener_cantidad_dados_jugador(j) == 5 for j in jugadores)


def test_juego_sin_jugador_actual_ni_anterior_al_inicio() -> None:
    """Verifica que al iniciar no hay jugador actual ni anterior."""
    partida = GestorPartida(["a", "b", "c"])
    assert partida.nombre_jugador_actual is None
    assert partida.nombre_jugador_anterior is None


def test_juego_no_terminado_al_inicio() -> None:
    """Verifica que el juego no está terminado al inicio y no hay ganador."""
    partida = GestorPartida(["a", "b", "c"])
    assert partida.juego_terminado == False
    assert partida.ganador is None


def test_determinar_inicio_asigna_turno() -> None:
    """Verifica que determinar el jugador inicial asigna correctamente el turno."""
    jugadores = ["a", "b"]
    partida = GestorPartida(jugadores)
    partida.determinar_jugador_inicial()
    assert partida.nombre_jugador_actual in jugadores


def test_establecer_jugador_inicial_existente() -> None:
    """Verifica que se puede establecer un jugador inicial válido."""
    jugadores = ["a", "b"]
    partida = GestorPartida(jugadores)
    partida.establecer_jugador_inicial(jugadores[0])
    assert partida.nombre_jugador_actual == jugadores[0]


def test_establecer_jugador_inicial_inexistente() -> None:
    """Verifica que un jugador inexistente no altera el turno actual."""
    partida = GestorPartida(["a", "b"])
    partida.establecer_jugador_inicial("c")
    assert partida.nombre_jugador_actual is None


def test_remover_dado_de_jugador() -> None:
    """Verifica que se puede remover un dado de un jugador."""
    jugadores = ["a", "b"]
    partida = GestorPartida(jugadores)
    partida.remover_dados_de_jugador(jugadores[0], 1)
    assert partida.obtener_cantidad_dados_jugador(jugadores[0]) == 4


def test_remover_demasiados_dados_de_jugador() -> None:
    """Verifica que remover más dados de los que tiene un jugador lo deja en 0."""
    jugadores = ["a", "b"]
    partida = GestorPartida(jugadores)
    partida.remover_dados_de_jugador(jugadores[0], 100)
    assert partida.obtener_cantidad_dados_jugador(jugadores[0]) == 0


def test_quedar_inactivo_te_elimina_de_lista_de_activos() -> None:
    """Verifica que un jugador sin dados se elimina de la lista de activos."""
    jugadores = ["a", "b", "c"]
    partida = GestorPartida(jugadores)
    partida.remover_dados_de_jugador(jugadores[1], 5)  # b pierde todos los dados
    assert sorted(partida.jugadores_activos) == sorted([jugadores[0], jugadores[2]])


def test_avanzar_turno_salta_jugadores_inactivos() -> None:
    """Verifica que avanzar turno salta jugadores inactivos."""
    jugadores = ["a", "b", "c"]
    partida = GestorPartida(jugadores)
    partida.establecer_jugador_inicial(jugadores[0])
    partida.remover_dados_de_jugador(jugadores[1], 5)  # b pierde todos los dados
    partida.avanzar_turno()
    assert partida.nombre_jugador_actual == jugadores[2]


def test_avanzar_turno_cicla_jugadores_sentido_horario() -> None:
    """Verifica que el turno cicla correctamente en sentido horario."""
    jugadores = ["a", "b", "c"]
    partida = GestorPartida(jugadores)
    partida.establecer_jugador_inicial(jugadores[0])  # a
    partida.avanzar_turno()  # b
    partida.avanzar_turno()  # c
    partida.avanzar_turno()  # a
    assert partida.nombre_jugador_actual == jugadores[0]


def test_avanzar_turno_cicla_jugadores_sentido_antihorario() -> None:
    """Verifica que el turno cicla correctamente en sentido antihorario."""
    jugadores = ["a", "b", "c"]
    partida = GestorPartida(jugadores)
    partida.cambiar_sentido()
    partida.establecer_jugador_inicial(jugadores[0])  # a
    partida.avanzar_turno()  # c
    partida.avanzar_turno()  # b
    partida.avanzar_turno()  # a
    assert partida.nombre_jugador_actual == jugadores[0]


def test_avanzar_turno_actualiza_jugador_anterior() -> None:
    """Verifica que avanzar turno actualiza correctamente al jugador anterior."""
    jugadores = ["a", "b", "c"]
    partida = GestorPartida(jugadores)
    partida.establecer_jugador_inicial(jugadores[0])  # a
    partida.avanzar_turno()  # b
    partida.avanzar_turno()  # c
    assert partida.nombre_jugador_anterior == jugadores[1]


def test_cambiar_sentido() -> None:
    """Verifica que cambiar sentido altera el flujo de turnos."""
    partida = GestorPartida(["a", "b"])
    assert partida.sentido == 1
    partida.cambiar_sentido()
    assert partida.sentido == -1
    partida.cambiar_sentido()
    assert partida.sentido == 1


def test_registrar_apuesta_normal() -> None:
    """Verifica que se puede registrar una apuesta normal."""
    partida = GestorPartida(["a", "b"])
    partida.registrar_apuesta(pinta=3, cantidad=2)
    assert partida.apuesta_actual.pinta == 3
    assert partida.apuesta_actual.cantidad == 2


def test_registrar_apuesta_en_obligo_fija_pinta() -> None:
    """Verifica que registrar apuesta en obligo fija la pinta obligo."""
    jugadores = ["a", "b"]
    partida = GestorPartida(jugadores)
    partida.establecer_jugador_inicial(jugadores[0])
    partida.remover_dados_de_jugador(jugadores[0], 4)
    partida.activar_obligo(abierto=True)
    partida.registrar_apuesta(pinta=4, cantidad=2)
    assert partida.pinta_obligo == 4


def test_resolver_duda_pierde_jugador_actual(mocker: MockerFixture) -> None:
    """Verifica que resolver duda hace perder un dado al jugador actual si pierde."""
    mock_valores_jugador1 = [2, 2, 2, 5, 6]
    mock_valores_jugador2 = [3, 4, 5, 6, 6]
    mock_randint = MagicMock(side_effect=mock_valores_jugador1 + mock_valores_jugador2)
    mocker.patch("src.dado.randint", mock_randint)

    jugadores = ["a", "b"]
    partida = GestorPartida(jugadores)
    partida.establecer_jugador_inicial(jugadores[1])
    partida.iniciar_ronda()
    partida.registrar_apuesta(pinta=2, cantidad=2)
    perdedor = partida.resolver_duda(usar_ases=False)
    assert perdedor == jugadores[1]
    assert partida.obtener_cantidad_dados_jugador(jugadores[1]) == 4


def test_resolver_calzar_correcto_gana_dado(mocker: MockerFixture) -> None:
    """Verifica que resolver calzar correctamente hace ganar un dado al jugador."""
    mock_valores_jugador1 = [3, 3, 3, 4, 5]
    mock_valores_jugador2 = [3, 6, 6, 6, 6]
    mock_randint = MagicMock(side_effect=mock_valores_jugador1 + mock_valores_jugador2)
    mocker.patch("src.dado.randint", mock_randint)

    jugadores = ["a", "b"]
    partida = GestorPartida(jugadores)
    partida.remover_dados_de_jugador(jugadores[0], 1)
    partida.establecer_jugador_inicial(jugadores[0])
    partida.iniciar_ronda()
    partida.registrar_apuesta(pinta=3, cantidad=4)
    ganador = partida.resolver_calzar(usar_ases=False)
    assert ganador == jugadores[0]
    assert partida.obtener_cantidad_dados_jugador(jugadores[0]) == 5


def test_resolver_calzar_incorrecto_pierde_dado(mocker: MockerFixture) -> None:
    """Verifica que resolver calzar incorrectamente hace perder un dado al jugador."""
    mock_valores_jugador1 = [3, 4, 5, 6, 6]
    mock_valores_jugador2 = [4, 5, 6, 6, 6]
    mock_randint = MagicMock(side_effect=mock_valores_jugador1 + mock_valores_jugador2)
    mocker.patch("src.dado.randint", mock_randint)

    jugadores = ["a", "b"]
    partida = GestorPartida(jugadores)
    partida.establecer_jugador_inicial(jugadores[0])
    partida.iniciar_ronda()
    partida.registrar_apuesta(pinta=3, cantidad=2)
    perdedor = partida.resolver_calzar(usar_ases=False)
    assert perdedor == jugadores[0]
    assert partida.obtener_cantidad_dados_jugador(jugadores[0]) == 4


def test_activar_obligo() -> None:
    """Verifica que un jugador puede activar obligo cuando tiene un dado."""
    jugadores = ["a", "b"]
    partida = GestorPartida(jugadores)
    partida.establecer_jugador_inicial(jugadores[0])
    partida.remover_dados_de_jugador(jugadores[0], 4)
    activado = partida.activar_obligo(abierto=True)
    assert activado == True
    assert partida.modo_obligo == ModoObligo.ABIERTO


def test_iniciar_ronda_resetea_obligo() -> None:
    """Verifica que iniciar una ronda resetea el modo obligo."""
    jugadores = ["a", "b"]
    partida = GestorPartida(jugadores)
    partida.establecer_jugador_inicial(jugadores[0])
    partida.remover_dados_de_jugador(jugadores[0], 4)
    partida.activar_obligo(abierto=True)
    partida.iniciar_ronda()
    assert partida.modo_obligo is None


def test_activar_obligo_no_vale_si_ya_usado() -> None:
    """Verifica que un jugador no puede reactivar obligo si ya lo usó."""
    jugadores = ["a", "b"]
    partida = GestorPartida(jugadores)
    partida.establecer_jugador_inicial(jugadores[0])
    partida.remover_dados_de_jugador(jugadores[0], 4)
    partida.activar_obligo(abierto=True)
    partida.iniciar_ronda()
    activado = partida.activar_obligo(abierto=False)
    assert activado == False
    assert partida.modo_obligo is None


def test_ganador_detectado() -> None:
    """Verifica que se detecta correctamente el ganador cuando solo queda un jugador activo."""
    jugadores = ["a", "b"]
    partida = GestorPartida(jugadores)
    partida.remover_dados_de_jugador(jugadores[1], 5)  # b pierde
    assert partida.juego_terminado
    assert partida.ganador == jugadores[0]
