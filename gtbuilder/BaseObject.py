
class BaseObject(object):
    def _write(self, f, fmt, *objs):
        # make sure everything is quoted correctly
        f.write(fmt % tuple(map(self._quote, objs)))

    def _quote(self, t):
        if t is None:
            return ''

        if type(t) is not str:
            return t

        # really should check for all symbols
        if ' ' in t:
            return '"%s"' % t

        return t
