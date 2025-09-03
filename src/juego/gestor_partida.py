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
    nombre: str
    cacho: Cacho
    obligo_usado: bool

    @property
    def activo(self) -> bool:
        return self.cacho.cantidad_dados > 0

    @property
    def puede_activar_obligo(self) -> bool:
        return self.cacho.cantidad_dados == 1 and not self.obligo_usado


@dataclass
class Apuesta:
    pinta: int
    cantidad: int


class ModoObligo(StrEnum):
    ABIERTO = "abierto"
    CERRADO = "cerrado"


class GestorPartida:
    _jugadores: list[Jugador]
    _turno_actual: int | None
    _sentido: Literal[1, -1]
    """1 = horario, -1 = antihorario"""
    _apuesta_actual: Apuesta | None
    _modo_obligo: ModoObligo | None
    _pinta_obligo: int | None

    def __init__(self, nombres_jugadores: list[str]) -> None:
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
        return self._sentido

    @property
    def apuesta_actual(self) -> Apuesta | None:
        return deepcopy(self._apuesta_actual)

    @property
    def modo_obligo(self) -> ModoObligo | None:
        return self._modo_obligo

    @property
    def pinta_obligo(self) -> int | None:
        return self._pinta_obligo

    @property
    def jugadores(self) -> Sequence[str]:
        return [j.nombre for j in self._jugadores]

    @property
    def nombre_jugador_actual(self) -> str | None:
        jugador = self._jugador_actual
        return jugador.nombre if jugador is not None else None

    @property
    def nombre_jugador_anterior(self) -> str | None:
        jugador = self._jugador_anterior
        return jugador.nombre if jugador is not None else None

    @property
    def jugadores_activos(self) -> Sequence[str]:
        return [j.nombre for j in self._jugadores if j.activo]

    @property
    def cantidad_dados(self) -> int:
        return sum(j.cacho.cantidad_dados for j in self._jugadores)

    @property
    def juego_terminado(self) -> bool:
        return sum(j.activo for j in self._jugadores) == 1

    @property
    def ganador(self) -> str | None:
        if not self.juego_terminado:
            return None

        nombre: str | None = None
        for j in self._jugadores:
            if j.activo:
                nombre = j.nombre
                break
        return nombre

    def cambiar_sentido(self) -> None:
        self._sentido *= -1

    def registrar_apuesta(self, pinta: int, cantidad: int) -> None:
        self._apuesta_actual = Apuesta(pinta=pinta, cantidad=cantidad)
        if self._modo_obligo is not None and self._pinta_obligo is None:
            self._pinta_obligo = pinta

    def determinar_jugador_inicial(self) -> None:
        dado = Dado()
        candidatos = [j for j in self._jugadores]

        while len(candidatos) > 1:
            tiradas: list[tuple[Jugador, int]] = [(j, dado.tirar()) for j in candidatos]
            max_tirada = max(t[1] for t in tiradas)
            candidatos = [j for j, tirada in tiradas if tirada == max_tirada]

        self._turno_actual = self._jugadores.index(candidatos[0])

    def establecer_jugador_inicial(self, nombre: str) -> None:
        datos = self._obtener_jugador_por_nombre(nombre)
        if datos:
            self._turno_actual = datos[1]

    def iniciar_ronda(self) -> None:
        for j in self._jugadores:
            if j.activo:
                j.cacho.tirar_dados()
        self._apuesta_actual = None
        self._modo_obligo = None
        self._pinta_obligo = None

    def avanzar_turno(self) -> None:
        for _ in self._jugadores:
            self._turno_actual += self._sentido
            self._turno_actual %= len(self._jugadores)
            if self._jugadores[self._turno_actual].activo:
                break

    def resolver_duda(self, usar_ases: bool) -> str:
        pierde_quien_duda = not self._arbitro_ronda.dudar(
            self._apuesta_actual.cantidad,
            self._apuesta_actual.pinta,
            usar_ases and self._modo_obligo is None,
        )

        perdedor = self._jugador_actual if pierde_quien_duda else self._jugador_anterior
        perdedor.cacho.remover_dado()

        return perdedor.nombre

    def resolver_calzar(self, usar_ases: bool) -> str:
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
        jugador = self._jugador_actual
        if not jugador.puede_activar_obligo:
            return False

        jugador.obligo_usado = True
        self._modo_obligo = ModoObligo.ABIERTO if abierto else ModoObligo.CERRADO
        self._pinta_obligo = None
        return True

    def remover_dados_de_jugador(self, nombre: str, cantidad: int) -> None:
        datos = self._obtener_jugador_por_nombre(nombre)
        if datos:
            jugador = datos[0]
            while jugador.activo and cantidad > 0:
                jugador.cacho.remover_dado()
                cantidad -= 1

    def obtener_cantidad_dados_jugador(self, nombre: str) -> int | None:
        datos = self._obtener_jugador_por_nombre(nombre)
        return datos[0].cacho.cantidad_dados if datos is not None else None

    @property
    def _jugador_actual(self) -> Jugador | None:
        return self._jugadores[self._turno_actual] if self._turno_actual is not None else None

    @property
    def _jugador_anterior(self) -> Jugador | None:
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
        contador = ContadorPintas([j.cacho for j in self._jugadores if j.activo])
        return ArbitroRonda(contador)

    def _obtener_jugador_por_nombre(self, jugador: str) -> tuple[Jugador, int] | None:
        for i, j in enumerate(self._jugadores):
            if j.nombre == jugador:
                return j, i
        return None
