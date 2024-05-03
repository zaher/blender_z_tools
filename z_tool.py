"""Module Blender Z Tools."""
#* https://docs.blender.org/api/2.79/bpy.ops.object.html
#* https://blenderartists.org/t/renaming-bone-script/1299862/5

import bpy
from bpy.types import Operator
from bpy.props import FloatVectorProperty
#from bpy_extras.object_utils import AddObjectHelper, object_data_add
from mathutils import Vector

class OBJECT_OT_C2Mesh_modifier(bpy.types.Operator):
    bl_idname = "object.convert_to_mesh"
    bl_label = "Convert To Mesh"
    bl_description = "Convert Curve to Mesh"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        obj = context.object
        mod = obj.modifiers.new(name="ConvertToMesh", type='SUBSURF')
        mod.levels = 2
        return {'FINISHED'}

## Registration

def register():
    bpy.utils.register_class(OBJECT_OT_C2Mesh_modifier)

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_C2Mesh_modifier)