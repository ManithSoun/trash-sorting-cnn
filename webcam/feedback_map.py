def get_feedback_for_class(class_name):

    feedback = {
        "battery": 
            "⚠️ Batteries contain toxic chemicals. Do NOT throw in normal bins. "
            "Store separately and take to a hazardous waste collection center.",

        "biological": 
            "🌱 This is organic waste. Place it in the ORGANIC / COMPOST bin.",

        "brown-glass": 
            "♻️ Brown glass is recyclable. Rinse and put in the GLASS RECYCLING bin.",

        "cardboard": 
            "📦 Cardboard is recyclable. Flatten the box and place it in the PAPER/CARDBOARD recycling bin.",

        "clothes": 
            "👕 Clothes should NOT go into normal trash. Donate, reuse, or drop at textile recycling points.",

        "green-glass": 
            "♻️ Green glass is recyclable. Rinse and put in the GLASS RECYCLING bin.",

        "metal": 
            "🪙 Metal is recyclable. Clean if needed and place into METAL recycling bin.",

        "paper": 
            "📄 Paper is recyclable. Make sure it's dry and clean, then put it in PAPER recycling.",

        "plastic": 
            "🧴 Plastic is recyclable. Rinse it and place in the PLASTIC recycling bin.",

        "shoes": 
            "👟 Shoes are generally NOT recyclable. Donate if usable, otherwise dispose in GENERAL waste.",

        "trash": 
            "🗑️ This item cannot be recycled. Dispose it in the GENERAL waste bin.",

        "white-glass": 
            "♻️ White/clear glass is recyclable. Rinse and place in the GLASS recycling bin."
    }

    return feedback.get(class_name, "❓ No feedback available for this item.")
