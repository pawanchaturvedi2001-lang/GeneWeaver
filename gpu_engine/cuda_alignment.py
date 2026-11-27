"""CUDA-based sequence alignment."""
import numpy as np
from numba import cuda

from .gpu_memory import (
    encode_sequence,
    allocate_gpu_output
)


@cuda.jit
def dna_alignment_kernel(seq1, seq2, scores, len1, len2):
    """
    CUDA kernel for parallel DNA alignment.

    Each GPU thread calculates the score
    for one alignment offset.
    """

    idx = cuda.grid(1)

    total_offsets = len1 + len2 - 1

    if idx < total_offsets:

        shift = idx - (len2 - 1)

        score = 0

        for i in range(len1):

            j = i - shift

            if j >= 0 and j < len2:

                if seq1[i] == seq2[j]:
                    score += 1

                else:
                    score -= 1

        scores[idx] = score


def align_sequences_gpu(sequence1, sequence2):
    """
    Perform DNA alignment using GPU.
    """

    if not cuda.is_available():
        raise RuntimeError("CUDA GPU is not available")

    seq1 = encode_sequence(sequence1)
    seq2 = encode_sequence(sequence2)

    len1 = len(seq1)
    len2 = len(seq2)

    total_offsets = len1 + len2 - 1

    gpu_seq1 = cuda.to_device(seq1)
    gpu_seq2 = cuda.to_device(seq2)

    gpu_scores = allocate_gpu_output(total_offsets)

    threads_per_block = 128

    blocks_per_grid = (
        total_offsets + threads_per_block - 1
    ) // threads_per_block

    dna_alignment_kernel[
        blocks_per_grid,
        threads_per_block
    ](
        gpu_seq1,
        gpu_seq2,
        gpu_scores,
        len1,
        len2
    )

    scores = gpu_scores.copy_to_host()

    best_index = int(np.argmax(scores))

    best_offset = best_index - (len2 - 1)

    return {
        "best_score": int(scores[best_index]),
        "best_offset": best_offset,
        "all_scores": scores.tolist()
    }