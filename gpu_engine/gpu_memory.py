import numpy as np


def encode_sequence(sequence):
    """
    Convert DNA sequence into numerical values.
    """

    sequence = sequence.upper()

    valid_bases = set("ATGC")

    if not sequence:
        raise ValueError("DNA sequence cannot be empty")

    if not set(sequence).issubset(valid_bases):
        raise ValueError("Invalid DNA sequence")

    return np.frombuffer(
        sequence.encode("ascii"),
        dtype=np.uint8
    )


if __name__ == "__main__":

    dna = "ATGC"

    result = encode_sequence(dna)

    print("Original DNA:", dna)
    print("Numerical DNA:", result)
    print("Data Type:", result.dtype)
    print("Sequence Length:", len(result))
    print("GPU MEMORY FILE STARTED")