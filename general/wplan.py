class WPlan(object):
    """docstring for WPlan"""

    def __init__(self, string):
        self.blocks = self.strToBlocks(string)

    def strToBlocks(self, string):
        return string

    def getBlocks(self):
        return self.blocks
