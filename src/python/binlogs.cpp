#include <boost/python.hpp>
#include <boost/python/suite/indexing/vector_indexing_suite.hpp>

#include "bunsan/binlogs/python/Header.hpp"

using namespace boost::python;
namespace binlogs = bunsan::binlogs;

namespace
{

object getStringListRepr(const binlogs::python::StringList &stringList)
{
    list l;
    for (const std::string &s: stringList) {
        l.append(str(s).attr("__repr__")());
    }
    return str("[") + str(", ").join(l) + str("]");
}

}

BOOST_PYTHON_MODULE(_binlogs)
{
    class_<binlogs::python::StringList>("StringList")
        .def(vector_indexing_suite<binlogs::python::StringList>())
        .def("__repr__", getStringListRepr);

    class_<binlogs::python::Header>("Header", no_init)
        .def_readonly("proto", &binlogs::python::Header::proto)
        .def_readonly("types", &binlogs::python::Header::types);
}
