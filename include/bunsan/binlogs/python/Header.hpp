#pragma once

#include "bunsan/binlogs/Header.hpp"

#include <string>

namespace bunsan {
namespace binlogs {
namespace python {

struct Header {
    static Header get(const binlogs::Header &header);

    std::string proto;
    std::vector<std::string> types;
};

}
}
}
