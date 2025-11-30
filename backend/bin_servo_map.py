"""
bin_servo_map.py

Maps each waste type to the exact servo instructions needed
to control the sorting mechanism.

Servo 1 (S1)  → 180° tilt servo (exact angles)
Servo 2 (S2)  → 360° continuous rotation (direction commands)

IMPORTANT:
- Do NOT put numeric values like 82, 0, 91 here.
- Those values belong in the ESP8266 firmware only.
- Python only sends symbolic commands: "left", "right", "stop", etc.

This keeps the system clean, modular, and easy to recalibrate.
"""


# ================================
# 🔵 360° Servo Motion Commands
# ================================
# These symbolic labels match the ESP8266 commands:
#
#   "left"        → ESP sends 0  (LEFT_360)
#   "right"       → ESP sends 91 (RIGHT_360)
#   "stop"        → ESP sends 82 (STOP_360)
#   "left_short"  → short burst left, then stop
#   "right_short" → short burst right, then stop
#
# DO NOT PUT NUMBERS IN PYTHON.
# ================================


# ================================
# 🔵 SERVO POSITION TABLE
# ================================
# Waste Type → 180° Servo Angle + 360° Servo Command
#
# s1 = angle for the 180° tilt servo (0–180°)
# s2 = direction command for the 360° servo
# ================================

SERVO_POSITIONS = {

    # ♻️ Recyclable (paper, plastic, cardboard, glass)
    "recyclable": {
        "s1": 20,           # tilt to left bin
        "s2": "left"        # rotate conveyor left
    },

    # ☣️ Hazardous (battery, metal, electronics)
    "hazardous": {
        "s1": 90,           # tilt to center
        "s2": "right"       # rotate conveyor right
    },

    # 🍃 Organic (food waste, biological)
    "organic": {
        "s1": 45,           # slight tilt
        "s2": "left_short"  # quick push left
    },

    # 🚮 Non-Recyclable (trash, clothes, shoes)
    "non-recyclable": {
        "s1": 110,          # tilt to right bin
        "s2": "right_short" # quick push right
    },
}


# ================================
# 🔵 Safe fallback for unknown types
# ================================
# If the ML model outputs a class that is not in the mapping,
# we return a safe fallback:
#
# - S1 → return to center (90°)
# - S2 → STOP 360° servo ("stop")
# ================================

def get_servo_positions(waste_type: str):
    """
    Given a waste_type ("recyclable", "organic", "hazardous", "non-recyclable"),
    return the correct S1 and S2 instructions.

    Includes a safe fallback when waste_type is unknown.
    """
    return SERVO_POSITIONS.get(
        waste_type,
        {
            "s1": 90,       # center tilt
            "s2": "stop"    # STOP continuous servo
        }
    )
