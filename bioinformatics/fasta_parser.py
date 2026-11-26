
from Bio import SeqIO
from pathlib import Path


def parse_fasta(file_path):
    """
    Read a FASTA file and extract sequence information.

    Supports multiple FASTA records and validates sequence IDs
    and empty sequences.
    """

    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"FASTA file not found: {file_path}")

    if not file_path.is_file():
        raise ValueError(f"Expected a file, received: {file_path}")

    records = []
    seen_ids = set()

    try:
        for record in SeqIO.parse(str(file_path), "fasta"):

            sequence_id = record.id
            sequence = str(record.seq).upper()

            # Check for duplicate sequence IDs
            if sequence_id in seen_ids:
                raise ValueError(
                    f"Duplicate sequence ID found: {sequence_id}"
                )

            # Check for empty sequences
            if not sequence:
                raise ValueError(
                    f"Empty sequence found for ID: {sequence_id}"
                )

            seen_ids.add(sequence_id)

            records.append({
                "id": sequence_id,
                "description": record.description,
                "sequence": sequence
            })

    except ValueError:
        raise

    except Exception as error:
        raise ValueError(
            f"Unable to parse FASTA file: {error}"
        ) from error

    if not records:
        raise ValueError(
            "The FASTA file contains no valid sequences."
        )

    return records
