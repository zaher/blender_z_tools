#* https://docs.blender.org/api/2.79/bpy.ops.object.html
#* https://blenderartists.org/t/renaming-bone-script/1299862/5

bl_info = {
    "name": "Ported Tools",
    "author": "Zaher Dirkey",
    "version": (1, 0),
    "blender": (2, 75, 0),
    "location": "View3D > Object > Ported Tools > ",
    "description": "Rename Bones",
    "warning": "",
    "wiki_url": "",
    "category": "User"
}

import bpy
from bpy.types import Operator
from bpy.props import FloatVectorProperty
#from bpy_extras.object_utils import AddObjectHelper, object_data_add
from mathutils import Vector

def top_menu(self, context):
    self.layout.menu(
        "PT_ParentMenu",
        text=PT_ParentMenu.bl_label
    )

class PT_ParentMenu(bpy.types.Menu):
    bl_idname = "PT_ParentMenu"
    bl_label = "Ports Tools"

    def draw(self, context):
        layout = self.layout

##################################

class PT_RenameBones(Operator):

    bl_idname = "object.rename_bones"
    bl_label = "Rename Bones"
    bl_options = {'REGISTER', 'UNDO'}

    def draw(self, context):
        layout = self.layout

        layout.operator("wm.open_mainfile")
        layout.operator("wm.save_as_mainfile")

    def execute(self, context):

        dict = {
            'J_Bip_C_Spine': 'mPelvis',
            '': ''
        }

        if hasattr(context.object.data, 'bones'):
            for b in context.object.data.bones:
                if b.name in dict.keys():
                    print("renamed: " + b.name + " -> " + dict[b.name])
                    b.name = dict[b.name]

        return {'FINISHED'}

##################################

class PT_ExportBones(Operator):

    bl_idname = "object.export_bones"
    bl_label = "Export Bones"
    bl_options = {'REGISTER', 'UNDO'}
    filepath = bpy.props.StringProperty(subtype="FILE_PATH")
    filename = bpy.props.StringProperty()
    directory = bpy.props.StringProperty(subtype="FILE_PATH")

    def draw(self, context):
        layout = self.layout

        layout.operator("wm.open_mainfile")
        layout.operator("wm.save_as_mainfile")

    def execute(self, context):

        if hasattr(context.object.data, 'bones'):
            with open(self.filepath, 'w') as f:
                for b in context.object.data.bones:
                   f.write(b.name+"\n\r")
            return {'FINISHED'}

        return {'FINISHED'}

    def invoke(self, context, event):
        self.filename = "bones.txt"
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

##################################

# Registration

def rename_menu(self, context):
    self.layout.operator(
        PT_RenameBones.bl_idname,
        text=PT_RenameBones.bl_label
    )

def export_menu(self, context):
    self.layout.operator(
        PT_ExportBones.bl_idname,
        text=PT_ExportBones.bl_label
    )

def register():
    bpy.utils.register_class(PT_ParentMenu)
    bpy.types.VIEW3D_MT_object.append(top_menu)

    bpy.utils.register_class(PT_RenameBones)
    bpy.types.PT_ParentMenu.append(rename_menu)

    bpy.utils.register_class(PT_ExportBones)
    bpy.types.PT_ParentMenu.append(export_menu)

def unregister():
    bpy.types.PT_ParentMenu.remove(export_menu)
    bpy.utils.unregister_class(PT_ExportBones)

    bpy.types.PT_ParentMenu.remove(rename_menu)
    bpy.utils.unregister_class(PT_RenameBones)

    bpy.types.VIEW3D_MT_object.remove(top_menu)
    bpy.utils.unregister_class(PT_ParentMenu)

if __name__ == "__main__":
    register()
