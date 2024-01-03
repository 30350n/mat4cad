import re
from dataclasses import dataclass
from copy import copy
from typing import Tuple

@dataclass
class Material:
    diffuse: Tuple[float, float, float] = (0.8, 0.8, 0.8)
    alpha: float = 1.0
    metallic: float = 0.0
    roughness: float = 0.8
    subsurface_mm: float = 0.0
    subsurface_radius: Tuple[float, float, float] = None
    transmission: float = 0.0
    ior: float = 1.45
    emission: float = 0.0
    emission_color: Tuple[float, float, float] = (1.0, 1.0, 1.0)
    coat: float = 0.0
    coat_roughness: float = 0.03
    bevel_mm: float = 0.05

    name: str = None
    base: str = None
    color: str = None
    variant: str = None

    has_custom_color: bool = False
    custom_color: str = None

    @property
    def transparency(self):
        return 1.0 - self.alpha

    @property
    def shininess(self):
        return 1.0 - self.roughness

    @staticmethod
    def from_name(name: str):
        from .materials import (
            BASE_MATERIALS, BASE_MATERIAL_COLORS, BASE_MATERIAL_VARIANTS, SUBSURFACE_RADIUSES
        )

        if name.count("-") != 2:
            return None

        base_str, color_str, variant_str = name.split("-")

        if not (base := BASE_MATERIALS.get(base_str)):
            return None

        material = base.copy()

        if custom_color_regex.match(color_str):
            material.has_custom_color = True
            material.custom_color = color_str.split("_")[1]
            material.diffuse = hex2rgb(material.custom_color)
        else:
            color_options = BASE_MATERIAL_COLORS[base_str]
            if not (color := color_options.get(color_str)):
                return None
            if isinstance(color, Material):
                material = color.copy()
            else:
                material.diffuse = color

        variants = BASE_MATERIAL_VARIANTS[base_str]
        if values := variants.get(variant_str):
            for attr, value in values.items():
                if isinstance(value, dict):
                    if not (value := value.get(color_str)):
                        continue
                setattr(material, attr, value)

        if ssrs := SUBSURFACE_RADIUSES.get(base_str):
            if ssr := ssrs.get(color_str):
                material.subsurface_radius = ssr

        material.name = name
        material.base = base_str
        material.color = color_str
        material.variant = variant_str

        return material

    def copy(self):
        return copy(self)

custom_color_regex = re.compile(r"^custom_[0-9A-Fa-f]{6}$")

def hex2rgb(hex_string):
    return (
        int(hex_string[0:2], 16) / 255,
        int(hex_string[2:4], 16) / 255,
        int(hex_string[4:6], 16) / 255,
    )

def rgb2hex(rgb):
    return "".join((
        f"{int(rgb[0] * 255):02x}",
        f"{int(rgb[1] * 255):02x}",
        f"{int(rgb[2] * 255):02x}",
    ))

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
