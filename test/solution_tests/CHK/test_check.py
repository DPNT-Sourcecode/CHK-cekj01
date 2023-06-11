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

    def test_best_special_offer_used(self):
        """
        When multiple special offers are available, expect the one for the highest number
        of items to be applied first
        """
        # Applies the discount for 5, not 3
        assert checkout_solution.checkout(5 * 'A') == 200

    def test_special_offer_hits_multiple_times(self):
        # Expect the offer to be applied as many times as it can, with any excess
        # priced normally
        assert checkout_solution.checkout(5 * 'B') == 120

    def test_order_of_special_offer_application(self):
        """
        Suppose we have two special offers for item 'A':
         - 3 for 130
         - 5 for 200

         With a normal price of 1 for 50

         Given 6 As, we should expect this to be applied as:
           - 5 for 200
           - 1 for 50
         Which is 250

         I.e. it does not work this out as 2 * (3 for 130) == 260

         It maximises the number of times the largest discount can be used. Implicitly assumes therefore that discounts
         on larger numbers of items are 'better'
        """
        assert checkout_solution.checkout(6 * 'A') == 250
        # Hit 5 for 200 multiple times - should still prioritise this over 3 for 130
        assert checkout_solution.checkout(11 * 'A') == 450

    def test_multiple_discounts_hit(self):
        """
        Multiple different special offers can be applied to the same item, with the best discounts being applied first
        until there are not enough items left, then the remainder being tested against smaller special offers and so on
        """
        # 5A for 200 + 3A for 130 == 330
        assert checkout_solution.checkout(8 * 'A') == 330

