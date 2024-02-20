"""
    @author: Zaher Dirkey
    @licesnse: MPL

    Module Blender Z Tools.

thanks to 
    https://medium.com/geekculture/creating-a-custom-panel-with-blenders-python-api-b9602d890663    
    https://blender.stackexchange.com/questions/146417/quickest-way-to-create-panel-buttons-with-quick-functionality

"""
if "bpy" in locals():
    import importlib
    if "z_create_convex" in locals():
        importlib.reload(z_create_convex)
    if "z_export_all" in locals():
        importlib.reload(z_export_all)

import bpy
import inspect
import sys
from bpy.types import Operator
from bpy.props import (PointerProperty, FloatVectorProperty, BoolProperty)
from bpy.types import (Panel, PropertyGroup)

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

##
## Export
##

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
    bl_label = "By Convex"

    def execute(self, context):
        # Add code here to define what the operator should do
        z_export_all.export_opensim(individual=False, operator=self)
        return {'FINISHED'}

class Z_ExportByCollections(Operator):
    """ Export all object based on collections name "output" folder"""
    bl_idname = "ztools.export_all_bycollections"
    bl_label = "By Collections"

    def execute(self, context):
        # Add code here to define what the operator should do
        z_export_all.export_opensim(by_collections=True, operator=self)
        return {'FINISHED'}

class Z_OpenSIM_Panel(Panel):
    bl_idname = "VIEW_3D_PT_z_export_tools"
    bl_label = "OpenSIM"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Z Tools"
    bl_context = "objectmode" 
    bl_options = {'HEADER_LAYOUT_EXPAND'}

#    @classmethod
#    def poll(self,context):
#        return context.object is not None

    def draw(self, context):
        layout = self.layout

        layout.label(text="Export:")
        
        row = layout.column(align=True)
        #row = col.row(align=True)
        row.operator(Z_ExportIndividual.bl_idname, text=Z_ExportIndividual.bl_label, icon="EXPORT")


        layout.label(text="Groups:")

        row = layout.column(align=True)
        #row = col.row(align=True)
        row.operator(Z_ExportGrouped.bl_idname, text=Z_ExportGrouped.bl_label, icon="EXPORT")

        row = layout.column(align=True)
        row.operator(Z_ExportByCollections.bl_idname, text=Z_ExportByCollections.bl_label, icon="EXPORT")

##
## Convex
##

class Z_ConvexSettings(PropertyGroup):
    selected_only : BoolProperty(
        name="Enable or Disable",
        description="A bool property",
        default = False
    )

class Z_CreateConvex(Operator):
    """Create objects from current object that have "Convex" FaceMap, only using faces in this FaceMap"""
    bl_idname = "ztools.create_convex"
    bl_label = "Create Convex"

    selected_only: bpy.props.BoolProperty(name="selected_only", description="Selected Only", default=False)

    def execute(self, context):
        # Add code here to define what the operator should do
        #preferences = context.preferences.addons[Z_ToolsPreferences.bl_idname].preferences
        z_create_convex.create_convex(selected_only = context.scene.z_convex_settings.selected_only, operator=self)
        return {'FINISHED'}

class Z_Mesh_Panel(Panel):
    bl_idname = "VIEW_3D_PT_z_mesh_tools"
    bl_label = "Mesh Tools"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Z Tools"
    bl_context = "objectmode" 
    bl_options = {'HEADER_LAYOUT_EXPAND'}

#    @classmethod
#    def poll(self,context):
#        return context.object is not None

    def draw(self, context):
        layout = self.layout
        z_convex_settings = context.scene.z_convex_settings

        layout.label(text="Create Convex:")
        
        row = layout.row(align=True)
        # display the properties
        row.prop(z_convex_settings, "selected_only", text="Selected Only")
        row = layout.row(align=True)
        #row.separator_spacer()
        #row = col.row(align=True)
        row.operator(Z_CreateConvex.bl_idname, text=Z_CreateConvex.bl_label)
##        op.selected_only =

##
## Addon
##

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
    bpy.utils.register_class(Z_ConvexSettings)
    z_register()
    bpy.types.Scene.z_convex_settings = PointerProperty(type=Z_ConvexSettings)

def unregister():
    z_unregister()
    del bpy.types.Scene.z_convex_settings
    bpy.utils.unregister_class(Z_ConvexSettings)

if __name__ == "__main__":
    register()
