from typing import Optional, TextIO


class DebugWrite:
    """Debug writing utility class."""
    debug_write_instance: Optional['DebugWrite'] = None

    @staticmethod
    def get_instance(fw: Optional[TextIO] = None) -> 'DebugWrite':
        """Get or create a debug write instance."""
        if DebugWrite.debug_write_instance is None:
            DebugWrite.debug_write_instance = DebugWrite(fw)

        fw0 = DebugWrite.debug_write_instance.file_writer

        if fw is not None and fw0 != fw:
            DebugWrite.debug_write_instance = DebugWrite(fw)

        return DebugWrite.debug_write_instance

    def __init__(self, fw: Optional[TextIO]):
        """Initialize debug writer with file writer."""
        self.file_writer: Optional[TextIO] = fw
        self.debug_level: int = 10

    def write(self, text: str, level: int = 0) -> None:
        """Write text if level is within debug level."""
        if self.file_writer is not None and level <= self.debug_level:
            self.file_writer.write(text)
