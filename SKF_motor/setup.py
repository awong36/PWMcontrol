from distutils.core import setup
from Cython.Build import cythonize
from distutils.extension import Extension
from Cython.Distutils import build_ext

# ext_modules = [Extension("CommonFunction", ["CommonFunction.pyx"])]

# setup(
# name = 'CommonFunction',
# cmdclass = {'build_ext': build_ext},
# ext_modules = ext_modules
# )

extensions = [Extension("*", ["*.pyx"])]

setup(
    ext_modules = cythonize(extensions)
)