from __future__ import annotations

import matplotlib.pyplot as plt


class MatplotlibBackend:
    def histogram(self, df, column: str):
        fig, ax = plt.subplots()
        ax.hist(df[column])
        ax.set_title(column)
        return fig
