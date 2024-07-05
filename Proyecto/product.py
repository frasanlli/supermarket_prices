
class Product():
    def __init__(self,
                 product: str,
                 avoid_words: list[str],
                 key_words: list[str],
                 subproduct_words: list[str]) -> None:
        self.product = product
        """self.real_name: str = ""
        self.unit_price: float = 0
        self.quantity: float = 0
        self.quantity_magnitude: str = ""
        self.quantity_price = 0
        self.supermarket = """""
        self.avoid_words = avoid_words
        self.key_words = key_words
        self.subproduct_words = subproduct_words