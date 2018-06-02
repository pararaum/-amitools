from .value import Value, ValueList, ValueDict


class DefaultDict(object):

  def __init__(self, default=None):
    if default is None:
      default = {}
    self._check_default_cfg(default)
    self.default = {}
    self._rebuild_default_cfg(default, self.default)

  def get_cfg(self):
    return self.default

  def gen_dict(self):
    """generate a pure dictionary holding the default values"""
    return self._gen_default_dict(self.default)

  def _gen_default_dict(self, def_cfg):
    res = {}
    for key in def_cfg:
      val = def_cfg[key]
      if type(val) is dict:
        res[key] = self._gen_default_dict(val)
      else:
        res[key] = val.default
    return res

  def merge_cfg(self, mine, other, default=None):
    if default is None:
      default = self.default
    for key in other:
      if key in default:
        self.merge_cfg_key(mine, other, key, default)

  def merge_cfg_key(self, mine, other, key, default=None, def_key=None):
    if default is None:
      default = self.default
    if def_key is None:
      def_key = key
    # create dict if missing
    if key not in mine:
      mine[key] = {}
    oval = other[key]
    dval = default[def_key]
    mval = mine[key]
    if type(dval) is dict:
      # recurse in dict
      if type(oval) is not dict:
        raise ValueError("expected dict key: %s" % key)
      self.merge_cfg(mval, oval, dval)
    else:
      # overwrite my key
      mine[key] = dval.parse(oval)

  def _check_default_cfg(self, cfg):
    t = type(cfg)
    if t in (bool, str, int, Value, ValueList, ValueDict):
      pass
    elif t is dict:
      for key in cfg:
        v = cfg[key]
        self._check_default_cfg(v)
    else:
      raise ValueError("invalid config type: %s for %s" % (t, cfg))

  def _rebuild_default_cfg(self, in_cfg, out_cfg):
    for key in in_cfg:
      val = in_cfg[key]
      t = type(val)
      if t in (bool, int, str):
        # auto wrap in Value
        out_cfg[key] = Value(t, val)
      elif t is dict:
        new_dict = {}
        out_cfg[key] = new_dict
        self._rebuild_default_cfg(val, new_dict)
      elif t in (Value, ValueList, ValueDict):
        out_cfg[key] = val
      else:
        raise ValueError("invalid type in default config: %s" % val)
