#include "bunsan/binlogs/python/LogReader.hpp"

#include "bunsan/binlogs/LogFactory.hpp"

#include <boost/python/iterator.hpp>
#include <boost/scope_exit.hpp>

#include <stdexcept>

namespace bunsan {
namespace binlogs {
namespace python {

LogReader::LogReader(const boost::filesystem::path &path):
    path_(path),
    logReader_(binlogs::openReadOnly(path)),
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
    const MessageType *const msgType = logReader_->nextMessageType();
    if (!msgType) {
        BOOST_ASSERT(logReader_->eof());
        logReader_.reset();
        boost::python::objects::stop_iteration_error();
    }
    entry.type = msgType->typeName();
    const auto msg = msgType->newMessage();
    logReader_->read(msg);
    if (!msg->SerializeToString(&entry.data)) {
        throw std::runtime_error("Unable to serialize message.");
    }
    return entry;
}

void LogReader::close()
{
    if (logReader_) {
        BOOST_SCOPE_EXIT_ALL(this)
        {
            logReader_.reset();
        };
        logReader_->close();
    }
}

}
}
}
