from ..materials import BASE_MATERIAL_COLORS, BASE_MATERIALS, BASE_MATERIAL_VARIANTS
from ..core import Material, srgb2lin
from .custom_node_utils import *

import bpy
from bpy.props import EnumProperty, BoolProperty

from nodeitems_utils import NodeItem
from nodeitems_builtins import ShaderNodeCategory

def setup_principled_bsdf(self: Material, node_shader: bpy.types.ShaderNodeBsdfPrincipled):
    node_shader.inputs["Base Color"].default_value = (*srgb2lin(self.diffuse), 1.0)
    node_shader.inputs["Alpha"].default_value = self.alpha
    node_shader.inputs["Metallic"].default_value = self.metallic
    node_shader.inputs["Roughness"].default_value = self.roughness
    node_shader.inputs["Subsurface"].default_value = self.subsurface_mm * 0.001
    node_shader.inputs["Transmission"].default_value = self.transmission
    node_shader.inputs["Transmission Roughness"].default_value = self.transmission_roughness
    node_shader.inputs["IOR"].default_value = self.ior
    node_shader.inputs["Emission"].default_value = (*self.emission, 1.0)
    node_shader.inputs["Clearcoat"].default_value = self.clearcoat
    node_shader.inputs["Clearcoat Roughness"].default_value = self.clearcoat_roughness

    if self.subsurface_radius is not None:
        node_shader.inputs["Subsurface Color"].default_value = (*srgb2lin(self.diffuse), 1.0)
        node_shader.inputs["Subsurface Radius"].default_value = self.subsurface_radius

def setup_node_tree(self: Material, node_tree: bpy.types.NodeTree, force_principled=False):
    node_tree.nodes.clear()
    if self.base and not force_principled:
        node_shader = node_tree.nodes.new("ShaderNodeBsdfMat4cad")
        node_shader.mat_base = self.base.upper()
        node_shader.mat_color = self.color.upper()
        node_shader.mat_variant = self.variant.upper()
    else:
        node_shader = node_tree.nodes.new("ShaderNodeBsdfPrincipled")
        self.setup_principled_bsdf(node_shader)

        node_bevel = node_tree.nodes.new("ShaderNodeBevel")
        node_bevel.location = (-180, -530.5)
        node_bevel.inputs["Radius"].default_value = self.bevel_mm * 0.001
        node_tree.links.new(node_shader.inputs["Normal"], node_bevel.outputs[0])

    node_output = node_tree.nodes.new("ShaderNodeOutputMaterial")
    node_output.location = (300, 0)
    node_tree.links.new(node_output.inputs["Surface"], node_shader.outputs[0])

    return node_tree

setattr(Material, setup_principled_bsdf.__name__, setup_principled_bsdf)
setattr(Material, setup_node_tree.__name__, setup_node_tree)

class ShaderNodeBsdfMat4cad(CustomNodetreeNodeBase, bpy.types.ShaderNodeCustomGroup):
    bl_label = "Mat4cad BSDF"
    bl_width_default = 140

    @staticmethod
    def mat_base_items():
        return tuple(zip(
            (key.upper() for key in BASE_MATERIALS.keys()),
            BASE_MATERIALS.keys(),
            ("",) * len(BASE_MATERIALS)
        ))

    def mat_color_items(self, context):
        colors = BASE_MATERIAL_COLORS[self.mat_base.lower()]
        return tuple(zip(
            (key.upper() for key in colors.keys()),
            colors.keys(),
            ("",) * len(colors),
        ))

    def mat_variant_items(self, context):
        variants = BASE_MATERIAL_VARIANTS[self.mat_base.lower()]
        return tuple(zip(
            (key.upper() for key in variants.keys()),
            variants.keys(),
            ("",) * len(variants),
        ))

    def update_props(self, context):
        if not self.mat_color:
            self.mat_color = self.mat_color_items(context)[0][0]
        if not self.mat_variant:
            self.mat_variant = self.mat_variant_items(context)[0][0]

        material = self.get_material()
        material.setup_principled_bsdf(self.node_tree.nodes["shader"])
        self.update_bevel(context)

    mat_base: EnumProperty(name="Base Material", update=update_props,
        items=mat_base_items())

    mat_color: EnumProperty(name="Color", update=update_props,
        items=mat_color_items)

    mat_variant: EnumProperty(name="Variant", update=update_props,
        items=mat_variant_items)

    def update_bevel(self, context):
        material = self.get_material()
        bevel = material.bevel_mm * 0.001 if self.use_bevel else 0
        self.node_tree.nodes["bevel"].inputs["Radius"].default_value = bevel

    use_bevel: BoolProperty(name="Bevel", update=update_bevel, default=True)

    def init(self, context):
        inputs = {
            "Normal": ("NodeSocketVector", {"hide_value": True}),
        }

        nodes = {
            "bevel": ("ShaderNodeBevel", {}, {"Normal": ("inputs", "Normal")}),
            "shader": ("ShaderNodeBsdfPrincipled", {}, {"Normal": ("bevel", 0)}),
        }

        outputs = {
            "BSDF": ("NodeSocketShader", {}, ("shader", 0)),
        }

        self.init_node_tree(inputs, nodes, outputs)
        self.update_props(context)
        self.update_bevel(context)

    def get_material(self):
        material_name = "-".join((self.mat_base, self.mat_color, self.mat_variant)).lower()
        return Material.from_name(material_name)

shader_node_category = ShaderNodeCategory("SH_NEW_MAT4CAD", "Mat4cad", items=(
    NodeItem("ShaderNodeBsdfMat4cad"),
))

classes = (
    ShaderNodeBsdfMat4cad,
)

def register():
    bpy.utils.register_class(ShaderNodeBsdfMat4cad)
    register_node_category("SHADER", shader_node_category)

def unregister():
    unregister_node_category("SHADER", shader_node_category)
    bpy.utils.unregister_class(ShaderNodeBsdfMat4cad)
