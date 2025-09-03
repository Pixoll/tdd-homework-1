from collections.abc import Sequence
from copy import deepcopy
from dataclasses import dataclass
from enum import StrEnum
from typing import Literal

from .arbitro_ronda import ArbitroRonda
from .cacho import Cacho
from .contador_pintas import ContadorPintas
from .dado import Dado


@dataclass
class Jugador:
    """Representa a un jugador con su cacho y estado de obligo."""

    nombre: str
    cacho: Cacho
    obligo_usado: bool

    @property
    def activo(self) -> bool:
        """Indica si el jugador aún tiene dados en juego."""
        return self.cacho.cantidad_dados > 0

    @property
    def puede_activar_obligo(self) -> bool:
        """Indica si el jugador puede activar obligo en este turno."""
        return self.cacho.cantidad_dados == 1 and not self.obligo_usado


@dataclass
class Apuesta:
    """Representa una apuesta con pinta y cantidad."""

    pinta: int
    cantidad: int


class ModoObligo(StrEnum):
    """Modos de juego cuando se activa obligo."""

    ABIERTO = "abierto"
    CERRADO = "cerrado"


class GestorPartida:
    """Orquesta el flujo de la partida: turnos, apuestas y resolución de jugadas."""

    _jugadores: list[Jugador]
    _turno_actual: int | None
    _sentido: Literal[1, -1]
    """1 = horario, -1 = antihorario"""
    _apuesta_actual: Apuesta | None
    _modo_obligo: ModoObligo | None
    _pinta_obligo: int | None

    def __init__(self, nombres_jugadores: list[str]) -> None:
        """Crea una partida con la lista de jugadores."""
        if len(nombres_jugadores) < 2:
            raise ValueError("Se necesitan al menos 2 jugadores")

        self._jugadores = [
            Jugador(nombre=nombre, cacho=Cacho(), obligo_usado=False)
            for nombre in nombres_jugadores
        ]
        self._turno_actual = None
        self._sentido = 1
        self._apuesta_actual = None
        self._modo_obligo = None
        self._pinta_obligo = None

    @property
    def sentido(self) -> int:
        """Sentido actual de la partida (1 horario, -1 antihorario)."""
        return self._sentido

    @property
    def apuesta_actual(self) -> Apuesta | None:
        """Devuelve la apuesta actual (copia)."""
        return deepcopy(self._apuesta_actual)

    @property
    def modo_obligo(self) -> ModoObligo | None:
        """Modo de obligo activo en la ronda."""
        return self._modo_obligo

    @property
    def pinta_obligo(self) -> int | None:
        """Pinta elegida en obligo, si corresponde."""
        return self._pinta_obligo

    @property
    def jugadores(self) -> Sequence[str]:
        """Nombres de todos los jugadores."""
        return [j.nombre for j in self._jugadores]

    @property
    def nombre_jugador_actual(self) -> str | None:
        """Nombre del jugador que tiene el turno actual."""
        jugador = self._jugador_actual
        return jugador.nombre if jugador is not None else None

    @property
    def nombre_jugador_anterior(self) -> str | None:
        """Nombre del jugador que jugó en el turno anterior."""
        jugador = self._jugador_anterior
        return jugador.nombre if jugador is not None else None

    @property
    def jugadores_activos(self) -> Sequence[str]:
        """Nombres de los jugadores que aún tienen dados en juego."""
        return [j.nombre for j in self._jugadores if j.activo]

    @property
    def cantidad_dados(self) -> int:
        """Cantidad total de dados en juego."""
        return sum(j.cacho.cantidad_dados for j in self._jugadores)

    @property
    def juego_terminado(self) -> bool:
        """Indica si la partida ya tiene un ganador."""
        return sum(j.activo for j in self._jugadores) == 1

    @property
    def ganador(self) -> str | None:
        """Devuelve el nombre del ganador, si ya terminó la partida."""
        if not self.juego_terminado:
            return None

        nombre: str | None = None
        for j in self._jugadores:
            if j.activo:
                nombre = j.nombre
                break
        return nombre

    def cambiar_sentido(self) -> None:
        """Cambia el sentido de juego (horario/antihorario)."""
        self._sentido *= -1

    def registrar_apuesta(self, pinta: int, cantidad: int) -> None:
        """Registra una apuesta y actualiza obligo si aplica."""
        self._apuesta_actual = Apuesta(pinta=pinta, cantidad=cantidad)
        if self._modo_obligo is not None and self._pinta_obligo is None:
            self._pinta_obligo = pinta

    def determinar_jugador_inicial(self) -> None:
        """Determina aleatoriamente quién inicia la partida."""
        dado = Dado()
        candidatos = [j for j in self._jugadores]

        while len(candidatos) > 1:
            tiradas: list[tuple[Jugador, int]] = [(j, dado.tirar()) for j in candidatos]
            max_tirada = max(t[1] for t in tiradas)
            candidatos = [j for j, tirada in tiradas if tirada == max_tirada]

        self._turno_actual = self._jugadores.index(candidatos[0])

    def establecer_jugador_inicial(self, nombre: str) -> None:
        """Establece el jugador inicial por su nombre."""
        datos = self._obtener_jugador_por_nombre(nombre)
        if datos:
            self._turno_actual = datos[1]

    def iniciar_ronda(self) -> None:
        """Lanza los dados de todos los jugadores activos e inicia la ronda."""
        for j in self._jugadores:
            if j.activo:
                j.cacho.tirar_dados()
        self._apuesta_actual = None
        self._modo_obligo = None
        self._pinta_obligo = None

    def avanzar_turno(self) -> None:
        """Avanza al siguiente jugador activo según el sentido de juego."""
        for _ in self._jugadores:
            self._turno_actual += self._sentido
            self._turno_actual %= len(self._jugadores)
            if self._jugadores[self._turno_actual].activo:
                break

    def resolver_duda(self, usar_ases: bool) -> str:
        """Resuelve la acción de dudar y devuelve el nombre del perdedor."""
        pierde_quien_duda = not self._arbitro_ronda.dudar(
            self._apuesta_actual.cantidad,
            self._apuesta_actual.pinta,
            usar_ases and self._modo_obligo is None,
        )

        perdedor = self._jugador_actual if pierde_quien_duda else self._jugador_anterior
        perdedor.cacho.remover_dado()

        return perdedor.nombre

    def resolver_calzar(self, usar_ases: bool) -> str:
        """Resuelve la acción de calzar y devuelve el nombre del jugador afectado."""
        jugador = self._jugador_actual
        logro_calzar = self._arbitro_ronda.calzar(
            self._apuesta_actual.cantidad,
            self._apuesta_actual.pinta,
            usar_ases and self._modo_obligo is None,
        )

        if logro_calzar:
            if jugador.cacho.cantidad_dados < 5:
                jugador.cacho.agregar_dado()
        else:
            jugador.cacho.remover_dado()

        return jugador.nombre

    def activar_obligo(self, abierto: bool) -> bool:
        """Activa obligo si el jugador actual puede hacerlo."""
        jugador = self._jugador_actual
        if not jugador.puede_activar_obligo:
            return False

        jugador.obligo_usado = True
        self._modo_obligo = ModoObligo.ABIERTO if abierto else ModoObligo.CERRADO
        self._pinta_obligo = None
        return True

    def remover_dados_de_jugador(self, nombre: str, cantidad: int) -> None:
        """Remueve dados de un jugador específico."""
        datos = self._obtener_jugador_por_nombre(nombre)
        if datos:
            jugador = datos[0]
            while jugador.activo and cantidad > 0:
                jugador.cacho.remover_dado()
                cantidad -= 1

    def obtener_cantidad_dados_jugador(self, nombre: str) -> int | None:
        """Devuelve la cantidad de dados de un jugador por su nombre."""
        datos = self._obtener_jugador_por_nombre(nombre)
        return datos[0].cacho.cantidad_dados if datos is not None else None

    @property
    def _jugador_actual(self) -> Jugador | None:
        """Jugador que tiene el turno actual (o None si no hay)."""
        return self._jugadores[self._turno_actual] if self._turno_actual is not None else None

    @property
    def _jugador_anterior(self) -> Jugador | None:
        """Jugador que jugó antes del actual (o None si no hay)."""
        if self._turno_actual is None:
            return None

        index = self._turno_actual
        resultado: Jugador | None = None
        for _ in self._jugadores:
            index -= self._sentido
            index %= len(self._jugadores)
            jugador = self._jugadores[index]
            if jugador.activo:
                resultado = jugador
                break

        return resultado

    @property
    def _arbitro_ronda(self) -> ArbitroRonda:
        """Crea un árbitro de ronda con los cachos activos."""
        contador = ContadorPintas([j.cacho for j in self._jugadores if j.activo])
        return ArbitroRonda(contador)

    def _obtener_jugador_por_nombre(self, jugador: str) -> tuple[Jugador, int] | None:
        """Busca un jugador por nombre y devuelve la tupla (jugador, índice)."""
        for i, j in enumerate(self._jugadores):
            if j.nombre == jugador:
                return j, i
        return None
