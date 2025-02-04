DFT-D3 Python API
-----------------

Python interface for the D3 dispersion model.
This Python project is targeted at developers who want to interface their project via Python with ``s-dftd3``.

This interface provides access to the C-API of ``s-dftd3`` via the CFFI module.
The low-level CFFI interface is available in the ``dftd3.libdftd3`` module and only required for implementing other interfaces.
A more pythonic interface is provided in the ``dftd3.interface`` module which can be used to build more specific interfaces.

.. code:: python

   from dftd3.interface import RationalDampingParam, DispersionModel
   import numpy as np
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
   print(res.get("energy"))  # Results in atomic units
   # => -0.029489232932494884


QCSchema Integration
~~~~~~~~~~~~~~~~~~~~

This Python API natively understands QCSchema and the `QCArchive infrastructure <http://docs.qcarchive.molssi.org>`_.
If the QCElemental package is installed the ``dftd3.qcschema`` module becomes importable and provides the ``run_qcschema`` function.

.. code:: python

   from dftd3.qcschema import run_qcschema
   import qcelemental as qcel
   atomic_input = qcel.models.AtomicInput(
       molecule = qcel.models.Molecule(
           symbols = ["O", "H", "H"],
           geometry = [
               0.00000000000000,  0.00000000000000, -0.73578586109551,
               1.44183152868459,  0.00000000000000,  0.36789293054775,
              -1.44183152868459,  0.00000000000000,  0.36789293054775
           ],
       ),
       driver = "energy",
       model = {
           "method": "tpss",
       },
       keywords = {
           "level_hint": "d3bj",
       },
   )

   atomic_result = run_qcschema(atomic_input)
   print(atomic_result.return_result)
   # => -0.0004204244108151285


Building the extension module
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To perform an out-of-tree build some version of ``s-dftd3`` has to be available on your system and preferably findable by ``pkg-config``.
Try to find a ``s-dftd3`` installation you build against first with

.. code:: sh

   pkg-config --modversion s-dftd3

Adjust the ``PKG_CONFIG_PATH`` environment variable to include the correct directories to find the installation if necessary.


Using pip
^^^^^^^^^

This project support installation with pip as an easy way to build the Python API.

- C compiler to build the C-API and compile the extension module (the compiler name should be exported in the ``CC`` environment variable)
- Python 3.6 or newer
- The following Python packages are required additionally

  - `cffi <https://cffi.readthedocs.io/>`_
  - `numpy <https://numpy.org/>`_
  - `pkgconfig <https://pypi.org/project/pkgconfig/>`_ (setup only)

Make sure to have your C compiler set to the ``CC`` environment variable

.. code:: sh

   export CC=gcc

Install the project with pip

.. code:: sh

   pip install .



Using meson
^^^^^^^^^^^

This directory contains a separate meson build file to allow the out-of-tree build of the CFFI extension module.
The out-of-tree build requires

- C compiler to build the C-API and compile the extension module
- `meson <https://mesonbuild.com>`_ version 0.53 or newer
- a build-system backend, *i.e.* `ninja <https://ninja-build.org>`_ version 1.7 or newer
- Python 3.6 or newer with the `CFFI <https://cffi.readthedocs.io/>`_ package installed

Setup a build with

.. code:: sh

   meson setup _build -Dpython_version=3

The Python version can be used to select a different Python version, it defaults to ``'3'``.
Python 2 is not supported with this project, the Python version key is meant to select between several local Python 3 versions.

Compile the project with

.. code:: sh

   meson compile -C _build

The extension module is now available in ``_build/dftd3/_libdftd3.*.so``.
You can install as usual with

.. code:: sh

   meson configure _build --prefix=/path/to/install
   meson install -C _build
