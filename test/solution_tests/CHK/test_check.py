from solutions.CHK import checkout_solution


class TestCheck():

    def test_empty_basket(self):
        assert checkout_solution.checkout('') == 0

    def test_non_string_input(self):
        assert checkout_solution.checkout(1) == -1

    def test_unrecognised_sku_present(self):
        assert checkout_solution.checkout('ABZ') == -1

    def test_single_item(self):
        assert checkout_solution.checkout('A') == 50

    def test_no_special_offers_met(self):
        assert checkout_solution.checkout('ABC') == 100

    def test_special_offer(self):
        assert checkout_solution.checkout('AAA') == 130

    def test_special_offer_hits_multiple_times(self):
        assert checkout_solution.checkout('AAAAAAA') == 310
