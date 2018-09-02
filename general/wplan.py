import re


TITLE = re.compile(r'^[^\s\#\[](.*)')
ELEMENT = re.compile(r'^\t([^\t-]+)')
DETAIL = re.compile(r'^\t\t([^\t-]+)')
LIST = re.compile(r'^\t\t-\s([^\t]+)')


class WPlan(object):
    def __init__(self, string):
        self.Blocks = self.strToBlocks(string)
        self.Elements = self.initElements()

    def __delitem__(self, key):
        self.Blocks.__delattr__(key)

    def __getitem__(self, key):
        return self.Blocks.__getattribute__(key)

    def __setitem__(self, key, value):
        self.Blocks.__setattr__(key, value)

    def __iter__(self):
        return iter(self.Blocks)

    def strToBlocks(self, string):
        out = []
        for x in string.split('\n\n'):
            block = WPBlock(x)
            if block is not None:
                out.append(block)
        return out

    def initElements(self):
        out = []
        for x in self.Blocks:
            for e in x.Elements:
                if e not in out:
                    out.append(e)
        return out

    def getTimeSum(self):
        time = 0
        for x in self.Blocks:
            try:
                time += int(x.Elements['Time'])
            except Exception:
                pass
        return self.toTime(time)

    def toTime(self, integer):
        hours = integer // 60
        minutes = integer - (hours * 60)
        return '{}:{:02} h'.format(hours, minutes)


class WPBlock(object):
    def __init__(self, string):
        self.Title = ''
        self.Elements = {}
        self.last = 'undefined'
        self.strToData(string)

        if self.last == 'undefined':
            return None

    def __str__(self):
        out = self.Title
        for x in self.Elements:
            out += '\n  {}: {}'.format(
                x,
                self.Elements[x]
            )
        return out

    def strToData(self, string):
        for x in string.split('\n'):
            if TITLE.match(x):
                self.Title = TITLE.match(x).group(0)
                self.last = 'Title'

            elif ELEMENT.match(x) and self.last != 'undefined':
                self.last = ELEMENT.match(x).group(1)

            elif DETAIL.match(x) and self.last != 'undefined':
                if self.last not in self.Elements:
                    self.Elements[self.last] = ''

                if self.Elements[self.last] == '':
                    self.Elements[self.last] = DETAIL.match(x).group(1)
                else:
                    self.Elements[self.last] += '\n' + DETAIL.match(x).group(1)

            elif LIST.match(x) and self.last != 'undefined':
                if self.last not in self.Elements:
                    self.Elements[self.last] = []
                self.Elements[self.last].append(LIST.match(x).group(1))
