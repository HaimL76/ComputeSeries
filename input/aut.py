import sympy

def main():
    sympy.init_printing(use_latex=True)
    a11, a21, a22, a33 = sympy.symbols('a11 a21 a22 a33')
    b11, b12, b21, b22, b31, b41 = sympy.symbols('b11 b12 b21 b22 b31 b41')
    
    c1, c2, c3, c4 = sympy.symbols('c1 c2 c3 c4')
    g1, g2, g3, g4 = sympy.symbols('g1 g2 g3 g4')
    d1, d2, d3, d4 = sympy.symbols('d1 d2 d3 d4')
    d13, d24, d35, d14, d25, d15 = sympy.symbols('d13 d24 d35 d14 d25 d15')
    e1, e2, e3, e4 = sympy.symbols('e1 e2 e3 e4')
    e13, e24, e35, e14, e25, e15 = sympy.symbols('e13 e24 e35 e14 e25 e15')

    X1,X2,X3,X4 = sympy.symbols('X1 X2 X3 X4')
    X13,X24,X35 = sympy.symbols('X13 X24 X35')
    X14,X25,X15 = sympy.symbols('X14 X25 X15')

    Y1,Y2,Y3,Y4 = sympy.symbols('Y1 Y2 Y3 Y4')
    Y13,Y24,Y35 = sympy.symbols('Y13 Y24 Y35')
    Y14,Y25,Y15 = sympy.symbols('Y14 Y25 Y15')


    a1, a2, a3, a4 = sympy.symbols('a1 a2 a3 a4')
    a13, a24, a35 = sympy.symbols('a13 a24 a35')
    a14, a25, a15 = sympy.symbols('a14 a25 a15')
    
    b1, b2, b3, b4 = sympy.symbols('b1 b2 b3 b4')
    b13, b24, b35 = sympy.symbols('b13 b24 b35')
    b14, b25, b15 = sympy.symbols('b14 b25 b15')
    
    z1, z2, z3, z4 = sympy.symbols('z1 z2 z3 z4')
    z13, z24, z35 = sympy.symbols('z13 z24 z35')
    z14, z25, z15 = sympy.symbols('z14 z25 z15')
    #b2 = c*a2
    alpha = sympy.symbols('alpha')

    #sympy.solve(eq13, b1, b2)

    #print(f"b1={b1}, b2={b2}, b3={b3}, b4={b4}")

    #return

    N=sympy.Matrix(
        [
            [1, 0, 0, 0, a11,   0,      0,      b11,        b12,            c1],
            [0, 1, 0, 0, a21,   a22,    0,      a21*a22,    b22,            c2],
            [0, 0, 1, 0, 0,     -a11,   a33,    b31,        -a11*a33,       c3],
            [0, 0, 0, 1, 0,     0,      -a22,   b41,        a11*a22-b11,    c4],
            [0, 0, 0, 0, 1,     0,      0,      a22,        0,              b22],
            [0, 0, 0, 0, 0,     1,      0,      a21,        a33,            a21*a33],
            [0, 0, 0, 0, 0,     0,      1,      0,          -a11,           b31],
            [0, 0, 0, 0, 0,     0,      0,      1,          0,              a33],
            [0, 0, 0, 0, 0,     0,      0,      0,          1,              a21],
            [0, 0, 0, 0, 0,     0,      0,      0,          0,              1],
        ])

    H=sympy.Matrix(
        [
            [g1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, g2, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, g3, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, g4, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, g1*g2, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, g2*g3, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, g3*g4, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, g1*g2*g3, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, g2*g3*g4, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, g1*g2*g3*g4]
        ])
    
    #x=sympy.Matrix([d1*e1, d2*e2, d3*e3, d4*e4, d13*e13, d24*e24, d35*e35, d14*e14, d25*e25, d15*e15])

    M=N*H
    sympy.pprint(f"M={M}")

    return

    x=sympy.Matrix([[X1, 0, 0, 0, 0, 0, 0, 0, 0, 0]])

    x=sympy.transpose(x)

    print(f"x={x}")

    return

    for i in range(10):
        Mx = M*x
        print(f"Mx[{i}]={Mx}")
        x = Mx

    y=sympy.Matrix([[Y1, 0, Y3, Y4, Y13, 0, Y35, Y14, 0, 0]])

    

if __name__ == "__main__":    
    main()