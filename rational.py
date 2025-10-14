import math
from typing import List


class Rational:
    primes: List[int] = [2, 3, 5, 7, 11]

    def reduce(self) -> None:
        """Reduce the rational number to its simplest form."""
        if self.denominator == 0:
            raise ValueError("Denominator cannot be zero")
        
        # Handle zero case
        if self.numerator == 0:
            self.denominator = 1
            return
            
        # Handle negative denominator - move sign to numerator
        if self.denominator < 0:
            self.numerator = -self.numerator
            self.denominator = -self.denominator

        # Find GCD and reduce
        gcd_value = self._gcd(abs(self.numerator), abs(self.denominator))
        self.numerator = self.numerator // gcd_value
        self.denominator = self.denominator // gcd_value

    def _gcd(self, a: int, b: int) -> int:
        """Calculate greatest common divisor using Euclidean algorithm."""
        while b:
            a, b = b, a % b
        return a

    def __init__(self, numer: int, denom: int = 1):
        """Initialize a rational number with numerator and denominator."""
        if denom == 0:
            raise ValueError("Denominator cannot be zero")
        self.numerator: int = numer
        self.denominator: int = denom
        self.reduce()

    def __gt__(self, other: 'Rational') -> bool:
        """Compare if this rational is greater than other."""
        if not isinstance(other, Rational):
            return NotImplemented
        return self.numerator * other.denominator > other.numerator * self.denominator

    def is_minus(self) -> bool:
        """Check if the rational number is negative."""
        return self.numerator * self.denominator < 0

    @staticmethod
    def parse(text: str) -> 'Rational':
        """Parse a string representation of a rational number."""
        if not text or not text.strip():
            return Rational(0, 1)
            
        text = text.strip()
        parts: List[str] = text.split("/")

        if len(parts) == 1:
            if parts[0].isnumeric():
                return Rational(int(parts[0]), 1)
            else:
                raise ValueError(f"Invalid rational number format: {text}")
        elif len(parts) == 2:
            if parts[0].isnumeric() and parts[1].isnumeric():
                return Rational(int(parts[0]), int(parts[1]))
            else:
                raise ValueError(f"Invalid rational number format: {text}")
        else:
            raise ValueError(f"Invalid rational number format: {text}")

    def __add__(self, other: 'Rational') -> 'Rational':
        """Add two rational numbers."""
        if not isinstance(other, Rational):
            return NotImplemented
        denom: int = self.denominator * other.denominator
        numer1: int = self.numerator * other.denominator
        numer2: int = other.numerator * self.denominator
        return Rational(numer=numer1 + numer2, denom=denom)

    def __abs__(self) -> 'Rational':
        """Return absolute value of the rational number."""
        return Rational(numer=abs(self.numerator), denom=abs(self.denominator))

    def __sub__(self, other: 'Rational') -> 'Rational':
        """Subtract two rational numbers."""
        if not isinstance(other, Rational):
            return NotImplemented
        minus_other: Rational = Rational(numer=other.numerator * -1, denom=other.denominator)
        return self + minus_other

    def __mul__(self, other: 'Rational') -> 'Rational':
        """Multiply two rational numbers."""
        if not isinstance(other, Rational):
            return NotImplemented
        return Rational(numer=self.numerator * other.numerator, denom=self.denominator * other.denominator)

    def __eq__(self, other: object) -> bool:
        """Check equality of two rational numbers."""
        if not isinstance(other, Rational):
            return NotImplemented
        return self.numerator == other.numerator and self.denominator == other.denominator

    def __str__(self) -> str:
        """String representation of the rational number."""
        return self.get_ltx_str()

    def get_ltx_str(self) -> str:
        """Get LaTeX string representation."""
        s: str = f"{self.numerator}"
        if self.denominator != 1:
            s = f"\\frac{{{s}}}{{{self.denominator}}}"
        return s

    def get_str(self) -> str:
        """Get string representation."""
        s: str = f"{self.numerator}"
        if self.denominator != 1:
            s = f"{s}/{self.denominator}"
        return s
