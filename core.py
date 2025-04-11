import re
from copy import copy
from dataclasses import dataclass
from typing import Sequence


@dataclass
class Material:
    diffuse: tuple[float, float, float] = (0.8, 0.8, 0.8)
    alpha: float = 1.0
    metallic: float = 0.0
    roughness: float = 0.8
    subsurface_mm: float = 0.0
    subsurface_radius: tuple[float, float, float] | None = None
    transmission: float = 0.0
    ior: float = 1.45
    emission_strength: float = 0.0
    emission_color: tuple[float, float, float] = (1.0, 1.0, 1.0)
    coat: float = 0.0
    coat_roughness: float = 0.03
    bevel_mm: float = 0.05

    name: str | None = None
    base: str | None = None
    color: str | None = None
    variant: str | None = None

    has_custom_color: bool = False
    custom_color: str | None = None

    @property
    def emission(self):
        return tuple([component * self.emission_strength for component in self.emission_color])

    @property
    def transparency(self):
        return 1.0 - self.alpha

    @property
    def shininess(self):
        return 1.0 - self.roughness

    @classmethod
    def from_name(cls, name: str):
        from .materials import (
            BASE_MATERIAL_COLORS,
            BASE_MATERIAL_VARIANTS,
            BASE_MATERIALS,
            SUBSURFACE_RADIUSES,
        )

        if name.count("-") != 2:
            return None

        base_str, color_str, variant_str = name.split("-")

        if not (base := BASE_MATERIALS.get(base_str)):
            return None

        material = base.copy()

        if _CUSTOM_COLOR_REGEX.match(color_str):
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

        if variants := BASE_MATERIAL_VARIANTS[base_str]:
            if values := variants.get(variant_str):
                for attr, value in values.items():
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


_CUSTOM_COLOR_REGEX = re.compile(r"^custom_[0-9A-Fa-f]{6}$")

ColorTuple = tuple[float, float, float]


def hex2rgb(hex_string: str) -> ColorTuple:
    return (
        int(hex_string[0:2], 16) / 255,
        int(hex_string[2:4], 16) / 255,
        int(hex_string[4:6], 16) / 255,
    )


def rgb2hex(rgb: Sequence[float]):
    return "".join(
        (
            f"{int(rgb[0] * 255):02x}",
            f"{int(rgb[1] * 255):02x}",
            f"{int(rgb[2] * 255):02x}",
        )
    )


def srgb2lin(color: Sequence[float]) -> ColorTuple:
    def _srgb2lin(srgb: float):
        if srgb <= 0.0404482362771082:
            return srgb / 12.92
        else:
            return pow(((srgb + 0.055) / 1.055), 2.4)

    return (
        _srgb2lin(color[0]),
        _srgb2lin(color[1]),
        _srgb2lin(color[2]),
    )


def lin2srgb(color: Sequence[float]) -> ColorTuple:
    def _lin2srgb(lin: float):
        if lin > 0.0031308:
            return 1.055 * (pow(lin, (1.0 / 2.4))) - 0.055
        else:
            return 12.92 * lin

    return (
        _lin2srgb(color[0]),
        _lin2srgb(color[1]),
        _lin2srgb(color[2]),
    )
