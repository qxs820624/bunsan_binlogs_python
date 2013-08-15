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
        return 'Header(proto={0!r}, types={1!r})'.format(self._proto, self._types)


class LogReader(object):

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
        return self._log_reader.path

    @property
    def header(self):
        return self._header

    def __repr__(self):
        return repr(self._log_reader)

    def __iter__(self):
        return self

    def next(self):
        next_ = self._log_reader.next()
        descriptor = self._pool.FindMessageTypeByName(next_.type)
        message = self._factory.GetPrototype(descriptor)()
        message.ParseFromString(next_.data)
        return message

    def close(self):
        self._log_reader.close()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()
