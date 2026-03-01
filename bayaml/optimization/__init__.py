from .batching import batch
from .gpu_detection import gpu_available
from .lazy_evaluation import lazy
from .parallel_executor import parallel_map

__all__ = ["gpu_available", "parallel_map", "lazy", "batch"]
