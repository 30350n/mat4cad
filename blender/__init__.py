from dataclasses import fields
from typing import Literal, cast, overload

import bpy
from bl_ui import node_add_menu
from bpy.props import BoolProperty, EnumProperty
from bpy.types import (
    NodeSocketColor,
    NodeSocketFloat,
    NodeSocketShader,
    NodeSocketVector,
)
from mathutils import Vector

from ..core import Material, hex2rgb, lin2srgb, rgb2hex, srgb2lin
from ..materials import BASE_MATERIAL_COLORS, BASE_MATERIAL_VARIANTS, BASE_MATERIALS
from .custom_node_utils import (
    CustomNodetreeNodeBase,
    InputsDef,
    NodesDef,
    OutputsDef,
    SharedCustomNodetreeNodeBase,
)


class BlenderMaterial(Material):
    def setup_principled_bsdf(self, node_shader: bpy.types.ShaderNodeBsdfPrincipled):
        node_shader.inputs["Base Color"].default_value = (*srgb2lin(self.diffuse), 1.0)
        node_shader.inputs["Alpha"].default_value = self.alpha
        node_shader.inputs["Metallic"].default_value = self.metallic
        node_shader.inputs["Roughness"].default_value = self.roughness
        node_shader.inputs["Subsurface Weight"].default_value = self.subsurface_mm * 0.001
        node_shader.inputs["Transmission Weight"].default_value = self.transmission
        node_shader.inputs["IOR"].default_value = self.ior
        node_shader.inputs["Emission Strength"].default_value = self.emission_strength
        node_shader.inputs["Emission Color"].default_value = (*self.emission_color, 1.0)
        node_shader.inputs["Coat Weight"].default_value = self.coat
        node_shader.inputs["Coat Roughness"].default_value = self.coat_roughness

        if self.subsurface_radius is not None:
            node_shader.inputs["Subsurface Radius"].default_value = self.subsurface_radius

    def setup_node_tree(self, node_tree: bpy.types.NodeTree, force_principled: bool = False):
        node_tree.nodes.clear()

        if self.base and self.variant and not force_principled:
            node_mat4cad = cast(ShaderNodeBsdfMat4cad, node_tree.nodes.new("ShaderNodeBsdfMat4cad"))
            shader_output = node_mat4cad.outputs[0]
            node_mat4cad.mat_base = self.base.upper()
            node_mat4cad.mat_variant = self.variant.upper()

            if self.has_custom_color:
                node_mat4cad.mat_color = "CUSTOM"
                node_mat4cad.inputs["Color"].default_value = (*srgb2lin(self.diffuse), 1.0)
            else:
                assert self.color
                node_mat4cad.mat_color = self.color.upper()
        else:
            node_shader = node_tree.nodes.new("ShaderNodeBsdfPrincipled")
            shader_output = node_shader.outputs[0]
            self.setup_principled_bsdf(node_shader)

            node_bevel = node_tree.nodes.new("ShaderNodeBevel")
            node_bevel.location = (-180, -530.5)
            node_bevel.inputs["Radius"].default_value = self.bevel_mm * 0.001
            node_tree.links.new(node_shader.inputs["Normal"], node_bevel.outputs[0])

        node_output = node_tree.nodes.new("ShaderNodeOutputMaterial")
        node_output.location = (300, 0)
        node_tree.links.new(node_output.inputs["Surface"], shader_output)

        return node_tree

    @classmethod
    def from_name(cls, name: str):
        if not (material := Material.from_name(name)):
            return None
        return BlenderMaterial(**{f.name: getattr(material, f.name) for f in fields(material)})


class ShaderNodeBsdfMat4cad(CustomNodetreeNodeBase):
    bl_label = "Mat4cad BSDF"
    bl_width_default = 180

    @staticmethod
    def mat_base_items():
        mats = BASE_MATERIALS
        return tuple(zip((name.upper() for name in mats), mats, ("",) * len(mats)))

    def mat_color_items(self, context: bpy.types.Context | None):
        colors = ("custom", *BASE_MATERIAL_COLORS[self.mat_base.lower()].keys())
        return tuple(zip((name.upper() for name in colors), colors, ("",) * len(colors)))

    def mat_variant_items(self, context: bpy.types.Context | None):
        variants = BASE_MATERIAL_VARIANTS[self.mat_base.lower()] or {"default": {}}
        return tuple(zip((name.upper() for name in variants), variants, ("",) * len(variants)))

    def update_props(self, context: bpy.types.Context):
        if not self.mat_color:
            self.mat_color = self.mat_color_items(context)[1][0]
        if not self.mat_variant:
            self.mat_variant = self.mat_variant_items(context)[0][0]

        material = self.mat4cad_material
        material.setup_principled_bsdf(self.node_shader)

        self.inputs["Color"].default_value = (*srgb2lin(material.diffuse), 1.0)
        self.inputs["Color"].hide = not material.has_custom_color

        self.node_metallic.outputs[0].default_value = material.metallic
        self.node_roughness.outputs[0].default_value = material.roughness

        assert (node_tree := self.node_tree)
        node_tree.name = f"MAT4CAD_{material.name}"

        self.update_bevel(context)

    mat_base: EnumProperty(name="Base", update=update_props, items=mat_base_items())
    mat_color: EnumProperty(name="Color", update=update_props, items=mat_color_items)
    mat_variant: EnumProperty(name="Variant", update=update_props, items=mat_variant_items)

    def update_bevel(self, context: bpy.types.Context):
        bevel = self.mat4cad_material.bevel_mm * 0.001 if self.use_bevel else 0
        self.node_bevel.inputs["Radius"].default_value = bevel

    use_bevel: BoolProperty(name="Bevel", update=update_bevel, default=True)

    @property
    def mat4cad_material(self):
        color = self.mat_color
        if color == "CUSTOM":
            color = "custom_" + rgb2hex(lin2srgb(self.inputs["Color"].default_value[:3]))
        material_name = "-".join((self.mat_base, color, self.mat_variant)).lower()
        assert (material := BlenderMaterial.from_name(material_name))
        return material

    @property
    def node_shader(self):
        assert (node_tree := self.node_tree)
        assert (node := node_tree.nodes["shader"])
        return cast(bpy.types.ShaderNodeBsdfPrincipled, node)

    @property
    def node_bevel(self):
        assert (node_tree := self.node_tree) and (node := node_tree.nodes["bevel"])
        return cast(bpy.types.ShaderNodeBevel, node)

    @property
    def node_metallic(self):
        assert (node_tree := self.node_tree) and (node := node_tree.nodes["metallic"])
        return cast(bpy.types.ShaderNodeValue, node)

    @property
    def node_roughness(self):
        assert (node_tree := self.node_tree) and (node := node_tree.nodes["roughness"])
        return cast(bpy.types.ShaderNodeValue, node)

    def init(self, context: bpy.types.Context):
        inputs: InputsDef = {
            "Color": ("NodeSocketColor", {"default_value": (0.5, 0.5, 0.5, 1.0)}),
            "Texture Strength": ("NodeSocketFloat", {"default_value": 0.5}),
            "Scratches": ("NodeSocketFloat", {"default_value": 0.5}),
            "Normal": ("NodeSocketVector", {"hide_value": True}),
        }

        nodes: NodesDef = {
            "metallic": ("ShaderNodeValue", {}, {}),
            "roughness": ("ShaderNodeValue", {}, {}),
            "tex_strength_metal_fac": (
                "ShaderNodeMath",
                {"operation": "MULTIPLY_ADD"},
                {0: ("metallic", 0), 1: -3.0, 2: 4.5},
            ),
            "tex_strength_rough_fac": (
                "ShaderNodeMath",
                {"operation": "MULTIPLY_ADD"},
                {0: ("roughness", 0), 1: ("tex_strength_metal_fac", 0), 2: 0.5},
            ),
            "tex_strength": (
                "ShaderNodeMath",
                {"operation": "MULTIPLY"},
                {0: ("inputs", "Texture Strength"), 1: ("tex_strength_rough_fac", 0)},
            ),
            "scale_rough_fac": (
                "ShaderNodeMath",
                {"operation": "MULTIPLY_ADD"},
                {0: ("roughness", 0), 1: 1, 2: 0.5},
            ),
            "tex_coord": ("ShaderNodeTexCoord", {}, {}),
            "object_info": ("ShaderNodeObjectInfo", {}, {}),
            "scale_rough_fac_random": (
                "ShaderNodeMath",
                {"operation": "ADD"},
                {0: ("scale_rough_fac", 0), 1: ("object_info", "Random")},
            ),
            "with_noise": (
                "ShaderNodeMat4cadNoise",
                {},
                {
                    "Roughness": ("roughness", 0),
                    "Normal": ("inputs", "Normal"),
                    "Strength": ("tex_strength", 0),
                    "Vector": ("tex_coord", "Object"),
                    "Scale": ("scale_rough_fac_random", 0),
                },
            ),
            "with_scratches": (
                "ShaderNodeMat4cadScratches",
                {},
                {
                    "Color": ("inputs", "Color"),
                    "Roughness": ("with_noise", "Roughness"),
                    "Normal": ("with_noise", "Normal"),
                    "Strength": ("tex_strength", 0),
                    "Amount": ("inputs", "Scratches"),
                    "Vector": ("tex_coord", "Object"),
                    "Scale": ("scale_rough_fac_random", 0),
                },
            ),
            "bevel": ("ShaderNodeBevel", {"samples": 4}, {"Normal": ("with_scratches", "Normal")}),
            "shader": (
                "ShaderNodeBsdfPrincipled",
                {},
                {
                    "Base Color": ("with_scratches", "Color"),
                    "Metallic": ("metallic", 0),
                    "Roughness": ("with_scratches", "Roughness"),
                    "Normal": ("bevel", 0),
                },
            ),
        }

        outputs: OutputsDef = {
            "BSDF": ("NodeSocketShader", {}, ("shader", 0)),
        }

        self.init_node_tree(inputs, nodes, outputs)
        self.mat_color = self.mat_color_items(context)[1][0]
        self.update_props(context)
        self.update_bevel(context)

    class NodeInputs(bpy.types.NodeInputs):
        @overload
        def __getitem__(self, key: Literal[0] | Literal["Color"]) -> NodeSocketColor: ...  # pyright: ignore[reportNoOverloadImplementation]
        @overload
        def __getitem__(self, key: Literal[1] | Literal["Texture Strength"]) -> NodeSocketFloat: ...
        @overload
        def __getitem__(self, key: Literal[2] | Literal["Scratches"]) -> NodeSocketFloat: ...
        @overload
        def __getitem__(self, key: Literal[3] | Literal["Normal"]) -> NodeSocketVector: ...  # pyright: ignore[reportIncompatibleMethodOverride]

    inputs: NodeInputs  # pyright: ignore[reportIncompatibleVariableOverride]

    class NodeOutputs(bpy.types.NodeOutputs):
        def __getitem__(self, key: Literal[0] | Literal["BSDF"]) -> NodeSocketShader: ...  # pyright: ignore[reportIncompatibleMethodOverride]

    outputs: NodeOutputs  # pyright: ignore[reportIncompatibleVariableOverride]


class ShaderNodeMat4cadNoise(SharedCustomNodetreeNodeBase):
    bl_label = "Mat4cad Noise"
    bl_width_default = 140

    def init(self, context: bpy.types.Context):
        inputs: InputsDef = {
            "Roughness": ("NodeSocketFloat", {"hide_value": True, "default_value": 0.5}),
            "Normal": ("NodeSocketVector", {"hide_value": True}),
            "Strength": ("NodeSocketFloat", {"default_value": 0.5}),
            "Vector": ("NodeSocketVector", {"hide_value": True}),
            "Scale": ("NodeSocketFloat", {"default_value": 0.5}),
        }

        nodes: NodesDef = {
            "noise_scale": (
                "ShaderNodeMath",
                {"operation": "MULTIPLY"},
                {0: ("inputs", "Scale"), 1: 80},
            ),
            "noise": (
                "ShaderNodeTexNoise",
                {},
                {
                    "Vector": ("inputs", "Vector"),
                    "Scale": ("noise_scale", 0),
                    "Detail": 8.0,
                    "Roughness": 0.55,
                    "Distortion": 0.1,
                },
            ),
            "noise_mapped": (
                "ShaderNodeMapRange",
                {},
                {"Value": ("noise", "Fac"), "From Min": 0.4, "From Max": 0.6},
            ),
            "roughness_range": (
                "ShaderNodeMath",
                {"operation": "MULTIPLY"},
                {0: ("inputs", "Strength"), 1: 0.1},
            ),
            "roughness_min": (
                "ShaderNodeMath",
                {"operation": "SUBTRACT"},
                {0: ("inputs", "Roughness"), 1: ("roughness_range", 0)},
            ),
            "roughness_max": (
                "ShaderNodeMath",
                {"operation": "ADD"},
                {0: ("inputs", "Roughness"), 1: ("roughness_range", 0)},
            ),
            "roughness_mapped": (
                "ShaderNodeMapRange",
                {},
                {
                    "Value": ("noise_mapped", 0),
                    "From Min": 0.2,
                    "From Max": 0.8,
                    "To Min": ("roughness_min", 0),
                    "To Max": ("roughness_max", 0),
                },
            ),
            "bump_strength": (
                "ShaderNodeMath",
                {"operation": "MULTIPLY"},
                {0: ("inputs", "Strength"), 1: 0.02},
            ),
            "bump": (
                "ShaderNodeBump",
                {},
                {
                    "Normal": ("inputs", "Normal"),
                    "Strength": ("bump_strength", 0),
                    "Height": ("noise_mapped", 0),
                },
            ),
        }

        outputs: OutputsDef = {
            "Roughness": ("NodeSocketFloat", {}, ("roughness_mapped", 0)),
            "Normal": ("NodeSocketVector", {}, ("bump", 0)),
        }

        self.init_node_tree(inputs, nodes, outputs)


class ShaderNodeMat4cadScratches(SharedCustomNodetreeNodeBase):
    bl_label = "Mat4cad Scratches"
    bl_width_default = 140

    COLOR_WORN = srgb2lin(hex2rgb("A0A060"))

    def init(self, context: bpy.types.Context):
        inputs: InputsDef = {
            "Color": (
                "NodeSocketColor",
                {"hide_value": True, "default_value": (0.5, 0.5, 0.5, 1.0)},
            ),
            "Roughness": ("NodeSocketFloat", {"hide_value": True, "default_value": 0.5}),
            "Normal": ("NodeSocketVector", {"hide_value": True}),
            "Strength": ("NodeSocketFloat", {"default_value": 0.5}),
            "Amount": ("NodeSocketFloat", {"default_value": 0.5}),
            "Vector": ("NodeSocketVector", {"hide_value": True}),
            "Scale": ("NodeSocketFloat", {"default_value": 0.5}),
        }

        nodes: NodesDef = {
            "tex_coord": ("ShaderNodeTexCoord", {}, {}),
            "edges_bevel": (
                "ShaderNodeBevel",
                {"samples": 2},
                {"Radius": 0.0005, "Normal": ("tex_coord", "Normal")},
            ),
            "edges": (
                "ShaderNodeVectorMath",
                {"operation": "DISTANCE"},
                {0: ("edges_bevel", 0), 1: ("tex_coord", "Normal")},
            ),
            "edges_scaled": (
                "ShaderNodeMath",
                {"operation": "MULTIPLY"},
                {0: ("edges", "Value"), 1: ("inputs", "Strength")},
            ),
            "noise_tex_coord_scale": (
                "ShaderNodeMath",
                {"operation": "MULTIPLY"},
                {0: ("inputs", "Scale"), 1: 150},
            ),
            "noise_tex_coord": (
                "ShaderNodeTexVoronoi",
                {},
                {"Vector": ("inputs", "Vector"), "Scale": ("noise_tex_coord_scale", 0)},
            ),
            "scratches_tex_coord": (
                "ShaderNodeVectorMath",
                {"operation": "SUBTRACT"},
                {0: ("noise_tex_coord", "Position"), 1: ("inputs", "Vector")},
            ),
            "tex_coord_randomized": (
                "ShaderNodeVectorMath",
                {"operation": "ADD"},
                {0: ("scratches_tex_coord", 0), 1: ("noise_tex_coord", "Color")},
            ),
            "noise_scale": (
                "ShaderNodeMath",
                {"operation": "MULTIPLY"},
                {0: ("inputs", "Scale"), 1: 90},
            ),
            "noise1": (
                "ShaderNodeTexNoise",
                {},
                {
                    "Vector": ("tex_coord_randomized", "Vector"),
                    "Scale": ("noise_scale", 0),
                    "Detail": 8.0,
                    "Roughness": 0.4,
                    "Distortion": 2.9,
                },
            ),
            "scratches1_offset": (
                "ShaderNodeMath",
                {"operation": "SUBTRACT"},
                {0: ("noise1", "Fac"), 1: 0.5},
            ),
            "scratches1_abs": (
                "ShaderNodeMath",
                {"operation": "ABSOLUTE"},
                {0: ("scratches1_offset", 0)},
            ),
            "noise2": (
                "ShaderNodeTexVoronoi",
                {"feature": "DISTANCE_TO_EDGE"},
                {"Vector": ("tex_coord_randomized", "Vector"), "Scale": ("noise_scale", 0)},
            ),
            "scratches_layered": (
                "ShaderNodeMath",
                {"operation": "MULTIPLY"},
                {0: ("scratches1_abs", 0), 1: ("noise2", "Distance")},
            ),
            "scratches_separate": (
                "ShaderNodeTexVoronoi",
                {"feature": "DISTANCE_TO_EDGE"},
                {"Vector": ("inputs", "Vector"), "Scale": ("noise_tex_coord_scale", 0)},
            ),
            "scratches_separated": (
                "ShaderNodeMath",
                {"operation": "DIVIDE"},
                {0: ("scratches_layered", 0), 1: ("scratches_separate", "Distance")},
            ),
            "scratches_scaled": (
                "ShaderNodeMapRange",
                {},
                {
                    "Value": ("scratches_separated", 0),
                    "From Max": 0.0001,
                    "To Min": 1.0,
                    "To Max": 0.0,
                },
            ),
            "noise_filter_scale": (
                "ShaderNodeMath",
                {"operation": "MULTIPLY"},
                {0: ("inputs", "Scale"), 1: 170},
            ),
            "noise_filter": (
                "ShaderNodeTexNoise",
                {},
                {
                    "Vector": ("inputs", "Vector"),
                    "Scale": ("noise_filter_scale", 0),
                    "Detail": 8.0,
                    "Roughness": 0.55,
                    "Distortion": 0.1,
                },
            ),
            "noise_filter_edges": (
                "ShaderNodeMath",
                {"operation": "MULTIPLY_ADD"},
                {0: ("edges_scaled", 0), 1: 1.5, 2: ("noise_filter", "Fac")},
            ),
            "roughness_fac": (
                "ShaderNodeMath",
                {"operation": "MULTIPLY_ADD"},
                {0: ("inputs", "Roughness"), 1: 0.6, 2: 0.1},
            ),
            "amount": (
                "ShaderNodeMath",
                {"operation": "MULTIPLY_ADD"},
                {0: ("inputs", "Amount"), 1: ("roughness_fac", 0), 2: -0.7},
            ),
            "scratches_filter": (
                "ShaderNodeMath",
                {"operation": "ADD", "use_clamp": True},
                {0: ("noise_filter_edges", 0), 1: ("amount", 0)},
            ),
            "scratches_filtered": (
                "ShaderNodeMath",
                {"operation": "MULTIPLY"},
                {0: ("scratches_scaled", 0), 1: ("scratches_filter", 0)},
            ),
            "color_worn_fac": (
                "ShaderNodeMath",
                {"operation": "MULTIPLY"},
                {0: ("edges_scaled", 0), 1: 3.0},
            ),
            "mix_color_worn": (
                "ShaderNodeMixRGB",
                {"blend_type": "DODGE"},
                {
                    "Color1": ("inputs", "Color"),
                    "Color2": Vector((*self.COLOR_WORN, 1)),
                    "Fac": ("color_worn_fac", 0),
                },
            ),
            "mix_color_scratches": (
                "ShaderNodeMixRGB",
                {"blend_type": "DARKEN"},
                {
                    "Color1": ("mix_color_worn", 0),
                    "Color2": Vector((0.2, 0.2, 0.2, 1.0)),
                    "Fac": ("scratches_filtered", 0),
                },
            ),
            "roughness_worn": (
                "ShaderNodeMath",
                {"operation": "ADD"},
                {0: ("inputs", "Roughness"), 1: ("edges_scaled", 0)},
            ),
            "bump_strength": (
                "ShaderNodeMath",
                {"operation": "MULTIPLY"},
                {0: ("inputs", "Strength"), 1: ("roughness_fac", 0)},
            ),
            "bump": (
                "ShaderNodeBump",
                {"invert": True},
                {
                    "Normal": ("inputs", "Normal"),
                    "Strength": ("bump_strength", 0),
                    "Height": ("scratches_filtered", 0),
                },
            ),
        }

        outputs: OutputsDef = {
            "Color": ("NodeSocketColor", {}, ("mix_color_scratches", 0)),
            "Roughness": ("NodeSocketFloat", {}, ("roughness_worn", 0)),
            "Normal": ("NodeSocketVector", {}, ("bump", 0)),
        }

        self.init_node_tree(inputs, nodes, outputs)


class NODE_MT_category_shader_mat4cad(bpy.types.Menu):
    bl_idname = "NODE_MT_category_shader_mat4cad"
    bl_label = "Mat4Cad"

    def draw(self, context: bpy.types.Context):
        layout = self.layout

        node_add_menu.add_node_type(layout, "ShaderNodeBsdfMat4cad")
        node_add_menu.add_node_type(layout, "ShaderNodeMat4cadNoise")
        node_add_menu.add_node_type(layout, "ShaderNodeMat4cadScratches")

        node_add_menu.draw_assets_for_catalog(layout, self.bl_label)


def menu_draw(self: bpy.types.Menu, context: bpy.types.Context):
    assert self.layout
    self.layout.separator()
    self.layout.menu("NODE_MT_category_shader_mat4cad")


classes = (
    ShaderNodeBsdfMat4cad,
    ShaderNodeMat4cadNoise,
    ShaderNodeMat4cadScratches,
    NODE_MT_category_shader_mat4cad,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.NODE_MT_shader_node_add_all.append(menu_draw)


def unregister():
    bpy.types.NODE_MT_shader_node_add_all.remove(menu_draw)

    for cls in classes:
        bpy.utils.unregister_class(cls)
