"""
    @author: Zaher Dirkey
    @licesnse: MPL

    Module Blender Z Tools.

thanks to 
    https://medium.com/geekculture/creating-a-custom-panel-with-blenders-python-api-b9602d890663    
    https://blender.stackexchange.com/questions/146417/quickest-way-to-create-panel-buttons-with-quick-functionality

"""
import bpy
import inspect
import sys
from bpy.types import Operator
from bpy.props import FloatVectorProperty
from bpy.types import Panel

from . import z_rename
from . import z_tool
from . import z_create_convex
from . import z_export_all

bl_info = {
    "name": "Z Tools",
    "author": "Zaher Dirkey",
    "version": (1, 0),
    "blender": (3, 4, 0),
    "location": "View3D > Object > Z Tools > ",
    "description": "Z Tools",
    "warning": "",
    "wiki_url": "",
    "category": "User"
}

class Z_ExportAll(Operator):
    bl_idname = "ztools.export_all"
    bl_label = "Export Individual"

    def execute(self, context):
        # Add code here to define what the operator should do
        z_export_all.export_all_opensim(individual=True)
        return {'FINISHED'}

class Z_ExportAllGouped(Operator):
    bl_idname = "ztools.export_all_grouped"
    bl_label = "Export Grouped"

    def execute(self, context):
        # Add code here to define what the operator should do
        z_export_all.export_all_opensim(individual=False)
        return {'FINISHED'}

class Z_Panel(Panel):
    bl_idname = "VIEW_3D_PT_z_tools"
    bl_label = "Z Tools"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Z Tools"
    bl_context = "objectmode" 
    bl_options = {'DEFAULT_CLOSED'}

#    @classmethod
#    def poll(self,context):
#        return context.object is not None

    def draw(self, context):
        layout = self.layout

        layout.label(text="Export:")
        
        row = layout.column(align=True)
        #row = col.row(align=True)
        row.operator(Z_ExportAll.bl_idname, text=Z_ExportAll.bl_label, icon="EXPORT")

        row = layout.column(align=True)
        #row = col.row(align=True)
        row.operator(Z_ExportAllGouped.bl_idname, text=Z_ExportAllGouped.bl_label, icon="EXPORT")

current_module = sys.modules[__name__]
classes = inspect.getmembers(current_module, predicate=inspect.isclass)

def z_register():    
    for name, cls in classes:
        if hasattr(cls, 'bl_idname'):     
            bpy.utils.register_class(cls)
    #bpy.utils.register_class(Z_Panel)
    #py.utils.register_class(Z_ExportAll)

def z_unregister():
    for name, cls in reversed(classes):
        if hasattr(cls, 'bl_idname'):     
            bpy.utils.unregister_class(cls)
    #py.utils.unregister_class(Z_ExportAll)
    #bpy.utils.unregister_class(Z_Panel)

def register():
    z_register()
    #z_rename.register()
    #z_tool.register()

def unregister():
    #z_rename.unregister()
    #z_tool.unregister()
    z_unregister()

if __name__ == "__main__":
    register()
