#pragma once

#include "bunsan/binlogs/python/Header.hpp"

#include "bunsan/binlogs/LogReader.hpp"

#include <boost/filesystem/path.hpp>
#include <boost/noncopyable.hpp>
#include <boost/optional.hpp>

#include <memory>

namespace bunsan {
namespace binlogs {
namespace python {

class LogReader: private boost::noncopyable {
public:
    struct Entry {
        std::string type;
        std::string data;
    };

public:
    explicit LogReader(const boost::filesystem::path &path);

    const Header &header() const;

    /// \return boost::none on EOF
    boost::optional<Entry> read();

private:
    std::unique_ptr<binlogs::LogReader> logReader_;
    python::Header header_;
};

}
}
}
