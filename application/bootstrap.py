from __future__ import annotations
from csv import Dialect
from unittest import skipUnless
from domain.pricing import PricingStrategy, NoDiscount, PercentageDiscount, BulkItemDiscount, CompositeStrategy


def choose_strategy(kind: str, **kwargs) -> PricingStrategy:
    # TODO: Implement strategy selection logic based on the 'kind' parameter
    
    # Should support: "none", "percent", "bulk", "composite"
    # Each strategy type needs different parameters from **kwargs
    # Return the appropriate strategy instance or raise an error for unknown types
    
    if kind == "none":
        return NoDiscount()
    
    elif kind == "percent":
        percent = kwargs.get("percent")
        return PercentageDiscount(percent)
    
    elif kind == "bulk":
        sku = kwargs.get("sku")
        threshold = kwargs.get("threshold")
        per_item_off = kwargs.get("per_item_off")
        if None in (sku, threshold, per_item_off):
            raise ValueError("Missing one of the required paramters")
        return BulkItemDiscount(sku, threshold, per_item_off)
    
    elif kind == "composite":
        percent = kwargs.get("percent", 0.0)
        sku = kwargs.get("sku", "")
        threshold = kwargs.get("threshold", 0)
        per_item_off = kwargs.get("per_item_off", 0.0)
        return CompositeStrategy([
            PercentageDiscount(percent),
            BulkItemDiscount(sku, threshold, per_item_off),
        ])
    else:
        raise ValueError("kind must be a valid choice between 'none', 'percent', 'bulk', 'composite'")
