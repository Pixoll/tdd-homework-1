# TDD Homework 1

## Project structure

```
src/
├── dado.py
├── cacho.py
├── validador_apuesta.py
├── contador_pintas.py
├── arbitro_ronda.py
└── gestor_partida.py
tests/
├── test_dado.py
├── test_cacho.py
├── test_validador_apuesta.py
├── test_contador_pintas.py
├── test_arbitro_ronda.py
└── test_gestor_partida.py
```

## Install (Linux)

```shell
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Install (Windows)

```shell
python -m venv .venv
call .venv/bin/activate.bat
pip install -r requirements.txt
```

## Execute (Linux)

```shell
source .venv/bin/activate
python3 -m pytest --cov=src --cov-report=term-missing
```

## Execute (Windows)

```shell
call .venv/bin/activate.bat
python -m pytest --cov=src --cov-report=term-missing
```
