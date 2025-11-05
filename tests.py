from main import calculate

def approx_equal(a, b, eps=1e-9):
    return abs(a - b) < eps

def run_tests():
    assert calculate(2, 2, "+") == 4
    assert calculate(5, 3, "-") == 2
    assert calculate(3, 4, "*") == 12
    assert approx_equal(calculate(7, 2, "/"), 3.5)

    # Deling på 0
    try:
        calculate(1, 0, "/")
        raise AssertionError("Skulle ha feilet ved deling på 0")
    except ZeroDivisionError:
        pass

    print("Alle tester OK ✅")

if __name__ == "__main__":
    run_tests()
