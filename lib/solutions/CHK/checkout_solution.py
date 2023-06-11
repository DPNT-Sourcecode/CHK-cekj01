from collections import defaultdict


prices = {
    'A': 50,
    'B': 30,
    'C': 20,
    'D': 15
}

special_offers = {
    'A': [(5, 200), (3, 130)],
    'B': [(2, 45)],
}

# noinspection PyUnusedLocal
# skus = unicode string

def _build_counts_by_sku(skus: str):
    counts_per_sku = defaultdict(int)
    for sku in skus:
        if sku in prices:
            counts_per_sku[sku] += 1
        else:
            raise ValueError
    return counts_per_sku


def checkout(skus):
    # String will have a letter for each occurrence of the item
    if not type(skus) == str:
        return -1

    try:
        counts_per_sku = _build_counts_by_sku(skus)
    except ValueError:
        return -1

    total = 0
    for sku, count in counts_per_sku.items():
        remaining = count
        if special_offers_for_sku := special_offers.get(sku):
            for special_offer in special_offers_for_sku:
                amount_applicable = remaining // special_offer[0]
                total += amount_applicable * special_offer[1]
                remaining -= amount_applicable
        total += remaining * prices[sku]

    return total
