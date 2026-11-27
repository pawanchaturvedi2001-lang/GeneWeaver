
"""GeneWeaver CPU and GPU alignment benchmarking."""

import time
from .cpu_alignment import align_sequences_cpu


def run_benchmark(sequence1, sequence2):

    # CPU benchmark
    start = time.perf_counter()

    cpu_result = align_sequences_cpu(
        sequence1,
        sequence2
    )

    cpu_time = time.perf_counter() - start

    print("\n========== GeneWeaver Benchmark ==========")
    print("CPU Result:", cpu_result)
    print(f"CPU Time: {cpu_time:.6f} seconds")

    # Import CUDA only when GPU benchmarking is requested
    try:
        from numba import cuda

        if not cuda.is_available():
            raise RuntimeError("CUDA GPU is not available")

        from .cuda_alignment import align_sequences_gpu

        # GPU warm-up
        align_sequences_gpu(sequence1, sequence2)
        cuda.synchronize()

        # GPU benchmark
        start = time.perf_counter()

        gpu_result = align_sequences_gpu(
            sequence1, sequence2
        )

        cuda.synchronize()
        gpu_time = time.perf_counter() - start

        speedup = cpu_time / gpu_time if gpu_time > 0 else 0

        print("GPU Result:", gpu_result)
        print(f"GPU Time: {gpu_time:.6f} seconds")
        print(f"Speedup: {speedup:.2f}x")

        return {
            "cpu_time": cpu_time,
            "gpu_time": gpu_time,
            "speedup": speedup,
            "cpu_result": cpu_result,
            "gpu_result": gpu_result,
            "gpu_available": True
        }

    except Exception as error:
        print("\nGPU benchmark skipped:", error)
        print("CPU benchmark completed successfully.")
        print("==========================================")

        return {
            "cpu_time": cpu_time,
            "cpu_result": cpu_result,
            "gpu_available": False
        }


if __name__ == "__main__":

    dna1 = "ATGCGTACGTAG"
    dna2 = "ATGCGTACGTAG"

    run_benchmark(dna1, dna2)

