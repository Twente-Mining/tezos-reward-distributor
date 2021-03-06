from util.num_utils import floorf

class RoundingCommand:
    def __init__(self, scale):
        self.scale = scale

    def roundDown(self, decimal_num):
        if self.scale:
            return floorf(decimal_num, self.scale)
        else:
            return decimal_num

    def round(self, decimal_num):
        if self.scale:
            return round(decimal_num, self.scale)
        else:
            return decimal_num
