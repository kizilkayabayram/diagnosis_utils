import string
import textwrap
from .model import ScalarType, MapType, ListType, CfgType

_TEMPLATE = string.Template('''\
#ifndef _${NAMESPACE}__${CLASS_NAME}_H_
#define _${NAMESPACE}__${CLASS_NAME}_H_

#include <$gen_namespace/Config.h>

namespace $namespace
{
class $ClassName : public $gen_namespace::Config
{
public:
  $ClassName()
    : $initialization
  {
  }

  virtual ~$ClassName() = default;

  virtual void load(tug_cfg::ConfigSource& s) override
  {
    $load
    enforceConstraints();
  }

  virtual void enforceConstraints() override
  {
    $enforceConstraints
  }

  $members
};
}  // namespace $namespace

#endif  // _${NAMESPACE}__${CLASS_NAME}_H_
''')


class CppParam(object):
    def __init__(self, param):
        self.name = param.name
        self.type = self._generate_type_name(param.type)
        self.default = self._format_value(param, param.default)
        self.min = self._format_value(param, param.min)
        self.max = self._format_value(param, param.max)
        self.choices = tuple(self._format_value(param, choice) for choice in (param.choices or ()))
        self.suggestions = tuple(self._format_value(param, choice) for choice in (param.suggestions or ()))
        self.description = param.description

    def _generate_type_name(self, type_):
        if isinstance(type_, ScalarType):
            if type_.name == ScalarType.ANY:
                return 'boost::any'
            if type_.name == ScalarType.STR:
                return 'std::string'
            return type_.name
        if isinstance(type_, MapType):
            return 'std::map<%s, %s> ' % (self._generate_type_name(type_.key_type),
                                          self._generate_type_name(type_.value_type))
        if isinstance(type_, ListType):
            return 'std::vector<%s> ' % (self._generate_type_name(type_.item_type),)
        if isinstance(type_, CfgType):
            return '%s::%s' % (type_.package_name, type_.cfg_name)
        raise TypeError('Configuration model contains unknown type %r' % type_)

    def _format_value(self, param, value):
        if value is None:
            return None
        if isinstance(param.type, ScalarType):
            if param.type.name == ScalarType.BOOL:
                return 'true' if value else 'false'
            if param.type.name == ScalarType.STR:
                return '"%s"' % str(value).replace('"', '\\"')
            return repr(value)
        #raise TypeError('Type %r cannot have values' % param.type)
        return None


class Generator(object):
    def generate(self, stream, cfg):
        class_name = cfg.name + 'Config'
        params = list(CppParam(p) for p in cfg.parameters)
        members = []
        initialization = ',\n      '.join('%s(%s)' % (p.name, p.default) for p in params if p.default is not None)
        load = []
        enforce = []
        for p in params:
            members.append('')
            members.append('/**')
            if p.description:
                members.append(textwrap.fill(p.description, initial_indent=' * ', subsequent_indent='   * '))
            if p.default is not None:
                members.append(' * Default: %s' % p.default)
                load.append('s.load("%s", %s, %s);' % (p.name, p.name, p.default))
            else:
                load.append('s.load("%s", %s);' % (p.name, p.name))
            if p.min is not None:
                members.append(' * Minimum: %s' % p.min)
                enforce.append('enforceMin("%s", %s, %s);' % (p.name, p.name, p.min))
            if p.max is not None:
                members.append(' * Maximum: %s' % p.max)
                enforce.append('enforceMax("%s", %s, %s);' % (p.name, p.name, p.max))
            if p.choices:
                enforce.append('enforceChoices("%s", %s, {%s});' % (p.name, p.name, ', '.join(p.choices)))
            members.append(' */')
            members.append('%s %s;' % (p.type.strip(), p.name))
        stream.write(_TEMPLATE.substitute(
            gen_namespace=self.__class__.__module__.split('.')[0],
            NAMESPACE=cfg.package_name.upper(),
            namespace=cfg.package_name,
            CLASS_NAME=class_name.upper(),
            ClassName=class_name,
            members='\n  '.join(members),
            initialization=initialization,
            load='\n    '.join(load),
            enforceConstraints='\n    '.join(enforce),
        ))
