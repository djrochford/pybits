from typing import Sequence

import pytest

from arithmetic import ONE, ZERO, BinaryInt, Bit


def test_iter() -> None:
    init_sequence = [ONE, ZERO, ONE, ONE, ZERO]
    bitstring = BinaryInt(init_sequence)
    for i, (bit1, bit2) in enumerate(zip(init_sequence, bitstring)):
        assert bit1 is bit2, (
            "Iterating through BinaryInt and equivalent sequence "
            f"yields different resuts in poisition {i}"
        )


equals_test_data = [
    ([ONE, ZERO, ONE, ONE, ZERO], [ONE, ZERO, ONE, ONE, ZERO], True),
    ([ONE, ZERO, ONE, ONE, ZERO], [ONE, ZERO, ONE, ONE], True),
    ([ONE, ZERO, ONE, ONE, ZERO], [ONE, ZERO, ONE, ONE, ZERO, ZERO], True),
    ([ONE, ZERO, ONE, ONE, ZERO], [ONE, ZERO, ONE, ONE, ZERO, ONE], False),
    ([ONE, ZERO, ONE, ONE, ZERO], [ONE, ZERO, ONE, ONE, ONE], False),
    ([ONE, ZERO, ONE, ONE, ZERO], [ONE, ZERO, ONE], False),
]


@pytest.mark.parametrize(["bits1", "bits2", "expected"], equals_test_data)
def test_equal(bits1: Sequence[Bit], bits2: Sequence[Bit], expected: bool) -> None:
    assert (BinaryInt(bits1) == BinaryInt(bits2)) is expected


add_test_data = [
    ([ZERO, ZERO, ONE, ONE, ZERO], [ZERO, ONE, ZERO, ONE, ZERO], [ZERO, ONE, ONE, ZERO, ONE]),
    ([ZERO, ZERO, ONE, ONE, ZERO], [ZERO, ONE, ZERO, ONE], [ZERO, ONE, ONE, ZERO, ONE]),
    ([ONE, ONE, ONE, ONE], [ONE, ONE, ONE, ONE], [ZERO, ONE, ONE, ONE]),
    ([ONE, ONE, ONE, ONE], [ONE, ONE, ONE, ONE, ZERO], [ZERO, ONE, ONE, ONE, ONE]),
]


@pytest.mark.parametrize(["bits1", "bits2", "sum"], add_test_data)
def test_add(bits1: Sequence[Bit], bits2: Sequence[Bit], sum: Sequence[Bit]) -> None:
    assert BinaryInt(bits1) + BinaryInt(bits2) == BinaryInt(sum)
