from itertools import zip_longest
from typing import Any, Iterable, Iterator, TypeVar

ONE = True
ZERO = False
Bit = bool

bit_add = {
    (ZERO, ZERO, ZERO): (ZERO, ZERO),
    (ONE, ZERO, ZERO): (ONE, ZERO),
    (ZERO, ONE, ZERO): (ONE, ZERO),
    (ZERO, ZERO, ONE): (ONE, ZERO),
    (ONE, ONE, ZERO): (ZERO, ONE),
    (ONE, ZERO, ONE): (ZERO, ONE),
    (ZERO, ONE, ONE): (ZERO, ONE),
    (ONE, ONE, ONE): (ONE, ONE),
}


class BitString:
    def __init__(self, sequence: Iterable[Bit]):
        # Make a new, immutable, copy of input sequence, so there's
        # no spooky action-at-a-distance by mutation.
        # Also ensures that BitString is multiply iterable.
        # This propety should never need to be accessed outside of this module.
        self._bits = tuple(sequence)

    def __iter__(self) -> Iterator[Bit]:
        """
        Iterating over a bitstring yields the individual bits.
        """
        yield from self._bits


IntTypeVar = TypeVar("IntTypeVar", bound="Integer")


class Integer(BitString):
    """
    A bitstring representing an integer. The sequence used to initialise the integer
    is interpreted as having it's least-significant digit *first*, and it's most
    significant digit *last*. Iterating over the bitstring will yield bits in that order --
    i.e., from least to most significant.
    """

    def __eq__(bits1: IntTypeVar, bits2: Any) -> bool:
        """
        Two bitstring integers are here defined as equal iff every bit up to the
        most significant ONE is equal. Different numbers of ZEROS after
        that make no difference.
        """
        if not type(bits1) == type(bits2):
            return False
        for bit1, bit2 in zip_longest(bits1, bits2, fillvalue=ZERO):
            if bit1 != bit2:
                return False
        return True

    def __add__(bits1: IntTypeVar, bits2: IntTypeVar) -> IntTypeVar:
        """
        Return new bitstring representing sum of bits1 and bits2, modulo 2^w, where
        w is the width of the wider of bits1 and bits2.
        """
        # None of this dodgy type-casting between binary and twos-compliment.
        if type(bits1) != type(bits2):
            raise ValueError(
                f"Summands must be of same type. Left summand has type {type(bits1)}; tight summand has type {type(bits2)}."
            )
        return_val = []
        carry = ZERO
        # The `zip_longest` implicitly casts the shorter bitstring to the same
        # size as the longer bitstring by padding with ZEROs
        for bit1, bit2 in zip_longest(bits1, bits2, fillvalue=ZERO):
            next_digit, carry = bit_add[(bit1, bit2, carry)]
            return_val.append(next_digit)
        return type(bits1)(return_val)

    def __lshift__(self: IntTypeVar, shift: IntTypeVar) -> IntTypeVar:
        """
        Return new bitstring made by shifting `self`'s bits in the more-significant
        direction by `shift`-many steps. Width of return value is the same as width
        of `self`; if `shift` is greater than the width of `self`, the result will be
        an all ZERO bitstring.
        """
        self_iter = iter(self)
        return_seq = [ZERO for _ in zip(self_iter, shift.count_iter())]
        for _, bit in zip(self_iter, self):
            return_seq.append(bit)
        return type(self)(return_seq)

    def __str__(self: "Integer") -> str:
        """
        String representation uses `1` for ONE and `0` for ZERO values.

        Order is `reverse`d because the standard convention is to write out bitstrings
        with the most significant digit on the left, and the least on the right, whereas
        the standard way of writing out sequences is first element on the left and last on
        the right. These two conventions clash here, because the first element in our integers
        are the least significant, and the last the most.
        """
        bits_in_ints = ["1" if bit else "0" for bit in self]
        bits_in_ints.reverse()
        return "".join(bits_in_ints)

    def count_iter(self: IntTypeVar) -> Iterator[IntTypeVar]:
        increment = type(self)([ONE])

        count = type(self)([ZERO for _ in self._bits])
        while True:
            if count == self:
                break
            else:
                yield count
                count += increment


class BinaryInt(Integer):
    ...


class TwosComplimentInt(Integer):
    ...
