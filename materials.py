from .colors import METAL_COLORS, PCB_COLORS, RAL_COLORS
from .core import Material, hex2rgb

BASE_MATERIALS = {
    "plastic": Material(roughness=0.4),
    "plastic_transparent": Material(ior=1.46, transmission=0.5, roughness=0.05, alpha=0.5),
    "metal": Material(roughness=0.25, metallic=1.0),
    "metal_painted": Material(roughness=0.4, metallic=1.0, coat=1.0, coat_roughness=0.4),
    "pcb": Material(roughness=0.4, subsurface_mm=1.0, transmission=0.25, alpha=0.95),
    "rubber": Material(roughness=0.4, bevel_mm=0.2),
    "special": Material(),
}

SPECIAL_MATERIALS = {
    "pins_silver": Material(diffuse=hex2rgb("eaeae5"), metallic=1.0, roughness=0.2),
    "pins_gold": Material(diffuse=hex2rgb("efdfbb"), metallic=1.0, roughness=0.1),
}

BASE_MATERIAL_COLORS = {
    "plastic": RAL_COLORS,
    "plastic_transparent": RAL_COLORS,
    "metal": METAL_COLORS,
    "metal_painted": RAL_COLORS,
    "rubber": RAL_COLORS,
    "pcb": PCB_COLORS,
    "special": SPECIAL_MATERIALS,
}

PLASTIC_VARIANTS = {
    "glossy": {"roughness": 0.15},
    "semi_matte": {"roughness": 0.4},
    "matte": {"roughness": 0.8, "specular": 0.1, "coat": 0.1, "coat_roughness": 0.2},
}

PLASTIC_TRANSPARENT_VARIANTS = {
    "clear": {"roughness": 0.05},
    "diffused": {"roughness": 0.2},
}

METAL_VARIANTS = {
    "glossy": {"roughness": 0.1},
    "semi_matte": {"roughness": 0.25},
    "matte": {"roughness": 0.4},
}

METAL_PAINTED_VARIANTS = {
    "glossy": {"roughness": 0.1},
    "semi_matte": {"roughness": 0.4},
    "matte": {"roughness": 0.6},
}

RUBBER_VARIANTS = {
    "glossy": {"roughness": 0.15},
    "semi_matte": {"roughness": 0.4},
    "matte": {"roughness": 0.8},
}

BASE_MATERIAL_VARIANTS = {
    "plastic": PLASTIC_VARIANTS,
    "plastic_transparent": PLASTIC_TRANSPARENT_VARIANTS,
    "metal": METAL_VARIANTS,
    "metal_painted": METAL_PAINTED_VARIANTS,
    "pcb": None,
    "rubber": RUBBER_VARIANTS,
    "special": None,
}

SUBSURFACE_RADIUSES = {
    "pcb": {
        "pcb_brown": (1.0, 0.2, 0.1),
        "pcb_yellow": (0.4, 0.4, 0.1),
    }
}

for name, material in BASE_MATERIALS.items():
    globals()[f"BASE_{name.upper()}"] = material
