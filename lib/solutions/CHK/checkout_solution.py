from collections import defaultdict


prices = {
    'A': 50,
    'B': 30,
    'C': 20,
    'D': 15
}

special_offers = {
    'A': (3, 130),
    'B': (2, 45)
}

# noinspection PyUnusedLocal
# skus = unicode string
def checkout(skus):
    # String will have a letter for each occurrence of the item
    counts_per_sku = defaultdict(int)
    for sku in skus:
        if sku in prices:
            counts_per_sku[sku] += 1
        else:
            return -1

    total = 0
    for sku, count in counts_per_sku:
        if special_offer := special_offers.get('SKU'):
            total += (count / )
