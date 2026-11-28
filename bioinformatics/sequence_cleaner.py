
def clean_dna_sequence(sequence):
    """
    Clean and validate a DNA sequence.

    Converts the sequence to uppercase, removes whitespace,
    and checks for valid DNA nucleotide characters.

    Valid characters: A, T, G, C, N
    """

    if not isinstance(sequence, str):
        raise TypeError("DNA sequence must be a string.")

    # Convert to uppercase and remove whitespace
    cleaned_sequence = "".join(sequence.split()).upper()

    if not cleaned_sequence:
        raise ValueError("DNA sequence cannot be empty.")

    # Check for invalid nucleotide characters
    valid_nucleotides = set("ATGCN")

    invalid_characters = set(cleaned_sequence) - valid_nucleotides

    if invalid_characters:
        raise ValueError(
            f"Invalid DNA characters found: {sorted(invalid_characters)}"
        )

    return cleaned_sequence
