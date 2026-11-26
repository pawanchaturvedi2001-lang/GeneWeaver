
from pathlib import Path

import pytest

from bioinformatics.fasta_parser import parse_fasta


# Locate the sample FASTA file
SAMPLE_FASTA = Path(__file__).parent / "data" / "sample.fasta"


def test_parse_fasta_returns_three_records():
    records = parse_fasta(SAMPLE_FASTA)

    assert len(records) == 3


def test_parse_fasta_extracts_sequence_ids():
    records = parse_fasta(SAMPLE_FASTA)

    assert [record["id"] for record in records] == [
        "gene_001",
        "gene_002",
        "gene_003"
    ]


def test_parse_fasta_extracts_sequences():
    records = parse_fasta(SAMPLE_FASTA)

    assert [record["sequence"] for record in records] == [
        "ATGCCTAG",
        "TTGGCCAA",
        "ATATCGCG"
    ]


def test_parse_fasta_extracts_descriptions():
    records = parse_fasta(SAMPLE_FASTA)

    assert records[0]["description"] == "gene_001 Human gene"


def test_parse_fasta_file_not_found():
    with pytest.raises(FileNotFoundError):
        parse_fasta("missing_file.fasta")
