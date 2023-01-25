from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class AllMetrics(_message.Message):
    __slots__ = ["result"]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: str
    def __init__(self, result: _Optional[str] = ...) -> None: ...

class getAllMetricsParams(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class getMetadataForMetricsParams(_message.Message):
    __slots__ = ["idMetric"]
    IDMETRIC_FIELD_NUMBER: _ClassVar[int]
    idMetric: str
    def __init__(self, idMetric: _Optional[str] = ...) -> None: ...
