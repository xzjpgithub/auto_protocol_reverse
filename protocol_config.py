class protocol_config:

    def __init__(self):
        # -1 = unknown endian
        #  0 = little endian
        #  1 = big endian
        self.endian = -1

    def set_endian(self, endian):
        self.endian = endian

    def get_endian(self):
        return self.endian
