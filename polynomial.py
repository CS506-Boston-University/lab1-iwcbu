class X:
    def __init__(self):
        pass

    def __repr__(self):
        return "X"

    def evaluate(self, x_value):
        # return an Int object containing the numeric value of the variable
        return Int(int(x_value))

    def simplify(self):
        return self


class Int:
    def __init__(self, i):
        self.i = int(i)

    def __repr__(self):
        return str(self.i)

    def evaluate(self, x_value):
        return Int(self.i)

    def simplify(self):
        return self


class Add:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def __repr__(self):
        return repr(self.p1) + " + " + repr(self.p2)

    def evaluate(self, x_value):
        # add the given inputs after evaluating if they're more complex
        a = self.p1.evaluate(x_value)
        b = self.p2.evaluate(x_value)
        return Int(a.i + b.i)

    def simplify(self):
        p1s = self.p1.simplify()
        p2s = self.p2.simplify()

        # constant folding
        if isinstance(p1s, Int) and isinstance(p2s, Int):
            return Int(p1s.i + p2s.i)

        # X + 0 -> X, 0 + X -> X
        if isinstance(p1s, Int) and p1s.i == 0:
            return p2s
        if isinstance(p2s, Int) and p2s.i == 0:
            return p1s

        return Add(p1s, p2s)


class Mul:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def __repr__(self):
        if isinstance(self.p1, Add):
            if isinstance(self.p2, Add):
                return "( " + repr(self.p1) + " ) * ( " + repr(self.p2) + " )"
            return "( " + repr(self.p1) + " ) * " + repr(self.p2)
        if isinstance(self.p2, Add):
            return repr(self.p1) + " * ( " + repr(self.p2) + " )"
        return repr(self.p1) + " * " + repr(self.p2)

    def evaluate(self, x_value):
        # multiplies the 2 inputs after evaluation
        a = self.p1.evaluate(x_value)
        b = self.p2.evaluate(x_value)
        return Int(a.i * b.i)

    def simplify(self):
        p1s = self.p1.simplify()
        p2s = self.p2.simplify()

        # constant folding
        if isinstance(p1s, Int) and isinstance(p2s, Int):
            return Int(p1s.i * p2s.i)

        # X * 0 or 0 * X -> 0
        if (isinstance(p1s, Int) and p1s.i == 0) or (
            isinstance(p2s, Int) and p2s.i == 0
        ):
            return Int(0)

        # X * 1 -> X
        if isinstance(p1s, Int) and p1s.i == 1:
            return p2s
        if isinstance(p2s, Int) and p2s.i == 1:
            return p1s

        return Mul(p1s, p2s)


class Sub:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def __repr__(self):
        # recursive approach to solving with paranthesis
        left = repr(self.p1)
        right = repr(self.p2)
        if isinstance(self.p1, (Add, Sub, Div)):
            left = "( " + left + " )"
        if isinstance(self.p2, (Add, Sub, Mul, Div)):
            right = "( " + right + " )"
        return left + " - " + right

    def evaluate(self, x_value):
        a = self.p1.evaluate(x_value)
        b = self.p2.evaluate(x_value)
        return Int(a.i - b.i)

    def simplify(self):
        p1s = self.p1.simplify()
        p2s = self.p2.simplify()

        # constant folding
        if isinstance(p1s, Int) and isinstance(p2s, Int):
            return Int(p1s.i - p2s.i)

        # X - 0 -> X
        if isinstance(p2s, Int) and p2s.i == 0:
            return p1s

        return Sub(p1s, p2s)


class Div:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def __repr__(self):

        # recursive approach to solving with paranthesis
        left = repr(self.p1)
        right = repr(self.p2)
        if isinstance(self.p1, (Add, Sub, Mul, Div)):
            left = "( " + left + " )"
        if isinstance(self.p2, (Add, Sub, Mul, Div)):
            right = "( " + right + " )"
        return left + " / " + right

    def evaluate(self, x_value):
        a = self.p1.evaluate(x_value)
        b = self.p2.evaluate(x_value)
        # checks if the divisor is 0
        if b.i == 0:
            raise ZeroDivisionError("division by zero in polynomial evaluation")
        return Int(a.i // b.i)

    def simplify(self):
        p1s = self.p1.simplify()
        p2s = self.p2.simplify()

        # constant folding (integer division)
        if isinstance(p1s, Int) and isinstance(p2s, Int):
            if p2s.i == 0:
                raise ZeroDivisionError("division by zero in simplify")
            return Int(p1s.i // p2s.i)

        # X / 1 -> X
        if isinstance(p2s, Int) and p2s.i == 1:
            return p1s

        # 0 / X -> 0 (even if X is not constant, 0 divided by anything is 0)
        if isinstance(p1s, Int) and p1s.i == 0:
            return Int(0)

        return Div(p1s, p2s)


# Original polynomial example
poly = Add(Add(Int(4), Int(3)), Add(X(), Mul(Int(1), Add(Mul(X(), X()), Int(1)))))
print("Original polynomial:", poly)

# Test new Sub and Div classes
print("\n--- Testing Sub and Div classes ---")
try:
    sub_poly = Sub(Int(10), Int(3))
    print("Subtraction:", sub_poly)
except Exception as e:
    print("❌ Subtraction test failed - Sub class not implemented yet:", e)

try:
    div_poly = Div(Int(15), Int(3))
    print("Division:", div_poly)
except Exception as e:
    print("❌ Division test failed - Div class not implemented yet:", e)

# Test evaluation
print("\n--- Testing evaluation ---")
try:
    simple_poly = Add(Sub(Mul(Int(2), X()), Int(1)), Div(Int(6), Int(2)))
    print("Test polynomial:", simple_poly)
    result = simple_poly.evaluate(4)
    print(f"Evaluation for X=4: {result} (type: {type(result).__name__})")
except Exception as e:
    print("❌ Evaluation test failed - evaluate methods not implemented yet:", e)

try:
    original_result = poly.evaluate(2)
    print(f"Original polynomial evaluation for X=2: {original_result}")
except Exception as e:
    print(
        "❌ Original polynomial evaluation failed - evaluate methods not implemented yet:",
        e,
    )

# demonstrate simplify()
print("\n--- Testing simplify ---")
expr = Add(Int(0), X())
print("0 + X simplifies to:", expr.simplify())

expr = Mul(Int(1), Add(Int(2), Int(3)))
print("1 * (2 + 3) simplifies to:", expr.simplify())

expr = Div(Int(6), Int(2))
print("6 / 2 simplifies to:", expr.simplify())

expr = Sub(Int(5), Int(3))
print("5 - 3 simplifies to:", expr.simplify())

# Option to simulate running tests (no external test file available here)
if __name__ == "__main__":
    print("\n💡 Example tests finished.")
