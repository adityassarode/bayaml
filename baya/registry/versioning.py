class Versioning:
    def bump(self, version: str) -> str:
        parts = version.split('.')
        parts[-1] = str(int(parts[-1]) + 1)
        return '.'.join(parts)
