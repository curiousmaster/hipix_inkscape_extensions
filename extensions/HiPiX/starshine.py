#!/usr/bin/env python
#
# Copyright (C) 2021 Stefan Benediktsson
#
# GNU Affero General Public License v3.0
# Permissions of this strongest copyleft license are
# conditioned on making available complete source code
# of licensed works and modifications, which include
# larger works using a licensed work, under the same
# license. Copyright and license notices must be preserved.
# Contributors provide an express grant of patent rights.
# When a modified version is used to provide a service
# over a network, the complete source code of the modified
# version must be made available.
#
"""
Generate a Starshine as SVG.
"""

import random
from math import acos, cos, radians, sin, sqrt, tan

import inkex



def points_to_svgd(p):
        """
        p: list of 2 tuples (x, y coordinates)
        """
        f = p[0]
        p = p[1:]
        svgd = 'M{:.3f},{:.3f}'.format(f[0], f[1])
        for x in p:
                svgd += 'L{:.3f},{:.3f}'.format(x[0], x[1])
        svgd +='Z'
        return svgd

def checkSize(a, b):
        if a >= b:
                return b, a
        else:
                return a, b

class Starshine(inkex.GenerateExtension):
        container_label = 'Rendered Starshine'
        def add_arguments(self, pars):

                pars.add_argument("--r1", type=int, default=20, help="Inner Radius min")
                pars.add_argument("--r2", type=int, default=20, help="Inner Radius max")
                pars.add_argument("--R1", type=int, default=350, help="Outer Radius min")
                pars.add_argument("--R2", type=int, default=350, help="Outer Radius min")
                pars.add_argument("--a1", type=int, default=5, help="Angle min")
                pars.add_argument("--a2", type=int, default=7, help="Angle max")



        def generate(self):
                r1 = self.options.r1
                r2 = self.options.r2
                R1 = self.options.R1
                R2 = self.options.R2
                a1 = self.options.a1
                a2 = self.options.a2


                # generate points: list of (x, y) pairs

                r1, r2 = checkSize(r1, r2)
                R1, R2 = checkSize(R1, R2)
                a1, a2 = checkSize(a1, a2)
                a = 0

                style = {'stroke': '#000000', 'fill': '#000000', 'stroke-width': str(self.svg.unittouu('1px'))}

                points = []

                while a < 360:
                    dI = random.randint(r1,r2)
                    dO = random.randint(R1,R2)
                    ad = random.randint(a1,a2)

                    x00 = cos(radians(a)) * dI
                    y00 = sin(radians(a)) * dI

                    x10 = cos(radians(a+ad/2)) * dO
                    y10 = sin(radians(a+ad/2)) * dO

                    x01 = cos(radians(a+ad)) * dI
                    y01 = sin(radians(a+ad)) * dI

                    points.append((x00, y00))
                    points.append((x10, y10))
                    points.append((x01, y01))

                    a = a+ad

                path = points_to_svgd(points)

                yield inkex.PathElement(style=str(inkex.Style(style)), d=str(path))


if __name__ == '__main__':
        Starshine().run()

