# utils.py

# ---------------------------
# LABEL MAPPINGS
# ---------------------------

ACNE_MAP = {
    0: "no acne / clear skin",
    1: "mild acne",
    2: "moderate acne",
    3: "severe acne"
}

SKIN_TYPE_MAP = {
    0: "dry",
    1: "normal",
    2: "oily"
}

SKIN_TONE_MAP = {
    0: "Type I (Very Fair)",
    1: "Type II (Fair)",
    2: "Type III (Medium)",
    3: "Type IV (Olive)",
    4: "Type V (Brown)",
    5: "Type VI (Dark Brown/Black)"
}

# ---------------------------
# FUNCTIONS FOR IMPORT
# ---------------------------

def map_acne(code: int) -> str:
    return ACNE_MAP.get(code, "unknown")

def map_skin_type(code: int) -> str:
    return SKIN_TYPE_MAP.get(code, "unknown")

def map_skin_tone(code: int) -> str:
    return SKIN_TONE_MAP.get(code, "unknown")
