#include <boost/python.hpp>
#include <boost/python/suite/indexing/vector_indexing_suite.hpp>

#include "bunsan/binlogs/python/Header.hpp"
#include "bunsan/binlogs/python/LogReader.hpp"

using namespace boost::python;
namespace binlogs = bunsan::binlogs;

static object getStringListRepr(const binlogs::python::StringList &stringList)
{
    list l;
    for (const std::string &s: stringList) {
        l.append(str(s).attr("__repr__")());
    }
    return str("[") + str(", ").join(l) + str("]");
}

static object getHeaderRepr(const binlogs::python::Header &header)
{
    return str("Header(proto={0!r}, types={1!r})").attr("format")(header.proto, header.types);
}

static object getLogReaderEntryRepr(const binlogs::python::LogReader::Entry &entry)
{
    return str("LogReader.Entry(type={0!r}, data={1!r})").attr("format")(entry.type, entry.data);
}

static object getPathString(const boost::filesystem::path &path)
{
    return str(path.string());
}

static object getPathRepr(const boost::filesystem::path &path)
{
    return getPathString(path).attr("__repr__")();
}

BOOST_PYTHON_MODULE(_binlogs)
{
    class_<boost::filesystem::path>("Path", init<std::string>())
        .def("__str__", getPathString)
        .def("__repr__", getPathRepr);

    class_<binlogs::python::StringList>("StringList")
        .def(vector_indexing_suite<binlogs::python::StringList>())
        .def("__repr__", getStringListRepr);

    class_<binlogs::python::Header>("Header", no_init)
        .def_readonly("proto", &binlogs::python::Header::proto)
        .def_readonly("types", &binlogs::python::Header::types)
        .def("__repr__", getHeaderRepr);

    class_<binlogs::python::LogReader::Entry>("LogReader.Entry")
        .def_readonly("type", &binlogs::python::LogReader::Entry::type)
        .def_readonly("data", &binlogs::python::LogReader::Entry::data)
        .def("__repr__", getLogReaderEntryRepr);
}
