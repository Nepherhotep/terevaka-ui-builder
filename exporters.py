import const
from StringIO import StringIO

__author__ = 'alexey.zankevich'


class LuaExporter(object):
    def export(self, d):
        out = StringIO()
        out.write("return {\n")
        for prop in d[const.KEY_PROPS]:
            out.write(self.formatProp(prop))
            out.write(",\n")
        out.seek(0)
        return out.read()

    def formatProp(self, prop):
        s = "   {"
        for key, value in prop.items():
            s += self.formatKeyValue(key, value)
        s += "  }"
        return s

    def formatBool(self, b):
        return "true" if b else "false"

    def formatString(self, s):
        return '"%s"' %s

    def formatKeyValue(self, key, value):
        if type(value) in (int, float):
            return "    [\"%s\"] = %s,\n" %(key, value)
        if type(value) == bool:
            return "    [\"%s\"] = %s,\n" %(key, self.formatBool(value))
        else:
            return "    [\"%s\"] = %s,\n" %(key, self.formatString(value))

