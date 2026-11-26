
"""
GeneWeaver GPU Engine

Member 2 - GPU/HPC Engineer
Handles CUDA-based DNA alignment and GPU performance.
"""


def align_sequences_gpu(*args, **kwargs):
    from .cuda_alignment import align_sequences_gpu as gpu_function
    return gpu_function(*args, **kwargs)


__all__ = ["align_sequences_gpu"]
