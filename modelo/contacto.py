class Contacto():
    def __init__(self, nombre, apellidos, telefono):
        self.nombre = nombre
        self.apellidos = apellidos
        self.telefono = telefono

    def getNombre(self):
        return self.nombre

    def getApellidos(self):
        return self.apellidos

    def getTelefono(self):
        return self.telefono