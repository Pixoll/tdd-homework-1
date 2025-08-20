from random import randint


class Dado:
    @staticmethod
    def tirar() -> int:
        return randint(1, 6)
