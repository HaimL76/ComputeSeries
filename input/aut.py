import sympy

def main():
    sympy.init_printing(use_latex=True)

    b1, b2, b3, b4 = sympy.symbols('b1 b2 b3 b4')
    b13, b24, b35 = sympy.symbols('b13 b24 b35')

    b13=b24=b35=0

    a1, a2, a3, a4 = sympy.symbols('a1 a2 a3 a4')
    a13, a24, a35 = sympy.symbols('a13 a24 a35')
    a14, a25, a15 = sympy.symbols('a14 a25 a15')

    a2 = a1*b2/b1
    a3 = a1*b3/b1
    a4 = a1*b4/b1

    a24=a13*b3/b1
    a35=a13*(b4*b3)/(b2*b1)

    z13=b1*a2-b2*a1
    z24=b2*a3-b3*a2
    z35=b3*a4-b4*a3
    z14=b1*a24-b24*a1+b13*a3-b3*a13
    z25=b2*a35-b35*a2+b24*a4-b4*a24

    print(f"a2={a2}, a3={a3}, a4={a4}, a24={a24}, a35={a35}")
    print(f"z13={z13}, z24={z24}, z35={z35}, z14={z14}, z25={z25}")

    return


























    
    a11, a21, a22, a33 = sympy.symbols('a11 a21 a22 a33')
    
    c1, c2, c3, c4 = sympy.symbols('c1 c2 c3 c4')
    g1, g2, g3, g4 = sympy.symbols('g1 g2 g3 g4')
    d1, d2, d3, d4 = sympy.symbols('d1 d2 d3 d4')
    d13, d24, d35, d14, d25, d15 = sympy.symbols('d13 d24 d35 d14 d25 d15')
    e1, e2, e3, e4 = sympy.symbols('e1 e2 e3 e4')
    e13, e24, e35, e14, e25, e15 = sympy.symbols('e13 e24 e35 e14 e25 e15')



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


    #sympy.solve(eq13, b1, b2)

    #print(f"b1={b1}, b2={b2}, b3={b3}, b4={b4}")

    #return

    A1=sympy.Matrix(
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

    A2=sympy.Matrix(
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

    A=A1*A2
    #sympy.pprint(f"A={A}")

    B=A.inv()

    C1=A*B
    C2=B*A
    #print(C1)
    #print(C2)

    #print(B)

    x=sympy.Matrix([[d1, d2, d3, d4, d13, d24, d35, d14, d25, d15]])

    x0 = x*A

    #print(x0)

    x1=x0*B

    #x0 = x0.transpose()

    #sympy.pprint(x0)
    #sympy.pprint(f"x0={x0}")

    eq13 = a1*b2-a2*b1
    eq24 = a2*b3-a3*b2
    eq35 = a3*b4-a4*b3
    eq14 = a1*b24-a24*b1+a13*b3-a3*b13
    eq25 = a2*b35-a35*b2+a24*b4-a4*b24
    eq15 = a1*b25-a25*b1+a13*b35-a35*b13+a14*b4-a4*b14

    k = sympy.symbols('k')

    z1 = k * z1
    z2 = k * z2
    z3 = k * z3
    z4 = k * z4
    z13 = k * z13
    z24 = k * z24
    z35 = k * z35
    z14 = k * z14
    z25 = k * z25
    z15 = k * z15

    eqq13 = b1*z2-b2*z1
    eqq24 = b2*z3-b3*z2
    eqq35 = b3*z4-b4*z3
    eqq14 = b1*z24-b24*z1+b13*z3-b3*z13
    eqq25 = b2*z35-b35*z2+b24*z4-b4*z24
    eqq15 = b1*z25-b25*z1+b13*z35-b35*z13+b14*z4-b4*z14

    eeq1 = z2 - k*a2
    eeq2 = z24 - k*a24
    eeq3 = z25 - k*a25

    eqs = [eq13, eq24, eq35, 
           eqq13, eqq24, eqq35]

    solution = sympy.solve(eqs)#, [b1, b2, b3, b4])

    print(f"solution={solution}")

    #print(A.shape)
    #print(x.shape)
    #print(x0.shape)
    #print(x1.shape)

if __name__ == "__main__":    
    main()