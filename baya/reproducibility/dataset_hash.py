from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Final
import pandas as pd


CHUNK_SIZE: Final[int] = 1024 * 1024


# =====================================================
# File Hashing
# =====================================================

def hash_file(path: Path) -> str:
    """
    Deterministic file hash (streaming).
    """

    sha = hashlib.sha256()

    with path.open("rb") as f:
        while True:
            chunk = f.read(CHUNK_SIZE)
            if not chunk:
                break
            sha.update(chunk)

    return sha.hexdigest()


# =====================================================
# DataFrame Hashing (Deterministic)
# =====================================================

def hash_dataframe(df: pd.DataFrame) -> str:
    """
    Deterministic dataset hash.

    Guarantees:
        - Stable column ordering
        - Stable row ordering
        - Normalized line endings
        - Index included
        - Float precision fixed
    """

    if df is None:
        raise ValueError("Cannot hash None DataFrame.")

    # 1️⃣ Freeze column order
    df_sorted_cols = df.reindex(sorted(df.columns), axis=1)

    # 2️⃣ Freeze row order deterministically
    df_sorted = df_sorted_cols.sort_index()

    # 3️⃣ Stable CSV serialization
    csv_bytes = df_sorted.to_csv(
        index=True,
        float_format="%.12g",  # stable float precision
        line_terminator="\n",
    ).encode("utf-8")

    return hashlib.sha256(csv_bytes).hexdigest()