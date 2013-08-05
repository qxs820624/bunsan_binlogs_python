#include "bunsan/binlogs/python/LogReader.hpp"

#include "bunsan/binlogs/LogFactory.hpp"

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
    logReader_(openReadOnly(path)) {}

boost::optional<LogReader::Entry> LogReader::read()
{
    if (!logReader_) {
        return boost::none;
    }
    Entry entry;
    std::string error;
    const MessageType *const msgType = logReader_->nextMessageType(&error);
    if (!msgType) {
        if (logReader_->eof()) {
            logReader_.reset();
            return boost::none;
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

}
}
}
