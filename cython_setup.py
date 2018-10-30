from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
from Cython.Build import cythonize
import numpy as np

ext_modules = [Extension("rlscore.utilities.swapped",["rlscore/utilities/swapped.pyx"], include_dirs=[np.get_include()]),
    Extension("rlscore.learner._rls",["rlscore/learner/_rls.pyx"], include_dirs=[np.get_include()]),
    Extension("rlscore.learner._global_rankrls",["rlscore/learner/_global_rankrls.pyx"], include_dirs=[np.get_include()]),
    Extension("rlscore.learner._two_step_rls",["rlscore/learner/_two_step_rls.pyx"], include_dirs=[np.get_include()]),
    Extension("rlscore.learner._steepest_descent_mmc",["rlscore/learner/_steepest_descent_mmc.pyx"], include_dirs=[np.get_include()]),
    Extension("rlscore.learner._interactive_rls_classifier",["rlscore/learner/_interactive_rls_classifier.pyx"], include_dirs=[np.get_include()]),    
    Extension("rlscore.learner._greedy_rls",["rlscore/learner/_greedy_rls.pyx"], include_dirs=[np.get_include()]),
    Extension("rlscore.utilities._sampled_kronecker_products",["rlscore/utilities/_sampled_kronecker_products.pyx"], include_dirs=[np.get_include()], extra_compile_args=['-fopenmp'], extra_link_args=['-fopenmp'],)
    ]

setup(
    name = 'cmodules',
    cmdclass = {'build_ext': build_ext},
    ext_modules = cythonize(ext_modules),
    )

