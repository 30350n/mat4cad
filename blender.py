from .core import Material, srgb2lin

import bpy

def setup_node_tree(self: Material, node_tree: bpy.types.NodeTree):
    node_tree.nodes.clear()

    node_shader = node_tree.nodes.new("ShaderNodeBsdfPrincipled")
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
        node_ssr = node_tree.nodes.new("ShaderNodeRGB")
        node_ssr.location = (-180, -120)
        node_ssr.outputs[0].default_value = (*self.subsurface_radius, 1.0)
        node_tree.links.new(node_shader.inputs["Subsurface Radius"], node_ssr.outputs[0])

    node_output = node_tree.nodes.new("ShaderNodeOutputMaterial")
    node_output.location = (300, 0)
    node_tree.links.new(node_output.inputs["Surface"], node_shader.outputs[0])

    node_bevel = node_tree.nodes.new("ShaderNodeBevel")
    node_bevel.location = (-180, -530.5)
    node_bevel.inputs["Radius"].default_value = self.bevel_mm * 0.001
    node_tree.links.new(node_shader.inputs["Normal"], node_bevel.outputs[0])

    return node_tree

setattr(Material, setup_node_tree.__name__, setup_node_tree)
