#!/usr/bin/python2

from __future__ import absolute_import
from __future__ import print_function

import os
from os.path import dirname, exists, join

from google.protobuf.descriptor_pb2 import *


def get_field_type_name(field):
    if field.HasField('type_name'):
        return field.type_name
    else:
        return [
            None,
            'double',
            'float',
            'int64',
            'uint64',
            'int32',
            'fixed64',
            'fixed32',
            'bool',
            'string',
            'group',
            'message',
            'bytes',
            'uint32',
            'enum',
            'sfixed32',
            'sfixed64',
            'sint32',
            'sint64',
        ][field.type]


def get_field_label(l):
    return [None, 'optional', 'required', 'repeated'][l]


class FileSourceExtractor(object):

    def __init__(self, file_descriptor_proto):
        self._proto = file_descriptor_proto
        self._need_newline = False
        self._continue = False
        self._indent_step = 4
        self._indent = 0

    def _print_raw_option(self, name, value):
        self._print(
            'option',
            name,
            '=',
            value,
            end=';\n'
        )

    def _print_option(self, obj, name, transform=None):
        if obj.HasField(name):
            value = getattr(obj, name)
            if transform is not None:
                value = transform(value)
            self._print_raw_option(name, value)

    def _print_uninterpreted_option(self, option):
        name = []
        for name_part in option.name:
            if name_part.is_extension:
                name.append('({0})'.format(name_part.name_part))
            else:
                name.append(name_part)
        name = '.'.join(name)
        if option.HasField('identifier_value'):
            self._print_raw_option(name, option.identifier_value)
        if option.HasField('positive_int_value'):
            self._print_raw_option(name, option.positive_int_value)
        if option.HasField('negative_int_value'):
            self._print_raw_option(name, option.negative_int_value)
        if option.HasField('double_value'):
            self._print_raw_option(name, option.double_value)
        if option.HasField('string_value'):
            self._print_raw_option(name, '"{0}"'.format(option.string_value))
        if option.HasField('aggregate_value'):
            # TODO
            self._print_raw_option(name, option.aggregate_value)
        self._print_raw_option(name, )

    def _print_uninterpreted_options(self, options):
        for option in options:
            self._print_uninterpreted_option(option)

    def _print_string_option(self, obj, name):
        self._print_option(obj, name, lambda x: '"{0}"'.format(x))

    def _print_bool_option(self, obj, name):
        self._print_option(obj, name, lambda x: 'true' if x else 'false')

    def _print_enum_option(self, obj, name):
        # TODO
        self._print_option(obj, name)

    def _print_file_options(self, options):
        self._print_string_option(options, 'java_package')
        self._print_string_option(options, 'java_outer_classname')
        self._print_bool_option(options, 'java_multiple_files')
        self._print_bool_option(options, 'java_generate_equals_and_hash')
        self._print_enum_option(options, 'optimize_for')
        self._print_string_option(options, 'go_package')
        self._print_bool_option(options, 'cc_generic_services')
        self._print_bool_option(options, 'java_generic_services')
        self._print_bool_option(options, 'py_generic_services')
        self._print_uninterpreted_options(options.uninterpreted_option)
        self._end_section()

    def _print_field(self, field):
        self._print(
            get_field_label(field.label),
            get_field_type_name(field),
            field.name,
            '=',
            field.number,
            end=''
        )
        # TODO extendee
        if field.HasField('default_value'):
            # TODO
            self._print(end='')
        # TODO options
        self._print(';')

    def _print_message(self, message):
        with self._scope_indent('message {0} {{'.format(message.name), '}'):
            for extension in message.extension:
                self._print(extension)
            for nested_type in message.nested_type:
                self._print_message(nested_type)
            for enum_type in message.enum_type:
                self._print_enum(enum_type)
            for field in message.field:
                self._print_field(field)
            for extension_range in message.extension_range:
                # TODO
                self._print(extension_range)
            if message.HasField('options'):
                # TODO
                self._print(message.options)
        self._end_section()

    def _print_enum(self, enum):
        with self._scope_indent('enum {0} {{'.format(enum.name), '}'):
            for value in enum.value:
                self._print(
                    value.name,
                    '=',
                    value.number,
                    end=''
                )
                # TODO options
                self._print(';')
        # TODO options
        self._end_section()

    def _print_service(self, service):
        # TODO
        self._print(service)
        self._end_section()

    def _print_extension(self, extension):
        # TODO
        self._print_extension(extension)
        self._end_section()

    def extract(self, file):
        self._file = file
        if self._proto.HasField('package'):
            self._print('package {0};'.format(self._proto.package))
            self._end_section()

            self._print_file_options(self._proto.options)

            is_public = set(self._proto.public_dependency)
            for i, imp in enumerate(self._proto.dependency):
                self._print('import', end='')
                if i in is_public:
                    self._print(' public', end='')
                self._print(' "{0}";'.format(imp))
            self._end_section()

            for message in self._proto.message_type:
                self._print_message(message)

            for enum in self._proto.enum_type:
                self._print_enum(enum)

            for service in self._proto.service:
                self._print_service(service)

            for extension in self._proto.extension:
                self._print_extension(extension)

            # does not use self._proto.source_code_info

    def _scope_indent(self, open, close):
        this = self

        class ScopeIndent(object):

            def __enter__(self):
                this._print(open)
                this._inc_indent()

            def __exit__(self, type, value, traceback):
                this._dec_indent()
                this._print(close)

        return ScopeIndent()

    def _inc_indent(self):
        self._indent += self._indent_step

    def _dec_indent(self):
        assert self._indent >= self._indent_step
        self._indent -= self._indent_step

    def _print(self, *args, **kwargs):
        if not self._continue:
            if self._need_newline:
                self._need_newline = False
                self._print_new_line()
            self._print_raw(' ' * self._indent, end='')
        self._continue = False
        if kwargs.get('end', '\n').find('\n') == -1:
            self._continue = True
        self._print_raw(*args, **kwargs)

    def _print_new_line(self):
        self._print_raw()

    def _print_raw(self, *args, **kwargs):
        kwargs['file'] = self._file
        print(*args, **kwargs)

    def _end_section(self):
        self._need_newline = True


def extract_source_file(destination, file_descriptor_proto):
    filename = join(destination, file_descriptor_proto.name)
    directory = dirname(filename)
    if not exists(directory):
        os.makedirs(directory)
    with open(filename, 'w') as out_file:
        FileSourceExtractor(
            file_descriptor_proto=file_descriptor_proto).extract(out_file)


def extract_source_tree(destination, file_descriptor_set):
    for fd in file_descriptor_set.file:
        extract_source_file(destination, fd)


def main():
    import argparse

    from . import LogReader

    parser = argparse.ArgumentParser(
        description="Extract google::protobuf source tree from log file."
    )
    parser.add_argument('-o', '--destination',
                        required=True, help='Destination directory')
    parser.add_argument('-l', '--log', required=True, help='Log file')
    args = parser.parse_args()

    with LogReader(args.log) as log_reader:
        proto = log_reader.header.proto

    extract_source_tree(args.destination, proto)


if __name__ == '__main__':
    main()


__all__ = ['extract_source_tree', 'main', 'NonEmptyRootError']
