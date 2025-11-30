# 4-bin servo angles
BIN_ANGLES = {
    "recyclable": 45,   # paper, cardboard, plastic
    "glass": 135,       # all glass colors
    "metal": 225,       # metal + batteries
    "general": 315      # clothes, shoes, trash, biological
}

# Map 12 classes → 4 bin categories
CLASS_TO_CATEGORY = {
    "battery": "metal",
    "biological": "general",
    "brown-glass": "glass",
    "cardboard": "recyclable",
    "clothes": "general",
    "green-glass": "glass",
    "metal": "metal",
    "paper": "recyclable",
    "plastic": "recyclable",
    "shoes": "general",
    "trash": "general",
    "white-glass": "glass",
}


def get_category_for_class(class_name: str) -> str:
    """Map model class → bin category (recyclable/glass/metal/general)."""
    return CLASS_TO_CATEGORY.get(class_name, "general")


def get_angle_for_category(category: str) -> int:
    """Map bin category → servo angle."""
    return BIN_ANGLES.get(category, -1)


def get_angle_for_class(class_name: str) -> int:
    """Directly map model class → servo angle."""
    category = get_category_for_class(class_name)
    return get_angle_for_category(category)