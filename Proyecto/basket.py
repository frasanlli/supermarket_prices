from datetime import datetime
from product import Product

class Basket():
    def __init__(self):

        self.data: dict[str, list] = {
            "product":[],
            "name": [],
            "unitary price(€)": [],
            "quantity": [],
            "price per quantity(€/quantity)":[],
            "supermarket":[]
            }

        self.today = datetime.now().strftime("%d_%m_%y")

        legumbres: Product = Product(product = "legumbres",
                                    avoid_words = ["pasta", " de ", " con ", "queso"],
                                    key_words = ["garbanzo", "lenteja", "alubia"],
                                    subproduct_words = ["garbanzo", "lenteja", "alubia"])

        arroz: Product = Product(product = "arroz",
                                avoid_words = [" de ", " con ", " para ", "ultracongelado",
                                               "harina", "galleta", "tortitas"],
                                key_words = ["arroz"],
                                subproduct_words = [])

        harina: Product = Product(product = "harina",
                                avoid_words = [],
                                key_words = ["harina de trigo"],
                                subproduct_words = ["harina de trigo"])

        leche: Product = Product(product = "leche",
                                avoid_words = ["helado", "avena", "soja", "arroz", " con ", "dulce",
                                               " al ", " para ", "crema", "batido", "evaporada", "coco",
                                               " pan ", " pan", "fruta", "cereales", "polvo", "condensada",
                                               "facial", "facial", "queso", "q.", "galleta", "kit",
                                               "chocolate", "salchicha"],
                                key_words = ["leche"],
                                subproduct_words = ["leche entera", "leche semidesnatada", "leche desnatada",
                                                    "leche en polvo", "leche sin lactosa"])

        fruta: Product = Product(product = "fruta",
                                avoid_words = ["zumo", "batido", "congelado", "congelada", "vinagre",
                                               " y ", "sabor", "postre", "leche", "yogur"],
                                key_words = ["manzana", "banana", "plátano", "platano"],
                                subproduct_words = ["manzana", "banana", "plátano", "platano"])

        verdura: Product = Product(product = "verdura",
                                avoid_words = ["frito", "frita", "salsa", "polvo", " de ", " con ", "untar"
                                               "aperitivo", "light", " y ", "caramelizada", "troceado",
                                               "triturado", "frito", "piquillo", "freír", "hot", "picante",
                                               "bolsa", "confitura", "sardinilla"],
                                key_words = ["pimiento", "tomate", "cebolla", "berenjena", "patata"],
                                subproduct_words = [])

        huevo: Product = Product(product = "huevo",
                                avoid_words = ["codorniz", " al ", "chocolate", "claras", "bizcocho",
                                               "sándwich","flan", "ensalada", "sin", "sorpresa",
                                               "kinder", "queso"],
                                key_words = ["huevo", "docena"],
                                subproduct_words = [])

        mantequilla: Product = Product(product = "mantequilla",
                                avoid_words = ["margarina", "masa"],
                                key_words = [],
                                subproduct_words = [])

        aceite: Product = Product(product = "aceite",
                                avoid_words = ["coco", "monodosis", "vinagre", "pack", " en ", "queso",
                                               "porciones", " con ", "aliño", "corporal", "facial",
                                               "ricino", "baño", " para ", "solar", "abrillantador",
                                               "tortas", " pan ", "pastas", "protectora", "cantábrico",
                                                "atún", "torta", "anchoa"],
                                key_words = ["aceite","aceite de girasol","aceite de oliva"],
                                subproduct_words = ["aceite de girasol","aceite de oliva"])

        pasta: Product = Product(product = "pasta",
                                avoid_words = ["precocinada", "precocinado", "fresca"],
                                key_words = ["pasta", "macarrones", "espagueti", "nidos"],
                                subproduct_words = [])

        agua: Product = Product(product = "agua",
                                avoid_words = ["gas", "coco"],
                                key_words = ["agua"],
                                subproduct_words = [])

        queso: Product = Product(product = "queso",
                                avoid_words = [],
                                key_words = ["queso"],
                                subproduct_words = ["queso fresco", "queso curado", "queso semicurado",
                                                    "queso tierno", "queso viejo", "queso añejo",
                                                    "queso sin lactosa"])

        self.products_list: list[Product] = [legumbres, arroz, harina, leche,
                                             fruta, verdura, huevo, mantequilla,
                                             aceite]
