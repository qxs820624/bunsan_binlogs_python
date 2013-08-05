#pragma once

#include "bunsan/binlogs/Header.hpp"

#include <string>

namespace bunsan {
namespace binlogs {
namespace python {

struct Header {
    std::string proto;
    std::vector<std::string> types;
};

}
}
}
