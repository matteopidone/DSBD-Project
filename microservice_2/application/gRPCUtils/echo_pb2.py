# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: echo.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\necho.proto\x12\x04\x65\x63ho\"!\n\ridMetricParam\x12\x10\n\x08idMetric\x18\x01 \x01(\t\"\x0c\n\nemptyParam\"\x1d\n\x0bresultValue\x12\x0e\n\x06result\x18\x01 \x01(\t\"#\n\x0estatsNameParam\x12\x11\n\tstatsName\x18\x01 \x01(\t2\xbc\x02\n\x0b\x45\x63hoService\x12\x36\n\rgetAllMetrics\x12\x10.echo.emptyParam\x1a\x11.echo.resultValue\"\x00\x12\x41\n\x15getMetadataForMetrics\x12\x13.echo.idMetricParam\x1a\x11.echo.resultValue\"\x00\x12@\n\x14getHistoryForMetrics\x12\x13.echo.idMetricParam\x1a\x11.echo.resultValue\"\x00\x12\x36\n\tsendStats\x12\x14.echo.statsNameParam\x1a\x11.echo.resultValue\"\x00\x12\x38\n\x0bsendMetrics\x12\x14.echo.statsNameParam\x1a\x11.echo.resultValue\"\x00\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'echo_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _IDMETRICPARAM._serialized_start=20
  _IDMETRICPARAM._serialized_end=53
  _EMPTYPARAM._serialized_start=55
  _EMPTYPARAM._serialized_end=67
  _RESULTVALUE._serialized_start=69
  _RESULTVALUE._serialized_end=98
  _STATSNAMEPARAM._serialized_start=100
  _STATSNAMEPARAM._serialized_end=135
  _ECHOSERVICE._serialized_start=138
  _ECHOSERVICE._serialized_end=454
# @@protoc_insertion_point(module_scope)
