def argsort(seq, dtype, desc: bool = False) -> list[int]:
    # http://stackoverflow.com/questions/3071415/efficient-method-to-calculate-the-rank-vector-of-a-list-in-python
    # return sorted(range(len(seq)), key=seq.__getitem__, reverse=desc)
    # Nones should be in the end
    return sorted(
        range(len(seq)),
        key=lambda x: seq[x] if seq[x] is not None else dtype(),
        reverse=desc,
    )


def sorted_by_pattern(seq: list, pattern: list) -> list:
    s = sorted(zip(pattern, seq), key=lambda x: x[0])
    return [x[1] for x in s]
