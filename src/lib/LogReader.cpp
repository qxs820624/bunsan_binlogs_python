#include "bunsan/binlogs/python/LogReader.hpp"

#include "bunsan/binlogs/LogFactory.hpp"

#include <boost/python/iterator.hpp>

namespace bunsan {
namespace binlogs {
namespace python {

namespace {

std::unique_ptr<binlogs::LogReader> openReadOnly(const boost::filesystem::path &path)
{
    std::string error;
    auto logReader = binlogs::openReadOnly(path, &error);
    if (!logReader) {
        throw std::runtime_error(error);
    }
    return logReader;
}

}

LogReader::LogReader(const boost::filesystem::path &path):
    path_(path),
    logReader_(openReadOnly(path_)),
    header_(python::Header::get(logReader_->messageTypePool().header())) {}

const boost::filesystem::path &LogReader::path() const
{
    return path_;
}

const Header &LogReader::header() const
{
    return header_;
}

LogReader &LogReader::iter()
{
    return *this;
}

LogReader::Entry LogReader::next()
{
    if (!logReader_) {
        boost::python::objects::stop_iteration_error();
    }
    Entry entry;
    std::string error;
    const MessageType *const msgType = logReader_->nextMessageType(&error);
    if (!msgType) {
        if (logReader_->eof()) {
            logReader_.reset();
            boost::python::objects::stop_iteration_error();
        }
        throw std::runtime_error(error);
    }
    entry.type = msgType->typeName();
    const auto msg = msgType->newMessage();
    if (!logReader_->read(msg, &error)) {
        throw std::runtime_error(error);
    }
    if (!msg->SerializeToString(&entry.data)) {
        throw std::runtime_error("Unable to serialize message.");
    }
    return entry;
}

void LogReader::close()
{
    if (logReader_) {
        std::string error;
        if (!logReader_->close(&error)) {
            throw std::runtime_error(error);
        }
    }
}

}
}
}
