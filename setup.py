from pybind11.setup_helpers import Pybind11Extension, build_ext
from setuptools import setup


ext_modules = [
    Pybind11Extension(
        "netnomos._hittingset_native",
        ["cpp/hittingset_native.cpp"],
    ),
]


setup(
    ext_modules=ext_modules,
    cmdclass={"build_ext": build_ext},
)
