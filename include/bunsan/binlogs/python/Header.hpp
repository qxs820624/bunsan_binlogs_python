#pragma once

#include "bunsan/binlogs/Header.hpp"

#include <string>
#include <vector>

namespace bunsan {
namespace binlogs {
namespace python {

typedef std::vector<std::string> StringList;

struct Header {
    static Header get(const binlogs::Header &header);

    std::string proto;
    StringList types;
};

}
}
}
