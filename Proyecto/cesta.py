from datetime import datetime

class Cesta():
    def __init__(self):
        self.hoy = datetime.now().strftime("%d_%m_%y")
        self.tipo_filtro=["clasificar", "eliminar", "seleccionar"]
        self.lista_todos=["garbanzo", "lenteja", "alubia", "arroz", "harina de trigo",
                        "leche entera", "manzana", "banana", "pimiento", "tomate",
                        "cebolla", "berenjena", "huevos", "mantequilla", "patata",
                        "aceite de oliva", "aceite de girasol", "aceite de coco"]

        self.lista_evitar=["monodosis", "vinagre"]
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
                        "harina":{
                            "tipo_filtro": self.tipo_filtro[2],
                            "filtro": ["harina de trigo"]
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
                            "filtro": ["pimiento", "calabacín", "cebolla", "berenjena", "patata"]
                            },
                        "huevos":{
                            "tipo_filtro": "",
                            "filtro": ""
                            }
                        }

        """queso fresco":{
                    "tipo_filtro": self.tipo_filtro[0],
                    "filtro": ["con lactosa","sin lactosa"]
                    },
            "agua":{
                    "tipo_filtro": self.tipo_filtro[1],
                    "filtro": ["gas", "coco"]
                    },
            "pasta":{
                            "tipo_filtro": "",
                            "filtro": ""
                            },"""
