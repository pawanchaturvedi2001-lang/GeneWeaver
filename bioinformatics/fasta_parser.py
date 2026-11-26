
from Bio import SeqIO
from pathlib import Path


def parse_fasta(file_path):
    """
    Read a FASTA file and extract sequence information.

    Args:
        file_path: Path to the FASTA file.

    Returns:
        A list of dictionaries containing sequence IDs,
        descriptions, and sequences.
    """

    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"FASTA file not found: {file_path}")

    if not file_path.is_file():
        raise ValueError(f"Expected a file, received: {file_path}")

    records = []

    try:
        for record in SeqIO.parse(str(file_path), "fasta"):
            sequence = str(record.seq).upper()

            records.append({
                "id": record.id,
                "description": record.description,
                "sequence": sequence
            })

    except Exception as error:
        raise ValueError(f"Unable to parse FASTA file: {error}") from error

    if not records:
        raise ValueError("The FASTA file contains no valid sequences.")

    return records
