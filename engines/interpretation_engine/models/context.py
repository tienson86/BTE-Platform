class InterpretationContext:
    def __init__(self, bazi_result=None, **kwargs):
        self.bazi_result = bazi_result
        self._data = dict(kwargs)

    def set(self, key, value): self._data[key] = value
    def get(self, key, default=None): return self._data.get(key, default)
    def update(self, values): self._data.update(values)
    def resolve(self, path, default=None):
        value = self._data
        for part in path.split("."):
            value = value.get(part, default) if isinstance(value, dict) else getattr(value, part, default)
            if value is default: return default
        return value
