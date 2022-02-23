from dataclasses import dataclass
from copy import copy

@dataclass
class Material:
    diffuse: (float, float, float) = (0.8, 0.8, 0.8)
    alpha: float = 1.0
    metallic: float = 0.0
    roughness: float = 0.8
    subsurface: float = 0.0
    subsurface_color: (float, float, float) = (0.8, 0.8, 0.8)
    transmission: float = 0.0
    transmission_roughness: float = 0.0
    ior: float = 1.45
    emission: (float, float, float) = (0.0, 0.0, 0.0)
    clearcoat: float = 1.0
    clearcoat_roughness: float = 0.03

    @property
    def transparency(self):
        return 1.0 - self.alpha

    @property
    def shininess(self):
        return 1.0 - self.roughness

    def from_name(name: str):
        from .materials import BASE_MATERIALS, BASE_MATERIAL_COLORS, BASE_MATERIAL_VARIANTS

        if name.count("-") != 2:
            return Material()

        base_str, color_str, variant_str = name.split("-")

        if not (base := BASE_MATERIALS.get(base_str)):
            return Material()

        colors = BASE_MATERIAL_COLORS[base_str]

        if not (color := colors.get(color_str)):
            return Material()

        material = base.copy()

        if type(color) == Material:
            return color
        else:
            material.diffuse = color

        variants = BASE_MATERIAL_VARIANTS[base_str]
        if values := variants.get(variant_str):
            for attr, value in values.items():
                setattr(material, attr, value)

        return material

    def copy(self):
        return copy(self)

def hex2rgb(hex_string):
    return (
        int(hex_string[0:2], 16) / 255,
        int(hex_string[2:4], 16) / 255,
        int(hex_string[4:6], 16) / 255
    )

def srgb2lin(color):
    result = []
    for srgb in color:
        if srgb <= 0.0404482362771082:
            lin = srgb / 12.92
        else:
            lin = pow(((srgb + 0.055) / 1.055), 2.4)
        result.append(lin)
    return result


def lin2srgb(color):
    result = []
    for lin in color:
        if lin > 0.0031308:
            srgb = 1.055 * (pow(lin, (1.0 / 2.4))) - 0.055
        else:
            srgb = 12.92 * lin
        result.append(srgb)
    return result
