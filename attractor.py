from vector import Vector

class Attractor:
    location: Vector
    mass: float

    def __init__(self, location:Vector, mass:float) -> None:
        self.location = location
        self.mass = mass