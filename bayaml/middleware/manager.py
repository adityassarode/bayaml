class MiddlewareManager:
    def __init__(self) -> None:
        self._items = []

    def use(self, middleware) -> None:
        self._items.append(middleware)

    def before_all(self, context) -> None:
        for item in self._items:
            item.before(context)

    def after_all(self, context) -> None:
        for item in reversed(self._items):
            item.after(context)
