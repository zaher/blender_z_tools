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
    "version": (1, 2),
    "blender": (3, 4, 0),
    "location": "View3D > Object > Z Tools > ",
    "description": "Z Tools",
    "warning": "",
    "wiki_url": "",
    "category": "User"
}

class Z_ExportIndividual(Operator):
    """ Export selected objects to "output" folder into multiple .dae files"""
    bl_idname = "ztools.export_individual"
    bl_label = "Export Individual"

    def execute(self, context):
        # Add code here to define what the operator should do
        z_export_all.export_opensim(individual=True, operator=self)
        return {'FINISHED'}

class Z_ExportGrouped(Operator):
    """ Export all object based on FaceMap "Convex" to "output" folder into 3 .dae files"""
    bl_idname = "ztools.export_all_grouped"
    bl_label = "Export Grouped"

    def execute(self, context):
        # Add code here to define what the operator should do
        z_export_all.export_opensim(individual=False, operator=self)
        return {'FINISHED'}

class Z_OpenSIM_Panel(Panel):
    bl_idname = "VIEW_3D_PT_z_exprot_tools"
    bl_label = "OpenSIM"
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
        row.operator(Z_ExportIndividual.bl_idname, text=Z_ExportIndividual.bl_label, icon="EXPORT")

        row = layout.column(align=True)
        #row = col.row(align=True)
        row.operator(Z_ExportGrouped.bl_idname, text=Z_ExportGrouped.bl_label, icon="EXPORT")

class Z_CreateConvex(Operator):
    """Create objects from current object that have "Convex" FaceMap, only using faces in this FaceMap"""
    bl_idname = "ztools.create_convex"
    bl_label = "Create Convex"

    def execute(self, context):
        # Add code here to define what the operator should do
        z_create_convex.create_convex()
        return {'FINISHED'}

class Z_Mesh_Panel(Panel):
    bl_idname = "VIEW_3D_PT_z_mesh_tools"
    bl_label = "Mesh Tools"
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

        layout.label(text="Mesh:")
        
        row = layout.column(align=True)
        #row = col.row(align=True)
        row.operator(Z_CreateConvex.bl_idname, text=Z_CreateConvex.bl_label)

current_module = sys.modules[__name__]
classes = inspect.getmembers(current_module, predicate=inspect.isclass)

def z_register():    
    for name, cls in classes:
        if hasattr(cls, 'bl_idname'):     
            bpy.utils.register_class(cls)

def z_unregister():
    for name, cls in reversed(classes):
        if hasattr(cls, 'bl_idname'):     
            bpy.utils.unregister_class(cls)

def register():
    z_register()

def unregister():
    z_unregister()

if __name__ == "__main__":
    register()
