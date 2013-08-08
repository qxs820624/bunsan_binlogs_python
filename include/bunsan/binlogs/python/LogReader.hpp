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

    const boost::filesystem::path &path() const;

    const Header &header() const;

    LogReader &iter();

    Entry next();

    void close();

private:
    const boost::filesystem::path path_;
    std::unique_ptr<binlogs::LogReader> logReader_;
    python::Header header_;
};

}
}
}
