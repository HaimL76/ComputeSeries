class DebugWrite:
    debug_write_instance = None

    @staticmethod
    def get_instance(fw=None):
        if DebugWrite.debug_write_instance is None:
            DebugWrite.debug_write_instance = DebugWrite(fw)

        return DebugWrite.debug_write_instance

    def __init__(self, fw):
        self.file_writer = fw

    def write(self, text: str):
        self.file_writer.write(text)
