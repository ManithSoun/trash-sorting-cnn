def get_category(predicted_class):
    category_map = {
        "battery": "hazardous",
        "biological": "organic",

        "brown-glass": "recyclable",
        "green-glass": "recyclable",
        "white-glass": "recyclable",
        "cardboard": "recyclable",
        "paper": "recyclable",
        "plastic": "recyclable",
        "metal": "recyclable",

        "clothes": "non-recyclable",
        "shoes": "non-recyclable",
        "trash": "non-recyclable",
    }

    return category_map.get(predicted_class, "non-recyclable")
