# This file is part of s-dftd3.
# SPDX-Identifier: LGPL-3.0-or-later
#
# s-dftd3 is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# s-dftd3 is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with s-dftd3.  If not, see <https://www.gnu.org/licenses/>.

from dftd3.interface import (
    Structure,
    RationalDampingParam,
    ZeroDampingParam,
    ModifiedZeroDampingParam,
    ModifiedRationalDampingParam,
    DispersionModel,
)
from pytest import approx, raises
import numpy as np


def test_rational_damping_noargs():
    """Check constructor of damping parameters for insufficient arguments"""

    with raises(RuntimeError):
        RationalDampingParam()

    with raises(RuntimeError, match="s8"):
        RationalDampingParam(a1=0.4, a2=5.0)

    with raises(RuntimeError, match="a1"):
        RationalDampingParam(s8=1.0, a2=5.0)

    with raises(RuntimeError, match="a2"):
        RationalDampingParam(s8=1.0, a1=0.4)


def test_zero_damping_noargs():
    """Check constructor of damping parameters for insufficient arguments"""

    with raises(RuntimeError):
        ZeroDampingParam()

    with raises(RuntimeError, match="s8"):
        ZeroDampingParam(rs6=1.2)

    with raises(RuntimeError, match="rs6"):
        ZeroDampingParam(s8=1.0)


def test_modified_rational_damping_noargs():
    """Check constructor of damping parameters for insufficient arguments"""

    with raises(RuntimeError):
        ModifiedRationalDampingParam()

    with raises(RuntimeError, match="s8"):
        ModifiedRationalDampingParam(a1=0.4, a2=5.0)

    with raises(RuntimeError, match="a1"):
        ModifiedRationalDampingParam(s8=1.0, a2=5.0)

    with raises(RuntimeError, match="a2"):
        ModifiedRationalDampingParam(s8=1.0, a1=0.4)


def test_modified_zero_damping_noargs():
    """Check constructor of damping parameters for insufficient arguments"""

    with raises(RuntimeError):
        ModifiedZeroDampingParam()

    with raises(RuntimeError, match="s8"):
        ModifiedZeroDampingParam(rs6=1.2, bet=1.0)

    with raises(RuntimeError, match="rs6"):
        ModifiedZeroDampingParam(s8=1.0, bet=1.0)

    with raises(RuntimeError, match="bet"):
        ModifiedZeroDampingParam(s8=1.0, rs6=1.2)


def test_structure():
    """check if the molecular structure data is working as expected."""

    numbers = np.array(
        [6, 7, 6, 7, 6, 6, 6, 8, 7, 6, 8, 7, 6, 6, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    )
    positions = np.array(
        [
            [+2.02799738646442, +0.09231312124713, -0.14310895950963],
            [+4.75011007621000, +0.02373496014051, -0.14324124033844],
            [+6.33434307654413, +2.07098865582721, -0.14235306905930],
            [+8.72860718071825, +1.38002919517619, -0.14265542523943],
            [+8.65318821103610, -1.19324866489847, -0.14231527453678],
            [+6.23857175648671, -2.08353643730276, -0.14218299370797],
            [+5.63266886875962, -4.69950321056008, -0.13940509630299],
            [+3.44931709749015, -5.48092386085491, -0.14318454855466],
            [+7.77508917214346, -6.24427872938674, -0.13107140408805],
            [10.30229550927022, -5.39739796609292, -0.13672168520430],
            [12.07410272485492, -6.91573621641911, -0.13666499342053],
            [10.70038521493902, -2.79078533715849, -0.14148379504141],
            [13.24597858727017, -1.76969072232377, -0.14218299370797],
            [+7.40891694074004, -8.95905928176407, -0.11636933482904],
            [+1.38702118184179, +2.05575746325296, -0.14178615122154],
            [+1.34622199478497, -0.86356704498496, +1.55590600570783],
            [+1.34624089204623, -0.86133716815647, -1.84340893849267],
            [+5.65596919189118, +4.00172183859480, -0.14131371969009],
            [14.67430918222276, -3.26230980007732, -0.14344911021228],
            [13.50897177220290, -0.60815166181684, +1.54898960808727],
            [13.50780014200488, -0.60614855212345, -1.83214617078268],
            [+5.41408424778406, -9.49239668625902, -0.11022772492007],
            [+8.31919801555568, -9.74947502841788, +1.56539243085954],
            [+8.31511620712388, -9.76854236502758, -1.79108242206824],
        ]
    )

    # Constructor should raise an error for nuclear fusion input
    with raises(RuntimeError, match="Too close interatomic distances found"):
        Structure(numbers, np.zeros((24, 3)))

    # The Python class should protect from garbage input like this
    with raises(ValueError, match="Dimension missmatch"):
        Structure(np.array([1, 1, 1]), positions)

    # Also check for sane coordinate input
    with raises(ValueError, match="Expected tripels"):
        Structure(numbers, np.random.rand(7))

    # Construct real molecule
    mol = Structure(numbers, positions)

    # Try to update a structure with missmatched coordinates
    with raises(ValueError, match="Dimension missmatch for positions"):
        mol.update(np.random.rand(7))

    # Try to add a missmatched lattice
    with raises(ValueError, match="Invalid lattice provided"):
        mol.update(positions, np.random.rand(7))

    # Try to update a structure with nuclear fusion coordinates
    with raises(RuntimeError, match="Too close interatomic distances found"):
        mol.update(np.zeros((24, 3)))


def test_pbe0_d3_bj():

   numbers = np.array([1, 1, 6, 5, 1, 15, 8, 17, 13, 15, 5, 1, 9, 15, 1, 15])
   positions = np.array([  # Coordinates in Bohr
       [+2.79274810283778, +3.82998228828316, -2.79287054959216],
       [-1.43447454186833, +0.43418729987882, +5.53854345129809],
       [-3.26268343665218, -2.50644032426151, -1.56631149351046],
       [+2.14548759959147, -0.88798018953965, -2.24592534506187],
       [-4.30233097423181, -3.93631518670031, -0.48930754109119],
       [+0.06107643564880, -3.82467931731366, -2.22333344469482],
       [+0.41168550401858, +0.58105573172764, +5.56854609916143],
       [+4.41363836635653, +3.92515871809283, +2.57961724984000],
       [+1.33707758998700, +1.40194471661647, +1.97530004949523],
       [+3.08342709834868, +1.72520024666801, -4.42666116106828],
       [-3.02346932078505, +0.04438199934191, -0.27636197425010],
       [+1.11508390868455, -0.97617412809198, +6.25462847718180],
       [+0.61938955433011, +2.17903547389232, -6.21279842416963],
       [-2.67491681346835, +3.00175899761859, +1.05038813614845],
       [-4.13181080289514, -2.34226739863660, -3.44356159392859],
       [+2.85007173009739, -2.64884892757600, +0.71010806424206],
   ])
   model = DispersionModel(numbers, positions)
   res = model.get_dispersion(RationalDampingParam(method="pbe0"), grad=False)
   assert approx(res.get("energy")) == -0.029489232932494884


def test_b3lyp_d3_zero():

   numbers = np.array([1, 1, 6, 5, 1, 15, 8, 17, 13, 15, 5, 1, 9, 15, 1, 15])
   positions = np.array([  # Coordinates in Bohr
       [+2.79274810283778, +3.82998228828316, -2.79287054959216],
       [-1.43447454186833, +0.43418729987882, +5.53854345129809],
       [-3.26268343665218, -2.50644032426151, -1.56631149351046],
       [+2.14548759959147, -0.88798018953965, -2.24592534506187],
       [-4.30233097423181, -3.93631518670031, -0.48930754109119],
       [+0.06107643564880, -3.82467931731366, -2.22333344469482],
       [+0.41168550401858, +0.58105573172764, +5.56854609916143],
       [+4.41363836635653, +3.92515871809283, +2.57961724984000],
       [+1.33707758998700, +1.40194471661647, +1.97530004949523],
       [+3.08342709834868, +1.72520024666801, -4.42666116106828],
       [-3.02346932078505, +0.04438199934191, -0.27636197425010],
       [+1.11508390868455, -0.97617412809198, +6.25462847718180],
       [+0.61938955433011, +2.17903547389232, -6.21279842416963],
       [-2.67491681346835, +3.00175899761859, +1.05038813614845],
       [-4.13181080289514, -2.34226739863660, -3.44356159392859],
       [+2.85007173009739, -2.64884892757600, +0.71010806424206],
   ])
   model = DispersionModel(numbers, positions)
   res = model.get_dispersion(ZeroDampingParam(method="b3lyp"), grad=False)
   assert approx(res.get("energy")) == -0.022714307913634844


def test_pbe_d3_bjm():

   numbers = np.array([1, 1, 6, 5, 1, 15, 8, 17, 13, 15, 5, 1, 9, 15, 1, 15])
   positions = np.array([  # Coordinates in Bohr
       [+2.79274810283778, +3.82998228828316, -2.79287054959216],
       [-1.43447454186833, +0.43418729987882, +5.53854345129809],
       [-3.26268343665218, -2.50644032426151, -1.56631149351046],
       [+2.14548759959147, -0.88798018953965, -2.24592534506187],
       [-4.30233097423181, -3.93631518670031, -0.48930754109119],
       [+0.06107643564880, -3.82467931731366, -2.22333344469482],
       [+0.41168550401858, +0.58105573172764, +5.56854609916143],
       [+4.41363836635653, +3.92515871809283, +2.57961724984000],
       [+1.33707758998700, +1.40194471661647, +1.97530004949523],
       [+3.08342709834868, +1.72520024666801, -4.42666116106828],
       [-3.02346932078505, +0.04438199934191, -0.27636197425010],
       [+1.11508390868455, -0.97617412809198, +6.25462847718180],
       [+0.61938955433011, +2.17903547389232, -6.21279842416963],
       [-2.67491681346835, +3.00175899761859, +1.05038813614845],
       [-4.13181080289514, -2.34226739863660, -3.44356159392859],
       [+2.85007173009739, -2.64884892757600, +0.71010806424206],
   ])
   model = DispersionModel(numbers, positions)
   res = model.get_dispersion(ModifiedRationalDampingParam(method="pbe"), grad=False)
   assert approx(res.get("energy")) == -0.06327406660942464


def test_bp_d3_zerom():

   numbers = np.array([1, 1, 6, 5, 1, 15, 8, 17, 13, 15, 5, 1, 9, 15, 1, 15])
   positions = np.array([  # Coordinates in Bohr
       [+2.79274810283778, +3.82998228828316, -2.79287054959216],
       [-1.43447454186833, +0.43418729987882, +5.53854345129809],
       [-3.26268343665218, -2.50644032426151, -1.56631149351046],
       [+2.14548759959147, -0.88798018953965, -2.24592534506187],
       [-4.30233097423181, -3.93631518670031, -0.48930754109119],
       [+0.06107643564880, -3.82467931731366, -2.22333344469482],
       [+0.41168550401858, +0.58105573172764, +5.56854609916143],
       [+4.41363836635653, +3.92515871809283, +2.57961724984000],
       [+1.33707758998700, +1.40194471661647, +1.97530004949523],
       [+3.08342709834868, +1.72520024666801, -4.42666116106828],
       [-3.02346932078505, +0.04438199934191, -0.27636197425010],
       [+1.11508390868455, -0.97617412809198, +6.25462847718180],
       [+0.61938955433011, +2.17903547389232, -6.21279842416963],
       [-2.67491681346835, +3.00175899761859, +1.05038813614845],
       [-4.13181080289514, -2.34226739863660, -3.44356159392859],
       [+2.85007173009739, -2.64884892757600, +0.71010806424206],
   ])
   model = DispersionModel(numbers, positions)
   res = model.get_dispersion(ModifiedZeroDampingParam(method="bp"), grad=False)
   assert approx(res.get("energy")) == -0.02601335734255335
