#!/usr/bin/python2

from __future__ import absolute_import

from google.protobuf.descriptor_pb2 import FileDescriptorSet
from google.protobuf.descriptor_pool import DescriptorPool
from google.protobuf.message_factory import MessageFactory

from ._binlogs import LogReader as _LogReader


class Header(object):

    def __init__(self, proto, types):
        self._proto = proto
        self._types = types

    @property
    def proto(self):
        return self._proto

    @proto.setter
    def proto(self, value):
        self._proto = value

    @property
    def types(self):
        return self._types

    @types.setter
    def types(self, value):
        self._types = value

    def __repr__(self):
        return 'Header(proto={0!r}, types={1!r})'.format(
            self._proto, self._types)


class LogItem(object):

    def __init__(self, type, value):
        self._type = type
        self._value = value

    @property
    def type(self):
        """Fully-qualified google.protobuf.Message type name."""
        return self._type

    @property
    def value(self):
        """google.protobuf.Message representing log entry."""
        return self._value

    def __str__(self):
        return '[{0}]\n{1}'.format(self._type, self._value)

    def __repr__(self):
        return 'LogItem(type={0!r}, value={1!r})'.format(
            self._type, self._value)


class LogReader(object):
    """
        File-like interface for binary logs.

        >>> with LogReader("path/to/log/file.gz") as log:
        ...     for item in log.items():
        ...         print(entry.type)
        ...         print(entry.value.some.nested.object)
        ...         print()

        >>> with LogReader("path/to/log/file.gz") as log:
        ...     for value in log.values():
        ...         print(value.some.nested.object)
        ...         print()
    """

    def __init__(self, path):
        self._log_reader = _LogReader(path)
        # header
        header_ = self._log_reader.header
        fd_set = FileDescriptorSet()
        fd_set.ParseFromString(header_.proto)
        self._header = Header(proto=fd_set, types=header_.types)
        # descriptors
        self._pool = DescriptorPool()
        for proto in self._header.proto.file:
            self._pool.Add(proto)
        self._factory = MessageFactory()

    @property
    def path(self):
        """Log path."""
        return self._log_reader.path

    @property
    def header(self):
        """Log header."""
        return self._header

    def __repr__(self):
        return repr(self._log_reader)

    def items(self):
        """Return iterator to log items."""
        this = self

        class Iterator(object):

            def __iter__(self):
                return self

            def next(self):
                return this._next()

        return Iterator()

    def values(self):
        """Return iterator to log values."""
        this = self

        class Iterator(object):

            def __iter__(self):
                return self

            def next(self):
                return this._next().value

        return Iterator()

    def _next(self):
        next_ = self._log_reader.next()
        descriptor = self._pool.FindMessageTypeByName(next_.type)
        value = self._factory.GetPrototype(descriptor)()
        value.ParseFromString(next_.data)
        return LogItem(next_.type, value)

    def read(self):
        """Return None on EOF."""
        try:
            return self._next().value
        except StopIteration:
            return None

    def close(self):
        """Closes LogReader. LogReader will take EOF state."""
        self._log_reader.close()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()
