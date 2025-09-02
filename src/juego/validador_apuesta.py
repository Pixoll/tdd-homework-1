import math
class ValidadorApuesta:
    def __init__(self, pinta, cantidad):
        self.pinta = pinta
        self.cantidad = cantidad
    
    @staticmethod
    def VerificarRangoPinta(pinta):
        if pinta<1 or pinta>6:
            return False
        return True
        
    @staticmethod
    def VerificarRangoCantidad(cantidad):
        if cantidad<1:
            return False
        return True
    
    @staticmethod
    def CambioToAses(pinta_actual, cantidad_actual, pinta_nueva):
        if pinta_nueva != 1:
            return (cantidad_actual, False)
        
        if cantidad_actual%2 == 0:
            cantidad_nueva = (cantidad_actual//2)+1
        else:
            cantidad_nueva = math.ceil(cantidad_actual/2)
        return (cantidad_nueva, True)
    
    @staticmethod
    def CambioDeAshes(pinta_actual, cantidad_actual, pinta_nueva):
        if pinta_actual != 1:
            return (cantidad_actual, False)
        
        cantidad_nueva = (cantidad_actual*2)+1
        
        return (cantidad_nueva, True)