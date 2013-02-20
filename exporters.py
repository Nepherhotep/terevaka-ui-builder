import const
from StringIO import StringIO

__author__ = 'alexey.zankevich'


class LuaExporter(object):
    def export(self, d):
        out = StringIO()
        out.write("return {\n")
        props = d[const.KEY_PROPS]
        for i, prop in enumerate(props):
            out.write(self.formatProp(prop))
            if i + 1 < len(props):
                out.write(",\n")
            else:
                out.write("\n")
        out.write("}")
        out.seek(0)
        return out.read()

    def formatProp(self, prop):
        s = "    {\n"
        for key, value in prop.items():
            s += self.formatKeyValue(key, value)
        s += "    }"
        return s

    def formatBool(self, b):
        return "true" if b else "false"

    def formatString(self, s):
        return '"%s"' %s

    def formatKeyValue(self, key, value):
        if type(value) in (int, float):
            return "        [\"%s\"] = %s,\n" %(key, value)
        if type(value) == bool:
            return "        [\"%s\"] = %s,\n" %(key, self.formatBool(value))
        else:
            return "        [\"%s\"] = %s,\n" %(key, self.formatString(value))

