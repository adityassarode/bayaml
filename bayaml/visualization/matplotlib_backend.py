from __future__ import annotations

import matplotlib.pyplot as plt


class MatplotlibBackend:
    def histogram(self, df, column: str):
        fig, ax = plt.subplots()
        ax.hist(df[column])
        ax.set_title(column)
        return fig

    def scatter(self, df, x: str, y: str):
        fig, ax = plt.subplots()
        ax.scatter(df[x], df[y])
        ax.set_xlabel(x)
        ax.set_ylabel(y)
        ax.set_title(f"{x} vs {y}")
        return fig
