#include <boost/python.hpp>
#include <boost/python/suite/indexing/vector_indexing_suite.hpp>

#include "bunsan/binlogs/python/Header.hpp"

using namespace boost::python;
namespace binlogs = bunsan::binlogs;

BOOST_PYTHON_MODULE(_binlogs)
{
    class_<binlogs::python::StringList>("StringList")
        .def(vector_indexing_suite<binlogs::python::StringList>());

    class_<binlogs::python::Header>("Header", no_init)
        .def_readonly("proto", &binlogs::python::Header::proto)
        .def_readonly("types", &binlogs::python::Header::types);
}
