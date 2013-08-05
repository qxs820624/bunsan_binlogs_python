# distutils: language = c++
# distutils: libraries = bunsan_pm_compatibility
# distutils: extra_compile_args = -std=c++11


from libcpp cimport bool
from libcpp.string cimport string
from libcpp.vector cimport vector


cdef extern from "bunsan/binlogs/Header.hpp" namespace "bunsan::binlogs":
    cdef cppclass Header:
        cdef proto
        cdef vector[string] types
