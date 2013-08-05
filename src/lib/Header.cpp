#include "bunsan/binlogs/python/Header.hpp"

namespace bunsan {
namespace binlogs {
namespace python {

Header Header::get(const binlogs::Header &header)
{
    Header h;
    if (!header.proto.SerializeToString(&h.proto)) {
        throw std::runtime_error("Unable to serialize bunsan::binlogs::Header::proto.");
    }
    h.types = header.types;
    return h;
}

}
}
}
