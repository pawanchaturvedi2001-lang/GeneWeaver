
"""Tests for GeneWeaver GPU and CPU functionality."""

import pytest

from gpu_engine.gpu_memory import encode_sequence
from gpu_engine.cpu_alignment import align_sequences_cpu


def cuda_available():
    try:
        from numba import cuda
        return cuda.is_available()
    except Exception:
        return False


def test_encode_sequence():
    result = encode_sequence("ATGC")
    assert result.tolist() == [65, 84, 71, 67]


def test_lowercase_sequence():
    result = encode_sequence("atgc")
    assert result.tolist() == [65, 84, 71, 67]


def test_invalid_dna_sequence():
    with pytest.raises(ValueError):
        encode_sequence("ATGX")


def test_empty_sequence():
    with pytest.raises(ValueError):
        encode_sequence("")


def test_cpu_identical_sequences():
    result = align_sequences_cpu("ATGC", "ATGC")
    assert result["best_score"] == 4
    assert result["best_offset"] == 0


def test_cpu_different_sequences():
    result = align_sequences_cpu("AAAA", "TTTT")
    assert result["best_score"] == -1


@pytest.mark.skipif(
    not cuda_available(),
    reason="CUDA GPU is not available"
)
def test_gpu_identical_sequences():
    from gpu_engine.cuda_alignment import align_sequences_gpu

    result = align_sequences_gpu("ATGC", "ATGC")
    assert result["best_score"] == 4
    assert result["best_offset"] == 0


@pytest.mark.skipif(
    not cuda_available(),
    reason="CUDA GPU is not available"
)
def test_gpu_different_sequences():
    from gpu_engine.cuda_alignment import align_sequences_gpu

    result = align_sequences_gpu("AAAA", "TTTT")
    assert result["best_score"] == -1
