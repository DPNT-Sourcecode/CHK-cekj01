from collections import defaultdict

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


class TestRunBuyXGetYFreeOffers():

    def _remove_zero_skus(self, counts_per_sku):
        return {k: v for k, v in counts_per_sku.items() if v > 0}

    def test_no_items(self):
        """
        Smoke test to make sure everything works with an empty basket
        """
        counts_per_sku = checkout_solution.build_counts_by_sku('')
        assert len(counts_per_sku) == 0

        offers_ran = checkout_solution.run_buy_x_get_y_free_offers(counts_per_sku)
        assert self._remove_zero_skus(offers_ran) == {}

    def test_no_matches(self):
        """
        When there are no matches, expect the counts to remain unchanged
        """
        counts_per_sku = checkout_solution.build_counts_by_sku('EB')
        assert counts_per_sku == {'E': 1, 'B': 1}

        offers_ran = checkout_solution.run_buy_x_get_y_free_offers(counts_per_sku)
        assert self._remove_zero_skus(offers_ran) == {'E': 1, 'B': 1}

    def test_match(self):
        """
        When a match occurs, expect the amount of the free sku to be decremented
        """
        counts_per_sku = checkout_solution.build_counts_by_sku('EEB')
        assert counts_per_sku == {'E': 2, 'B': 1}

        offers_ran = checkout_solution.run_buy_x_get_y_free_offers(counts_per_sku)
        assert self._remove_zero_skus(offers_ran) == {'E': 2}

    def test_multiple_matches(self):
        """
        A match on the same offer can occur multiple times, decrementing the free sku each time
        """
        counts_per_sku = checkout_solution.build_counts_by_sku('EEEEBB')
        assert counts_per_sku == {'E': 4, 'B': 2}

        offers_ran = checkout_solution.run_buy_x_get_y_free_offers(counts_per_sku)
        assert self._remove_zero_skus(offers_ran) == {'E': 4}

    def test_decrement_stops_at_zero(self):
        """
        Suppose we have an offer 'Buy 2 Es and get 1 B free' and a basket of 4 Es and 1 B.

        The offer will trigger twice, but there is only 1 B in the basket to make 'free'. The count of B should be
        decremented to zero.
        """
        counts_per_sku = checkout_solution.build_counts_by_sku('EEEEB')
        assert counts_per_sku == {'E': 4, 'B': 1}

        offers_ran = checkout_solution.run_buy_x_get_y_free_offers(counts_per_sku)
        assert self._remove_zero_skus(offers_ran) == {'E': 4}

    def test_x_and_y_are_same_sku(self):
        """
        It should be possible to have X and Y be the same sku, e.g.
        'Buy 2 Fs and get an F free'
        """
        counts_per_sku = checkout_solution.build_counts_by_sku('FFF')
        assert counts_per_sku == {'F': 3}

        offers_ran = checkout_solution.run_buy_x_get_y_free_offers(counts_per_sku)
        assert self._remove_zero_skus(offers_ran) == {'F': 2}

    def test_x_and_y_same_multiple_applications(self):
        """
        When X and Y are the same, we are decrementing the same SKU we are counting. Each application of the offer
        must consider the total count to be the previously decremented value.
        """
        # Doesn't really make sense with the 2 for 1 - fix by having config injected when required
        counts_per_sku = checkout_solution.build_counts_by_sku('FFFFF')
        assert counts_per_sku == {'F': 5}

        # Remove an F on first run, second time there isn't one to remove
        offers_ran = checkout_solution.run_buy_x_get_y_free_offers(counts_per_sku)
        assert self._remove_zero_skus(offers_ran) == {'F': 4}


class TestOffersIntegration():
    """
    Complex test cases involving multiple test schemes and how they interact
    """
    # Refactor this later as new offers break out into their own method

    def test_free_items_applied_before_other_discounts(self):
        """
        Any offer which gives free items should be applied first. Once an item is considered 'free' it should
        no longer contribute to the cost nor to any further discounts on that sku. E.g. if we have
        - 'Buy 2 Es and get 1 B free' and
        - '2 Bs for 45'
        Given a basket of 4 Es and 3 Bs, this should apply as follows:
        - 'Buy 2 Es and get 1 B free' triggers twice, effectively removing 2 Bs from the cost and stopping them counting
          towards any further discounts
        - With 1 B left not affected, it is added at it's normal cost
        """
        assert checkout_solution.checkout('EEEEBBB') == (4 * 40) + 30
