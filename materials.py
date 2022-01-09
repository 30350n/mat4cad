from .core import Material
from .colors import *

_PLASTIC_BASE       = Material(roughness=0.4)
_METAL_BASE         = Material(roughness=0.25, metallic=1.0)
_METAL_PAINTED_BASE = Material(roughness=0.4, clearcoat=1.0, clearcoat_roughness=0.4)
_PCB_BASE           = Material(roughness=0.4, subsurface=0.7)

(PLASTIC_JET_BLACK := _PLASTIC_BASE.copy()).diffuse = JET_BLACK
(PLASTIC_JET_BLACK_MATTE  := PLASTIC_JET_BLACK.copy()).roughness = 0.8
(PLASTIC_JET_BLACK_GLOSSY := PLASTIC_JET_BLACK.copy()).roughness = 0.2

(PLASTIC_MOUSE_GREY := _PLASTIC_BASE.copy()).diffuse = MOUSE_GREY
(PLASTIC_MOUSE_GREY_MATTE  := PLASTIC_MOUSE_GREY.copy()).roughness = 0.8
(PLASTIC_MOUSE_GREY_GLOSSY := PLASTIC_MOUSE_GREY.copy()).roughness = 0.2

(PLASTIC_TRAFFIC_WHITE := _PLASTIC_BASE.copy()).diffuse = TRAFFIC_WHITE
(PLASTIC_TRAFFIC_WHITE_MATTE  := PLASTIC_TRAFFIC_WHITE.copy()).roughness = 0.8
(PLASTIC_TRAFFIC_WHITE_GLOSSY := PLASTIC_TRAFFIC_WHITE.copy()).roughness = 0.2

(PLASTIC_MOSS_GREEN := _PLASTIC_BASE.copy()).diffuse = MOSS_GREEN
(PLASTIC_MOSS_GREEN_MATTE  := PLASTIC_MOSS_GREEN.copy()).roughness = 0.8
(PLASTIC_MOSS_GREEN_GLOSSY := PLASTIC_MOSS_GREEN.copy()).roughness = 0.2

(PLASTIC_SIGNAL_GREEN := _PLASTIC_BASE.copy()).diffuse = SIGNAL_GREEN
(PLASTIC_SIGNAL_GREEN_MATTE  := PLASTIC_SIGNAL_GREEN.copy()).roughness = 0.8
(PLASTIC_SIGNAL_GREEN_GLOSSY := PLASTIC_SIGNAL_GREEN.copy()).roughness = 0.2

PLASTIC_TRANSPARENT_DIFFUSED = Material(
    diffuse=MOUSE_GREY, ior=1.46, transmission=0.5, transmission_roughness=0.2, alpha=0.5)
PLASTIC_TRANSPARENT_CLEAR = PLASTIC_TRANSPARENT_DIFFUSED.copy()
PLASTIC_TRANSPARENT_CLEAR.transmission_roughness = 0.02

(METAL_BRIGHT := _METAL_BASE.copy()).diffuse = SIGNAL_GREY
(METAL_BRIGHT_MATTE  := METAL_BRIGHT.copy()).roughness = 0.6
(METAL_BRIGHT_GLOSSY := METAL_BRIGHT.copy()).roughness = 0.05

(METAL_DARK := _METAL_BASE.copy()).diffuse = MOUSE_GREY
(METAL_DARK_MATTE  := METAL_DARK.copy()).roughness = 0.6
(METAL_DARK_GLOSSY := METAL_DARK.copy()).roughness = 0.05

(METAL_BRASS := _METAL_BASE.copy()).diffuse = hex2rgb("b1a342")
(METAL_BRASS_MATTE  := METAL_BRASS.copy()).roughness = 0.6
(METAL_BRASS_GLOSSY := METAL_BRASS.copy()).roughness = 0.05

(METAL_PAINTED_JET_BLACK := _METAL_PAINTED_BASE.copy()).diffuse = JET_BLACK
(METAL_PAINTED_JET_BLACK_MATTE  := METAL_PAINTED_JET_BLACK.copy()).clearcoat_roughness = 0.75
(METAL_PAINTED_JET_BLACK_GLOSSY := METAL_PAINTED_JET_BLACK.copy()).clearcoat_roughness = 0.05

PCB_BROWN = _PCB_BASE.copy()
PCB_BROWN.diffuse = (0.059, 0.020, 0.0)
PCB_BROWN.subsurface_color = (0.011, 0.06, 0.004)

MATERIALS = {
    "plastic-jet_black-matte":         PLASTIC_JET_BLACK_MATTE,
    "plastic-jet_black":               PLASTIC_JET_BLACK,
    "plastic-jet_black-glossy":        PLASTIC_JET_BLACK_GLOSSY,
    
    "plastic-mouse_grey-matte":        PLASTIC_MOUSE_GREY_MATTE,
    "plastic-mouse_grey":              PLASTIC_MOUSE_GREY,
    "plastic-mouse_grey-glossy":       PLASTIC_MOUSE_GREY_GLOSSY,    
    
    "plastic-traffic_white-matte":     PLASTIC_TRAFFIC_WHITE_MATTE,
    "plastic-traffic_white":           PLASTIC_TRAFFIC_WHITE,
    "plastic-traffic_white-glossy":    PLASTIC_TRAFFIC_WHITE_GLOSSY,    
    
    "plastic-moss_green-matte":        PLASTIC_MOSS_GREEN_MATTE,
    "plastic-moss_green":              PLASTIC_MOSS_GREEN,
    "plastic-moss_green-glossy":       PLASTIC_MOSS_GREEN_GLOSSY,
    
    "plastic-signal_green-matte":      PLASTIC_SIGNAL_GREEN_MATTE,
    "plastic-signal_green":            PLASTIC_SIGNAL_GREEN,
    "plastic-signal_green-glossy":     PLASTIC_SIGNAL_GREEN_GLOSSY,
    
    "plastic-transparent-diffused":    PLASTIC_TRANSPARENT_DIFFUSED,
    "plastic-transparent-clear":       PLASTIC_TRANSPARENT_CLEAR,
    
    "metal-bright-matte":              METAL_BRIGHT_MATTE,
    "metal-bright":                    METAL_BRIGHT,
    "metal-bright-glossy":             METAL_BRIGHT_GLOSSY,
    
    "metal-dark-matte":                METAL_DARK_MATTE,
    "metal-dark":                      METAL_DARK,
    "metal-dark-glossy":               METAL_DARK_GLOSSY,

    "metal-brass-matte":               METAL_BRASS_MATTE,
    "metal-brass":                     METAL_BRASS,
    "metal-brass-glossy":              METAL_BRASS_GLOSSY,

    "metal_painted-black-matte":       METAL_PAINTED_JET_BLACK_MATTE,
    "metal_painted-black":             METAL_PAINTED_JET_BLACK,
    "metal_painted-black-glossy":      METAL_PAINTED_JET_BLACK_GLOSSY,

    "pcb-brown":                       PCB_BROWN,
}
