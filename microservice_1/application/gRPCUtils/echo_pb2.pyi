from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class emptyParam(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class listMetricsParam(_message.Message):
    __slots__ = ["listMetrics"]
    LISTMETRICS_FIELD_NUMBER: _ClassVar[int]
    listMetrics: str
    def __init__(self, listMetrics: _Optional[str] = ...) -> None: ...

class resultValue(_message.Message):
    __slots__ = ["result"]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: str
    def __init__(self, result: _Optional[str] = ...) -> None: ...

class statsNameParam(_message.Message):
    __slots__ = ["statsName"]
    STATSNAME_FIELD_NUMBER: _ClassVar[int]
    statsName: str
    def __init__(self, statsName: _Optional[str] = ...) -> None: ...
