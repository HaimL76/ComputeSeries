class DebugWrite:
    debug_write_instance = None

    @staticmethod
    def get_instance(fw=None):
        if DebugWrite.debug_write_instance is None:
            DebugWrite.debug_write_instance = DebugWrite(fw)

        return DebugWrite.debug_write_instance

    def __init__(self, fw):
        self.file_writer = fw
        self.debug_level: int = 0

    def write(self, text: str, level: int = 0):
        if level <= self.debug_level:
            self.file_writer.write(text)
