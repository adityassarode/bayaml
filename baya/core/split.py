from __future__ import annotations

from sklearn.model_selection import train_test_split

from ..context import Context


class SplitModule:
    def __init__(self, context: Context) -> None:
        self._ctx = context

    def train_test(self, test_size: float = 0.2) -> "SplitModule":
        df = self._ctx.ensure_dataframe()
        target = self._ctx.ensure_target()
        X = df.drop(columns=[target])
        y = df[target]
        seed = self._ctx.get_seed()
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=seed)
        self._ctx.set_split_data(X_train, X_test, y_train, y_test)
        return self

    def random(self, test_size: float = 0.2) -> "SplitModule":
        return self.train_test(test_size)
