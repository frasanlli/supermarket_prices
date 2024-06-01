from datetime import datetime

class Cesta():
    def __init__(self):
        self.hoy = datetime.now().strftime("%d_%m_%y")
        self.tipo_filtro=["clasificar", "eliminar", "seleccionar"]
        self.lista_todos=["aceite", "garbanzo", "lenteja", "alubia", "carne picada",
                          "arroz", "leche entera", "manzana", "banana", "pimiento",
                          "calabacín", "cebolla", "berenjena", "huevos", "mantequilla"]
        self.lista_mercadona={"aceite":{
                            "tipo_filtro": self.tipo_filtro[0],
                            "filtro": ["oliva", "girasol", "coco"]
                            },
                            "mantequilla":{
                            "tipo_filtro": self.tipo_filtro[2],
                            "filtro": ["mantequilla"]
                            },
                        "legumbres":{
                            "tipo_filtro": self.tipo_filtro[2],
                            "filtro": ["garbanzo", "lenteja", "alubia"]
                            },
                        "arroz":{
                            "tipo_filtro": self.tipo_filtro[2],
                            "filtro": ["arroz"]
                            },
                        "pasta":{
                            "tipo_filtro": "",
                            "filtro": ""
                            },
                        "leche entera":{
                            "tipo_filtro": self.tipo_filtro[0],
                            "filtro": ["con lactosa","sin lactosa"]
                            },
                        "fruta":{
                            "tipo_filtro": self.tipo_filtro[2],
                            "filtro": ["manzana", "banana"]
                            },
                        "verdura":{
                            "tipo_filtro": self.tipo_filtro[2],
                            "filtro": ["pimiento", "calabacín", "cebolla", "berenjena"]
                            },
                        "huevos":{
                            "tipo_filtro": "",
                            "filtro": ""
                            },
                        "carne picada":{
                            "tipo_filtro": self.tipo_filtro[0],
                            "filtro": ["pollo", "ternera"]
                            },
                        }

        """queso fresco":{
                    "tipo_filtro": self.tipo_filtro[0],
                    "filtro": ["con lactosa","sin lactosa"]
                    },
            "agua":{
                    "tipo_filtro": self.tipo_filtro[1],
                    "filtro": ["gas", "coco"]
                    },"""
