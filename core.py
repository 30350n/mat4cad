from dataclasses import dataclass
from copy import copy

@dataclass
class Material:
    diffuse: (float, float, float) = (0.8, 0.8, 0.8)
    alpha: float = 1.0
    metallic: float = 0.0
    roughness: float = 0.8
    subsurface_mm: float = 0.0
    subsurface_radius: (float, float, float) = None
    transmission: float = 0.0
    transmission_roughness: float = 0.0
    ior: float = 1.45
    emission: (float, float, float) = (0.0, 0.0, 0.0)
    clearcoat: float = 0.0
    clearcoat_roughness: float = 0.03
    bevel_mm: float = 0.05

    @property
    def transparency(self):
        return 1.0 - self.alpha

    @property
    def shininess(self):
        return 1.0 - self.roughness

    def from_name(name: str):
        from .materials import (
            BASE_MATERIALS, BASE_MATERIAL_COLORS, BASE_MATERIAL_VARIANTS, SUBSURFACE_RADIUSES
        )

        if name.count("-") != 2:
            return None

        base_str, color_str, variant_str = name.split("-")

        if not (base := BASE_MATERIALS.get(base_str)):
            return None

        color_options = BASE_MATERIAL_COLORS[base_str]
        if not (color := color_options.get(color_str)):
            return None

        material = base.copy()

        if type(color) == Material:
            return color
        else:
            material.diffuse = color

        variants = BASE_MATERIAL_VARIANTS[base_str]
        if values := variants.get(variant_str):
            for attr, value in values.items():
                if type(value) == dict:
                    if not (value := value.get(color_str)):
                        continue
                setattr(material, attr, value)

        if ssrs := SUBSURFACE_RADIUSES.get(base_str):
            if ssr := ssrs.get(color_str):
                material.subsurface_radius = ssr

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
