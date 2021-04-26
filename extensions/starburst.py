#!/usr/bin/env python
#
# Copyright (C) 2021 Stefan Benediktsson
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#
"""
Generate a StarBurst as SVG.
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

class StarBurst(inkex.GenerateExtension):
	container_label = 'Rendered StarBurst'
	def add_arguments(self, pars):
		pars.add_argument("--r1", type=int, default=20, help="Inner Radius min")
		pars.add_argument("--r2", type=int, default=20, help="Inner Radius max")
		pars.add_argument("--R1", type=int, default=350, help="Outer Radius min")
		pars.add_argument("--R2", type=int, default=350, help="Outer Radius min")
		pars.add_argument("--a1", type=int, default=5, help="Angle min")
		pars.add_argument("--a2", type=int, default=7, help="Angle max")
		pars.add_argument("--ad1", type=int, default=3, help="Angle delta min")
		pars.add_argument("--ad2", type=int, default=2, help="Angle delta max")



	def generate(self):
		r1 = self.options.r1
		r2 = self.options.r2
		R1 = self.options.R1
		R2 = self.options.R2
		a1 = self.options.a1
		a2 = self.options.a2
		ad1 = self.options.ad1
		ad2 = self.options.ad2

		# generate points: list of (x, y) pairs

		r1, r2 = checkSize(r1, r2)
		R1, R2 = checkSize(R1, R2)
		a1, a2 = checkSize(a1, a2)
		ad1, ad2 = checkSize(ad1, ad2)

		a = 0
		oX = 0
		oY = 0
		style = {'stroke': '#000000', 'fill': '#000000', 'stroke-width': str(self.svg.unittouu('1px'))}

		while a < 360:
			a = a+random.randint(a1,a2)
			dI = random.randint(r1,r2)
			dO = random.randint(R1,R2)
			ad = random.randint(ad1,ad2)

			x0 = int(cos(radians(a)) * dI)
			y0 = int(sin(radians(a)) * dI)

			x10 = int(cos(radians(a-ad/2)) * dO)
			y10 = int(sin(radians(a-ad/2)) * dO)

			x11 = int(cos(radians(a+ad/2)) * dO)
			y11 = int(sin(radians(a+ad/2)) * dO)

			points = []
			points.append((x0, y0))
			points.append((x10,y10))
			points.append((x11,y11))
			path = points_to_svgd(points)

			yield inkex.PathElement(style=str(inkex.Style(style)), d=str(path))

if __name__ == '__main__':
	StarBurst().run()
