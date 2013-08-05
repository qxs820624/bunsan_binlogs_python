#include <boost/python.hpp>

#include "bunsan/binlogs/python/Header.hpp"

using namespace boost::python;
namespace binlogs = bunsan::binlogs;

BOOST_PYTHON_MODULE(bunsan_binlogs)
{
    class_<binlogs::python::Header>("Header", no_init)
        .def_readonly("proto", &binlogs::python::Header::proto)
        .def_readonly("types", &binlogs::python::Header::types);
}
