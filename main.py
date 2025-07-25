import webbrowser

from debug_write import DebugWrite
from exponential import Exponential, ExponentialProduct
from polynomial import Polynomial
from polynomial_rational import PolynomialProductRational, PolynomialSummationRational
from process_file import ProcessFile, ProcessFolder
from series import SeriesProduct, SeriesProductSum
from substitution import VariableSubstitution

import matplotlib.pyplot as plt

const_coefficient: str = "(1-p^{-1})"
coeff: str = const_coefficient


def main():
    pf: ProcessFolder = ProcessFolder(".")

    pf.process_folder(".txt$")

    _ = 0

    pf: ProcessFile = ProcessFile("1.txt")

    pf.process_file()




main()
