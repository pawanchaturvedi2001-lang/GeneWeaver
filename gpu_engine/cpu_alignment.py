"""CPU-based sequence alignment."""

import numpy as np


def align_sequences_cpu(sequence1, sequence2):

    seq1 = np.array([ord(c) for c in sequence1], dtype=np.uint8)
    seq2 = np.array([ord(c) for c in sequence2], dtype=np.uint8)

    len1 = len(seq1)
    len2 = len(seq2)

    total_offsets = len1 + len2 - 1

    scores = np.zeros(total_offsets, dtype=np.int32)

    for idx in range(total_offsets):

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

    best_index = int(np.argmax(scores))
    best_offset = best_index - (len2 - 1)

    return {
        "best_score": int(scores[best_index]),
        "best_offset": best_offset,
        "all_scores": scores.tolist()
    }
