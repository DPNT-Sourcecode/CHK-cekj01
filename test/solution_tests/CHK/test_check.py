from solutions.CHK import checkout_solution


class TestCheck():

    def test_illegal_input(self):
        assert checkout_solution.checkout('') == -1