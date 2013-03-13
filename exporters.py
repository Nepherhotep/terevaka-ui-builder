import const
from StringIO import StringIO

__author__ = 'alexey.zankevich'


import const


class LuaExporter(object):
    def export(self, d):
        out = StringIO()
        out.write("return {\n")
        indent = 4
        for key in [const.KEY_LAYOUT_TYPE, const.KEY_LAYOUT_WIDTH,
                    const.KEY_LAYOUT_HEIGHT, const.KEY_LAYOUT_H_ALIGN]:
            if key in d:
                out.write(self.formatKeyValue(key, d[key], indent))
        out.write("%s[\"props\"] = {\n" %(indent * " "))
        props = d[const.KEY_PROPS]
        for i, prop in enumerate(props):
            out.write(self.formatProp(prop, indent + 4))
            if i + 1 < len(props):
                out.write(",\n")
            else:
                out.write("\n")
        out.write("%s}\n" %(indent * " "))
        out.write("}")
        out.seek(0)
        return out.read()

    def formatProp(self, prop, indent):
        s = "%s{\n" %(indent * " ")
        for key, value in prop.items():
            s += self.formatKeyValue(key, value, indent+4)
        s += "%s}" %(indent * " ")
        return s

    def formatBool(self, b):
        return "true" if b else "false"

    def formatString(self, s):
        return '"%s"' %s

    def formatKeyValue(self, key, value, indent):
        if type(value) in (int, float):
            return "%s[\"%s\"] = %s,\n" %(indent * " ", key, value)
        if type(value) == bool:
            return "%s[\"%s\"] = %s,\n" %(indent * " ", key, self.formatBool(value))
        else:
            return "%s[\"%s\"] = %s,\n" %(indent * " ", key, self.formatString(value))

