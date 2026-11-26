
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

def test_parse_fasta_detects_duplicate_ids(tmp_path):
    fasta_file = tmp_path / "duplicate.fasta"

    fasta_file.write_text(
        ">gene_001 First sequence\n"
        "ATGC\n"
        ">gene_001 Duplicate sequence\n"
        "TTAA\n",
        encoding="utf-8"
    )

    with pytest.raises(ValueError, match="Duplicate sequence ID"):
        parse_fasta(fasta_file)


def test_parse_fasta_rejects_empty_sequences(tmp_path):
    fasta_file = tmp_path / "empty.fasta"

    fasta_file.write_text(
        ">gene_001 Empty sequence\n"
        ">gene_002 Valid sequence\n"
        "ATGC\n",
        encoding="utf-8"
    )

    with pytest.raises(ValueError, match="Empty sequence"):
        parse_fasta(fasta_file)
