from __future__ import annotations
from dataclasses import dataclass
from abc import ABC, abstractmethod
from multiprocessing import Value
from typing import ItemsView


@dataclass(frozen=True)
class LineItem:
    sku: str
    qty: int
    unit_price: float


class PricingStrategy(ABC):
    # TODO: Define the common interface for all pricing strategies.
    # This should include a method that takes pricing parameters and returns a calculated value.
    @abstractmethod
    def apply(self, subtotal: float, items: list(LineItem)):
        
        raise NotImplementedError


class NoDiscount(PricingStrategy):
    # TODO: Implement a strategy that returns the original value without changes
    def apply(self, subtotal: float, items: list[LineItem]):
        if not isinstance(subtotal, (int, float)):
            raise TypeError("subtotal must be a number")
        if subtotal < 0:
            raise ValueError("subtotal cannot be negative")
        for it in items:
            if it.qty < 0:
                raise ValueError("qty cannot be negative")
            if it.unit_price < 0:
                raise ValueError("unit_price cannot be negative")
            
        return round(float(subtotal), 2)


class PercentageDiscount(PricingStrategy):
    def __init__(self, percent: float) -> None:
        # TODO: Store the percentage value and validate it's in the correct range
        if not isinstance(percent, (int,float)):
            raise TypeError("percent must be a number")
        if not 0 <= percent <= 100:
            raise ValueError("percent must be between 0 and 100")
        self._p = float(percent) / 100
        
    def apply(self, subtotal: float, items: list[LineItem]):
        if not isinstance(subtotal, (int, float)):
            raise TypeError("subtotal must be a number")
        if subtotal < 0:
            raise ValueError("subtotal cannot be negative")
        for it in items:
            if it.qty < 0:
                raise ValueError("qty cannot be negative")
            if it.unit_price < 0:
                raise ValueError("unit_price cannot be negative")
        return round(float(subtotal * (1 - self._p)), 2)
    # TODO: Implement the main calculation method that reduces the input by a percentage


class BulkItemDiscount(PricingStrategy):
    """If any single item's quantity >= threshold, apply a per-item discount for that SKU."""
    def __init__(self, sku: str, threshold: int, per_item_off: float) -> None:
        # TODO: Store the parameters needed to identify items and calculate reductions
        self._sku = sku
        self._threshold = threshold
        self._per_itm_discount = per_item_off

    # TODO: Implement logic to iterate through items and apply reductions based on quantity thresholds
    def apply(self, subtotal: float, items: list(LineItem)):
        if not isinstance(subtotal, (int, float)):
            raise TypeError("subtotal must be a number")
        if subtotal < 0:
            raise ValueError("subtotal cannot be negative")
        for it in items:
            if it.qty < 0:
                raise ValueError("qty cannot be negative")
            if it.unit_price < 0:
                raise ValueError("unit_price cannot be negative")
        for it in items:
            if it.sku == self._sku and it.qty >= self._threshold:
                subtotal -= self._per_itm_discount * it.qty 
        return round(float(subtotal), 2)

class CompositeStrategy(PricingStrategy):
    """Compose multiple strategies; apply in order."""
    def __init__(self, strategies: list[PricingStrategy]) -> None:
        # TODO: Store the collection of strategies to be applied sequentially
        self._strategies = strategies

    # TODO: Implement method that applies each strategy in sequence, using the output of one as input to the next
    def apply(self, subtotal: float, items: list(LineItem)):
        for strategy in self._strategies:
            subtotal = strategy.apply(subtotal, items)
        return round(float(subtotal), 2)
    
def compute_subtotal(items: list[LineItem]) -> float:
    return round(sum(it.unit_price * it.qty for it in items), 2)
