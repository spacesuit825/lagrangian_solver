import numpy as np
import sympy as sy
from sympy.physics.mechanics import dynamicsymbols as ds
from sympy import print_latex, init_printing
from IPython import display

from components import *

init_printing(use_latex=True)

# Double Pendulum

# Q_1 = ds('Q_1')
# Q_2 = ds('Q_2')

# point = Point()
# connector_1 = RigidConnector(point, length = sy.symbols('L_1'), theta = Q_1)
# mass_1 = PointMass(connector_1, mass = sy.symbols('m_1'))
# connector_2 = RigidConnector(mass_1, length = sy.symbols('L_2'), theta = Q_2)
# mass_2 = PointMass(connector_2, mass = sy.symbols('m_2'))

# scene = [point, connector_1, mass_1, connector_2, mass_2]
# coords = [Q_1, Q_2]


# Double mass spring

# x_1 = ds('x_1')
# x_2 = ds('x_2')

# point = Point()
# spring_1 = Spring(point, k = sy.symbols('k_1'), length = sy.symbols('L_1'), x = x_1)
# mass_1 = PointMass(spring_1, mass = sy.symbols('m_1'))
# spring_2 = Spring(mass_1, k = sy.symbols('k_2'), length = sy.symbols('L_2'), x = x_2)
# mass_2 = PointMass(spring_2, mass = sy.symbols('m_2'))

# scene = [point, spring_1, mass_1, spring_2, mass_2]
# coords = [x_1, x_2]


# Double Pendulum with spring

# Q_1 = ds('Q_1')
# Q_2 = ds('Q_2')

# point_1 = Point()
# connector_1 = RigidConnector(point_1, length = sy.symbols('L_1'), theta = Q_1)
# mass_1 = PointMass(connector_1, mass = sy.symbols('m_1'))

# point_2 = Point()
# connector_2 = RigidConnector(point_2, length = sy.symbols('L_2'), theta = Q_2)
# mass_2 = PointMass(connector_2, mass = sy.symbols('m_2'))

# spring = Spring(parent = mass_1, parent2 = mass_2, k = sy.symbols('k_2'), length = sy.symbols('L_2'))

# scene = [point_1, point_2, spring, mass_1, connector_1, connector_2, mass_2]
# coords = [Q_1, Q_2]


# Spring loaded mass with pendulum

# x = ds('x')
# Q = ds('Q')

# point = Point()
# spring = Spring(point, k = sy.symbols('k_1'), length = sy.symbols('L_1'), x = x)
# mass_1 = PointMass(spring, mass = sy.symbols('m_1'))
# connector = RigidConnector(mass_1, length = sy.symbols('L_1'), theta = Q)
# mass_2 = PointMass(connector, mass = sy.symbols('m_2'))

# scene = [point, spring, mass_1, connector, mass_2]
# coords = [x, Q]


# Inverted Pendulums with triple spring

# Q_1 = ds('Q_1')
# Q_2 = ds('Q_2')

# point_1 = Point()
# connector_1 = RigidConnector(point_1, length = sy.symbols('L_1'), theta = Q_1)
# mass_1 = PointMass(connector_1, mass = sy.symbols('m_1'))

# point_2 = Point()
# connector_2 = RigidConnector(point_2, length = sy.symbols('L_2'), theta = Q_2)
# mass_2 = PointMass(connector_2, mass = sy.symbols('m_2'))

# spring_1 = Spring(parent = mass_1, parent2 = mass_2, k = sy.symbols('k_1'), length = sy.symbols('L_2'))

# point_3 = Point()
# spring_2 = Spring(parent = mass_1, parent2 = point_3, k = sy.symbols('k_2'), length = sy.symbols('L_2'))

# point_4 = Point()
# spring_3 = Spring(parent = mass_2, parent2 = point_4, k = sy.symbols('k_3'), length = sy.symbols('L_2'))

# scene = [point_1, point_2, point_3, point_4, spring_1, spring_2, spring_3, mass_1, connector_1, connector_2, mass_2]
# coords = [Q_1, Q_2]


# Drum with springed mass

Q = ds('Q')
x = ds('x')

point_1 = Point()
drum = Drum(point_1, J = sy.symbols('J'), radius = sy.symbols('R'), theta = Q)

point_2 = Point()
spring_1 = Spring(parent = point_2, parent2 = drum, k = sy.symbols('k_1'), length = sy.symbols('L_2'))

spring_2 = Spring(parent = drum, k = sy.symbols('k_2'), length = sy.symbols('L_2'), x = x)
mass = PointMass(spring_2, sy.symbols('m'))

scene = [point_1, point_2, spring_1, spring_2, mass, drum]
coords = [Q, x]


class Simulate:
    def __init__(self, scene: list, coords):
        self.scene = scene
        self.coords = coords

        self.T = self.assemble_T()
        self.V = self.assemble_V()

        print('\n Kinetic Energy')
        display.display(self.T)
        print('\n Potential Energy')
        display.display(self.V)

        self.eqs = self.motion()

        print('\n Equation 1')
        display.display(self.eqs[0])
        print('\n Equation 2')
        display.display(self.eqs[1])

    def assemble_T(self):
        T = 0 
        for i in self.scene:
            if i.kinetic() != None:
                T += i.kinetic()
        return T

    def assemble_V(self):
        V = 0
        for i in self.scene:
            if i.potential() != None:
                V += i.potential()
        return V

    def motion(self):
        eqs = []
        for i in coords:
            dq = sy.diff((i), sy.symbols('t'), 1)
            dTdq = sy.diff((self.T), dq, 1)
            L = sy.diff((dTdq), sy.symbols('t'), 1) + sy.diff((self.V), i, 1)
            eqs.append(L)
        return eqs

sim = Simulate(scene, coords)