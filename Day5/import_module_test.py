# =============================
# import XXX
"""
import module_test

module_test.func1()
"""

# =============================
# from dir import module
"""
from . import module_test

module_test.func2()
"""

# =============================
# from module import [function,var,*]

from module_test import *

func1()

