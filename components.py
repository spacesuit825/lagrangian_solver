import numpy as np
import sympy as sy
from sympy.physics.mechanics import dynamicsymbols as ds

gravity = sy.symbols('g')

class Component:
    def __init__(self, name):
        self.name = name

    def potential(self):
        return None

    def kinetic(self):
        return None

class Point(Component):
    def __init__(self, location: list = [0, 0]):
        self.name = 'point'
        self.location = location

    def get_global_location(self):
        return self.location

class PointMass(Component):
    def __init__(self, parent, mass):
        self.name = 'mass'
        self.parent = parent
        self.mass = mass

    def kinetic(self):
        return 0.5 * self.mass * sy.diff((self.parent.get_global_location()[0]), sy.symbols('t'), 1) ** 2

    def potential(self):
        if self.parent.name in ('connector'):
            return self.mass * gravity * self.parent.get_global_location()[1]
        else:
            return None #self.parent.potential()

    def get_global_location(self):
        return self.parent.get_global_location()

class RigidConnector(Component):
    def __init__(self, parent, length, theta):
        self.name = 'connector'
        self.parent = parent
        self.length = length
        self.theta = theta

        self.start = self.parent.get_global_location()

    def get_global_location(self):
        return [self.start[0] + self.length * self.theta, self.start[1] + self.length * ((self.theta**2)/2)]

class Spring(Component):
    def __init__(self, parent, k, length, x = None, theta = None, parent2 = None):
        self.name = 'spring'
        self.parent = parent
        self.parent2 = parent2
        self.length = length
        self.k = k

        self.theta = theta
        self.x = x

        self.start = self.parent.get_global_location()
        
        if self.parent2:
            self.start2 = self.parent2.get_global_location()

    def kinetic(self):
        return None

    def potential(self):
        return 0.5 * self.k * self.get_global_location()[1] ** 2

    def get_global_location(self):
        if self.theta is None and self.x is None:
            return [self.start[0] - self.start2[0], self.start[0] - self.start2[0]]
        else:
            return [self.x, -self.start[0] + self.x]

class Drum(Component):
    def __init__(self, parent, J, radius, theta):
        self.name = 'drum'
        self.parent = parent
        self.J = J
        self.radius = radius
        self.theta = theta

        self.start = self.parent.get_global_location()

    def kinetic(self):
        return 0.5 * self.J * sy.diff(self.theta, sy.symbols('t'), 1) ** 2

    def get_global_location(self):
        return [self.start[0] + self.radius * self.theta, self.start[1] + self.radius * self.theta]

class RigidBody(Component):
    def __init__(self, parent, a, b, x, theta, y = None):
        self.name = 'rigid_body'
        self.parent = parent
        self.a = a
        self.b = b