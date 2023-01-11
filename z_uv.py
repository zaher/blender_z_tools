"""Module Blender Z Tools."""
#* https://docs.blender.org/api/2.79/bpy.ops.object.html
#* https://blenderartists.org/t/renaming-bone-script/1299862/5

import bpy
from bpy.types import Operator
from bpy.props import FloatVectorProperty
#from bpy_extras.object_utils import AddObjectHelper, object_data_add
from mathutils import Vector

class UV_Z_Tools(bpy.types.Menu):
    bl_idname = "UV_Z_Tools" #same as class name
    bl_label = "Z Tools"

    def draw(self, context):
        layout = self.layout

def UV_Z_Tools_menu(self, context):
    self.layout.menu(
        UV_Z_Tools.bl_idname,
        text=UV_Z_Tools.bl_label
    )

class UV_align(Operator):

    bl_idname = "uv.zt_align"
    bl_label = "Align"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        if not bpy.context.active_object:
            return False

        #Only in Edit mode
        if bpy.context.active_object.mode != 'EDIT':
            return False

        #Only in UV editor mode
        if bpy.context.area.type != 'IMAGE_EDITOR':
            return False

        #Requires UV map
        if not bpy.context.object.data.uv_layers:
            return False 	#self.report({'WARNING'}, "Object must have more than one UV map")

        # Not in Synced mode
        if bpy.context.scene.tool_settings.use_uv_select_sync:
            return False

        return True

    def draw(self, context):
        layout = self.layout

        layout.operator("wm.open_mainfile")
        layout.operator("wm.save_as_mainfile")

    def execute(self, context):
        #align(context, self.direction)
        return {'FINISHED'}

def UV_align_menu(self, context):
    self.layout.operator(
        UV_align.bl_idname,
        text=UV_align.bl_label
    )

## Registration

def register():
    bpy.utils.register_class(UV_Z_Tools)
    bpy.types.IMAGE_MT_uvs.append(UV_Z_Tools_menu)

    bpy.utils.register_class(UV_align)
    bpy.types.UV_Z_Tools.append(UV_align_menu)

def unregister():
    bpy.types.UV_Z_Tools.remove(UV_align_menu)
    bpy.utils.unregister_class(UV_align)

    bpy.types.IMAGE_MT_uvs.remove(UV_Z_Tools_menu)
    bpy.utils.unregister_class(UV_Z_Tools)
