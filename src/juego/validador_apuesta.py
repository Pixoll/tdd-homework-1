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