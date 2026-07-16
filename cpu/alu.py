from typing import Tuple

class ALU:
    """Arithmetic Logic Unit"""

    def __init__(self, width: int = 64):
        self.width = width
        self.mask = (1 << width) - 1

    def add(self, a: int, b: int) -> Tuple[int, bool, bool, bool]:
        """Add two numbers, return (result, carry, overflow, zero)"""
        result = (a + b) & self.mask
        carry = (a + b) > self.mask
        overflow = ((a & (1 << (self.width - 1))) ==
                    (b & (1 << (self.width - 1))) and
                    (result & (1 << (self.width - 1))) !=
                    (a & (1 << (self.width - 1))))
        zero = result == 0
        return result, carry, overflow, zero

    def sub(self, a: int, b: int) -> Tuple[int, bool, bool, bool]:
        """Add two numbers, return (result, carry, overflow, zero)"""
        result = (a - b) & self.mask
        carry = a < b
        overflow = ((a & (1 << (self.width - 1))) ==
                    (b & (1 << (self.width - 1))) and
                    (result & (1 << (self.width - 1))) !=
                    (a & (1 << (self.width - 1))))
        zero = result == 0
        return result, carry, overflow, zero

    def and_op(self, a: int, b: int) -> int:
        return (a & b) & self.mask

    def or_op(self, a: int, b: int) -> int:
        return (a | b) & self.mask

    def xor_op(self, a: int, b: int) -> int:
        return (a ^ b) & self.mask

    def not_op(self, a: int) -> int:
        return (~a) & self.mask

    def shift_left(self, a: int, amount: int) -> int:
        return (a << amount) & (self.mask)

    def shift_right(self, a: int, amount: int, arithmetic: bool = False) -> int:
        if arithmetic:
            # preserve sign bit
            sign = a & (1 << (self.width - 1))
            result = (a >> amount) & self.mask
            if sign:
                result |= (self.mask ^ ((1 << (self.width - amount)) - 1))
            return result
        return (a >> amount) & self.mask

    def compare(self, a: int, b: int) -> Tuple[bool, bool, bool]:
        """Compare two values, return (equal, greater, less)"""
        equal = a == b
        greater = a > b
        less = a < b
        return equal, greater, less