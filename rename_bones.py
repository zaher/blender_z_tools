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

def rename_bones(self, context):
    dict = {
        'J_Bip_C_Spine': 'mPelvis',
        'J_Bip_C_Chest': 'foo1'
    }

    for b in context.object.data.bones:
        if b.name in dict.keys():
            print("renamed: " + b.name + " -> " + dict[b.name])
            b.name = dict[b.name]

class PT_ParentMenu(bpy.types.Menu):
    bl_idname = "PT_ParentMenu"
    bl_label = "Ports Tools"

    def draw(self, context):
        layout = self.layout

class PT_RenameBones(Operator):

    bl_idname = "object.rename_bones"
    bl_label = "Rename Bones"
    bl_options = {'REGISTER', 'UNDO'}

    def draw(self, context):
        layout = self.layout

        layout.operator("wm.open_mainfile")
        layout.operator("wm.save_as_mainfile")

    def execute(self, context):

        rename_bones(self, context)

        return {'FINISHED'}

# Registration

def top_menu(self, context):
    self.layout.menu(
        "PT_ParentMenu",
        text=PT_ParentMenu.bl_label
    )

def rename_menu(self, context):
    self.layout.operator(
        PT_RenameBones.bl_idname,
        text=PT_RenameBones.bl_label
    )

def menu_func(self, context):
    self.layout.operator(
        PT_RenameBones.bl_idname
    )

def register():
    bpy.utils.register_class(PT_ParentMenu)
    bpy.types.VIEW3D_MT_object.append(top_menu)
    bpy.utils.register_class(PT_RenameBones)
    bpy.types.PT_ParentMenu.append(rename_menu)


def unregister():
    bpy.types.PT_ParentMenu.remove(rename_menu)
    bpy.types.VIEW3D_MT_object.remove(top_menu)
    bpy.utils.unregister_class(PT_ParentMenu)
    bpy.utils.unregister_class(PT_RenameBones)

if __name__ == "__main__":
    register()
