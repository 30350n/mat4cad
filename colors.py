from .core import hex2rgb

RAL_COLORS = {
    "mouse_grey":             hex2rgb("6b6e6b"),
    "pure_white":             hex2rgb("f0ede1"),
    "jet_black":              hex2rgb("0e0e10"),
    "signal_yellow":          hex2rgb("f2a900"),
    "signal_orange":          hex2rgb("cc5d29"),
    "signal_red":             hex2rgb("982323"),
    "signal_violet":          hex2rgb("874b83"),
    "signal_blue":            hex2rgb("005187"),
    "signal_green":           hex2rgb("1c8051"),
    "signal_grey":            hex2rgb("9b9b9b"),
    "signal_brown":           hex2rgb("774d3e"),
    "signal_white":           hex2rgb("ecece7"),
    "signal_black":           hex2rgb("2b2b2c"),

    "green_beige":            hex2rgb("c9bb88"),
    "beige":                  hex2rgb("ccb083"),
    "sand_yellow":            hex2rgb("cdaa6d"),
    "signal_yellow":          hex2rgb("f2a900"),
    "golden_yellow":          hex2rgb("dd9f00"),
    "honey_yellow":           hex2rgb("c58f00"),
    "maize_yellow":           hex2rgb("db9100"),
    "daffodil_yellow":        hex2rgb("e28d00"),
    "brown_beige":            hex2rgb("ab814f"),
    "lemon_yellow":           hex2rgb("d6b025"),
    "oyster_white":           hex2rgb("e1dac7"),
    "ivory":                  hex2rgb("d9c59a"),
    "light_ivory":            hex2rgb("e3d3b5"),
    "sulfur_yellow":          hex2rgb("e8de35"),
    "saffron_yellow":         hex2rgb("f0aa50"),
    "zinc_yellow":            hex2rgb("f2cb2e"),
    "grey_beige":             hex2rgb("a28f7a"),
    "olive_yellow":           hex2rgb("9d8f65"),
    "rope_yellow":            hex2rgb("eeb700"),
    "traffic_yellow":         hex2rgb("efb700"),
    "ochre_yellow":           hex2rgb("b5904b"),
    "luminous_yellow":        hex2rgb("ffff00"),
    "curry":                  hex2rgb("a2800c"),
    "melon_yellow":           hex2rgb("ff9c00"),
    "broom_yellow":           hex2rgb("dba400"),
    "dahlia_yellow":          hex2rgb("f39b1b"),
    "pastel_yellow":          hex2rgb("e69d51"),
    "pearl_beige":            hex2rgb("8e8370"),
    "pearl_gold":             hex2rgb("7d653f"),
    "sun_yellow":             hex2rgb("ea9300"),

    "yellow_orange":          hex2rgb("d56f00"),
    "red_orange":             hex2rgb("b6481c"),
    "vermilion":              hex2rgb("bc3823"),
    "pastel_orange":          hex2rgb("f17829"),
    "pure_orange":            hex2rgb("de5306"),
    "luminous_orange":        hex2rgb("ff4b11"),
    "luminous_bright_orange": hex2rgb("ffb700"),
    "bright_red_orange":      hex2rgb("e86b22"),
    "traffic_orange":         hex2rgb("da530a"),
    "signal_orange":          hex2rgb("cc5d29"),
    "deep_orange":            hex2rgb("dd6e0f"),
    "salmon_orange":          hex2rgb("d1654e"),
    "pearl_orange":           hex2rgb("8f3e26"),

    "flame_red":              hex2rgb("a42821"),
    "signal_red":             hex2rgb("982323"),
    "carmine_red":            hex2rgb("982222"),
    "ruby_red":               hex2rgb("841922"),
    "purple_red":             hex2rgb("691b23"),
    "wine_red":               hex2rgb("58181f"),
    "black_red":              hex2rgb("3d2022"),
    "oxide_red":              hex2rgb("663029"),
    "brown_red":              hex2rgb("772424"),
    "beige_red":              hex2rgb("c2856d"),
    "tomato_red":             hex2rgb("952e25"),
    "antique_pink":           hex2rgb("c97375"),
    "light_pink":             hex2rgb("d7a0a6"),
    "coral_red":              hex2rgb("a43c30"),
    "rose":                   hex2rgb("c8545d"),
    "strawberry_red":         hex2rgb("c43e4a"),
    "traffic_red":            hex2rgb("b81d13"),
    "salmon_pink":            hex2rgb("cc6955"),
    "luminous_red":           hex2rgb("ff2a24"),
    "luminous_bright_red":    hex2rgb("ff2620"),
    "raspberry_red":          hex2rgb("a9263d"),
    "pure_red":               hex2rgb("c92b26"),
    "orient_red":             hex2rgb("a43338"),
    "pearl_ruby_red":         hex2rgb("6e1c24"),
    "pearl_pink":             hex2rgb("a2392e"),

    "red_lilac":              hex2rgb("836083"),
    "red_violet":             hex2rgb("8c3c4b"),
    "heather_violet":         hex2rgb("c4608c"),
    "claret_violet":          hex2rgb("641d39"),
    "blue_lilac":             hex2rgb("7b679a"),
    "traffic_purple":         hex2rgb("913073"),
    "purple_violet":          hex2rgb("47243c"),
    "signal_violet":          hex2rgb("874b83"),
    "pastel_violet":          hex2rgb("9d8592"),
    "telemagenta":            hex2rgb("bb3e77"),
    "pearl_violet":           hex2rgb("716287"),
    "pearl_blackberry":       hex2rgb("6d6b7f"),

    "violet_blue":            hex2rgb("384e6f"),
    "green_blue":             hex2rgb("1d4c64"),
    "ultramarine_blue":       hex2rgb("1e367b"),
    "sapphire_blue":          hex2rgb("263855"),
    "black_blue":             hex2rgb("1a1e28"),
    "signal_blue":            hex2rgb("005187"),
    "brilliant_blue":         hex2rgb("426a8c"),
    "grey_blue":              hex2rgb("2d3a44"),
    "azure_blue":             hex2rgb("2d5e78"),
    "gentian_blue":           hex2rgb("004e7c"),
    "steel_blue":             hex2rgb("1e2b3d"),
    "light_blue":             hex2rgb("2e88b6"),
    "cobalt_blue":            hex2rgb("223053"),
    "pigeon_blue":            hex2rgb("687c96"),
    "sky_blue":               hex2rgb("0b7bb0"),
    "traffic_blue":           hex2rgb("005a8c"),
    "turquoise_blue":         hex2rgb("1b8b8c"),
    "capri_blue":             hex2rgb("0f5d84"),
    "ocean_blue":             hex2rgb("00414b"),
    "water_blue":             hex2rgb("007577"),
    "night_blue":             hex2rgb("2b2c5a"),
    "distant_blue":           hex2rgb("4a688d"),
    "pastel_blue":            hex2rgb("6792ac"),
    "pearl_gentian_blue":     hex2rgb("2c697c"),
    "pearl_night_blue":       hex2rgb("1b2f52"),

    "patina_green":           hex2rgb("3b7460"),
    "emerald_green":          hex2rgb("316834"),
    "leaf_green":             hex2rgb("2d5a27"),
    "olive_green":            hex2rgb("4e533b"),
    "blue_green":             hex2rgb("084442"),
    "moss_green":             hex2rgb("114232"),
    "grey_olive":             hex2rgb("3b392e"),
    "bottle_green":           hex2rgb("2a3222"),
    "brown_green":            hex2rgb("36342a"),
    "fir_green":              hex2rgb("27362a"),
    "grass_green":            hex2rgb("486f38"),
    "reseda_green":           hex2rgb("697d58"),
    "black_green":            hex2rgb("303d3a"),
    "reed_green":             hex2rgb("7a765a"),
    "yellow_olive":           hex2rgb("464135"),
    "black_olive":            hex2rgb("3c3d36"),
    "turquoise_green":        hex2rgb("006a4c"),
    "may_green":              hex2rgb("53803f"),
    "yellow_green":           hex2rgb("599a39"),
    "pastel_green":           hex2rgb("b7ceac"),
    "chrome_green":           hex2rgb("36422f"),
    "pale_green":             hex2rgb("879a77"),
    "olive_drab":             hex2rgb("393327"),
    "traffic_green":          hex2rgb("008450"),
    "fern_green":             hex2rgb("5a6e3b"),
    "opal_green":             hex2rgb("005f4e"),
    "light_green":            hex2rgb("80bab5"),
    "pine_green":             hex2rgb("305442"),
    "mint_green":             hex2rgb("00703c"),
    "signal_green":           hex2rgb("1c8051"),
    "mint_turquoise":         hex2rgb("48877f"),
    "pastel_turquoise":       hex2rgb("7cadac"),
    "pearl_green":            hex2rgb("134d24"),
    "pearl_opal_green":       hex2rgb("07584b"),
    "pure_green":             hex2rgb("008c27"),
    "luminous_green":         hex2rgb("00b612"),

    "squirrel_grey":          hex2rgb("7b888e"),
    "silver_grey":            hex2rgb("8e969d"),
    "olive_grey":             hex2rgb("7f7863"),
    "moss_grey":              hex2rgb("787769"),
    "signal_grey":            hex2rgb("9b9b9b"),
    "mouse_grey":             hex2rgb("6b6e6b"),
    "beige_grey":             hex2rgb("756a5e"),
    "khaki_grey":             hex2rgb("725f3c"),
    "green_grey":             hex2rgb("5c6058"),
    "tarpaulin_grey":         hex2rgb("585c56"),
    "iron_grey":              hex2rgb("53595d"),
    "basalt_grey":            hex2rgb("585d5e"),
    "brown_grey":             hex2rgb("565044"),
    "slate_grey":             hex2rgb("505359"),
    "anthracite_grey":        hex2rgb("383e42"),
    "black_grey":             hex2rgb("303234"),
    "umbra_grey":             hex2rgb("4c4a44"),
    "concrete_grey":          hex2rgb("7f8076"),
    "graphite_grey":          hex2rgb("46494f"),
    "granite_grey":           hex2rgb("384345"),
    "stone_grey":             hex2rgb("918e85"),
    "blue_grey":              hex2rgb("5d686d"),
    "pebble_grey":            hex2rgb("b4b0a1"),
    "cement_grey":            hex2rgb("7e8274"),
    "yellow_grey":            hex2rgb("90886f"),
    "light_grey":             hex2rgb("c5c7c4"),
    "platinum_grey":          hex2rgb("979392"),
    "dusty_grey":             hex2rgb("7a7b7a"),
    "agate_grey":             hex2rgb("afb1a9"),
    "quartz_grey":            hex2rgb("6a665e"),
    "window_grey":            hex2rgb("989ea1"),
    "traffic_grey_a":         hex2rgb("8e9291"),
    "traffic_grey_b":         hex2rgb("4f5250"),
    "silk_grey":              hex2rgb("b6b3a8"),
    "telegrey_1":             hex2rgb("8e9295"),
    "telegrey_2":             hex2rgb("7f868a"),
    "telegrey_4":             hex2rgb("c8c8c7"),
    "pearl_mouse_grey":       hex2rgb("807b73"),

    "green_brown":            hex2rgb("866a3e"),
    "ochre_brown":            hex2rgb("99632b"),
    "signal_brown":           hex2rgb("774d3e"),
    "clay_brown":             hex2rgb("7c4b27"),
    "copper_brown":           hex2rgb("8a4931"),
    "fawn_brown":             hex2rgb("6d462b"),
    "olive_brown":            hex2rgb("6f4a25"),
    "nut_brown":              hex2rgb("583827"),
    "red_brown":              hex2rgb("64332b"),
    "sepia_brown":            hex2rgb("483526"),
    "chestnut_brown":         hex2rgb("5d2f27"),
    "mahogany_brown":         hex2rgb("4b2b20"),
    "chocolate_brown":        hex2rgb("432f29"),
    "grey_brown":             hex2rgb("3d3635"),
    "black_brown":            hex2rgb("1a1719"),
    "orange_brown":           hex2rgb("a05729"),
    "beige_brown":            hex2rgb("765038"),
    "pale_brown":             hex2rgb("735847"),
    "terra_brown":            hex2rgb("4f3a2a"),
    "pearl_copper":           hex2rgb("7d4031"),

    "cream":                  hex2rgb("e7e1d2"),
    "grey_white":             hex2rgb("d6d5cb"),
    "signal_white":           hex2rgb("ecece7"),
    "signal_black":           hex2rgb("2b2b2c"),
    "jet_black":              hex2rgb("0e0e10"),
    "white_aluminium":        hex2rgb("a1a1a0"),
    "grey_aluminium":         hex2rgb("868581"),
    "pure_white":             hex2rgb("f0ede1"),
    "graphite_black":         hex2rgb("27292b"),
    "traffic_white":          hex2rgb("f0f1ea"),
    "traffic_black":          hex2rgb("2a292a"),
    "papyrus_white":          hex2rgb("c7cbc4"),
    "pearl_light_grey":       hex2rgb("858583"),
    "pearl_dark_grey":        hex2rgb("797b7b"),
}

PCB_COLORS = {
    "pcb_brown":       hex2rgb("452700"),
}

PCB_SUBSURFACE_COLORS = {
    "pcb_brown":       hex2rgb("1b120d"),
}

METAL_COLORS = {
    "steel":           hex2rgb("939595"),
    "iron":            hex2rgb("b9bcbc"),
    "silver":          hex2rgb("e7e5e1"),
    "gold":            hex2rgb("e7cd8c"),
    "brass":           hex2rgb("e1d388"),
    "copper":          hex2rgb("e1bbac"),
    "titanium":        hex2rgb("aaa39b"),
    "aluminium":       hex2rgb("e6e7e7"),
    "cobalt":          hex2rgb("bcbbb8"),
    "nickel":          hex2rgb("bcb4a9"),
    "tin":             hex2rgb("cbcac0"),
    "platinum":        hex2rgb("bcb7b0"),
}

ALL_COLORS = {**RAL_COLORS, **PCB_COLORS, **METAL_COLORS}

for name, color in ALL_COLORS.items():
    globals()[name.upper()] = color
