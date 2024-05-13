"""
    @author: Zaher Dirkey
    @licesnse: MPL

    for OpenSIM mesh
    Export all objects that have "Convex" as individual files.
    The rest of objects exported as one file     
"""

import bpy
import os
from bl_ui.utils import PresetPanel
from bpy.types import Panel, Menu

convex_name = "z_convex"
name_suffex =  "-Convex";
## Replace these with the names of the objects you want to export

def export_opensim(selected_only=False, rename_mesh=True, grouped=False, individual=False, by_collections = False, operator=None):

    exported_count = 0;
    exported_objects_count = 0;

    if selected_only:
        selected_objects = [obj for obj in bpy.context.selected_objects if ((obj.type == "MESH") or (obj.type == "ARMATURE")) and obj.visible_get()]
    else:
        selected_objects = [obj for obj in  bpy.context.scene.objects if ((obj.type == "MESH") or (obj.type == "ARMATURE")) and obj.visible_get()]

    if len(selected_objects) ==0:
        if operator != None:
            operator.report({'ERROR'}, "Select objects to export!")
        return

    renamed_data = []

    if rename_mesh:
        ## Correct names of mesh
        for obj in selected_objects:
            ## not a cloned/linked
            #if obj.data.users <= 1:
            if not (obj.data in renamed_data): ## Already named, good for cloned/linked objects, we take first object as original one
                obj.data.name = obj.name
                renamed_data.append(obj.data)
        #   obj.transform_apply(location=True, rotation=True, scale=True, isolate_users=True)

    ## Replace this with the path to the folder where you want to export the DAE files
    export_folder = os.path.dirname(bpy.data.filepath)+"/output/"
    base_name = os.path.splitext(os.path.basename(bpy.data.filepath))[0]

    if not os.path.exists(export_folder):
        os.makedirs(export_folder)

    ## Create the export folder if it doesn't exist
    if not os.path.exists(export_folder):
        os.makedirs(export_folder)

    def extend_filename(extend):
        if extend == "":
            return base_name
        if base_name[0].isupper():
            return base_name + "-" + extend.title()
        else:
            return base_name + "-" + extend.lower()

    def export_objects(export_file):

        nonlocal exported_count, exported_objects_count

        exported_count = exported_count + 1
        exported_objects_count = exported_objects_count + len(bpy.context.selected_objects)

        ## https://docs.blender.org/api/current/bpy.ops.wm.html
        bpy.ops.wm.collada_export(
            filepath=export_file,
            selected=True,
            open_sim=True,
            limit_precision=True,
            triangulate=True, ## Because FS/OS can have wrong tries
            apply_modifiers=True,
            keep_bind_info=True,
            include_children=True, ##Rig
            #include_armatures=True, ##Rig
            # export_object_transformation_type_selection='decomposed', ## ---nope---need it for scale -1 for some linked objects
            export_object_transformation_type_selection='matrix',
            use_texture_copies=True,
            #export_texture_type='COPY',
            sort_by_name=True,
            apply_global_orientation=True,
            export_global_forward_selection='-X',
            export_global_up_selection='Z',
            export_mesh_type_selection='view',
            use_object_instantiation=False ## False we can have bug in cloned objects when uploaded
        )        

    ## Export Objects that have Convex
    if not grouped:
        if individual:
            ## Export Objects file for each one
            for obj in selected_objects:
                bpy.ops.object.select_all(action='DESELECT')
                obj.select_set(True)
                export_objects(os.path.join(export_folder, obj.name + ".dae"))
        else:
            bpy.ops.object.select_all(action='DESELECT')
            for obj in selected_objects:
                obj.select_set(True)
            export_objects(os.path.join(export_folder, base_name + ".dae"))

    else: ## Grouped
        if by_collections: ## by Collection
            for collection in bpy.data.collections:
                bpy.ops.object.select_all(action='DESELECT')
                for obj in collection.all_objects:
                    if (obj in selected_objects):
                        obj.select_set(True)
                #for collection_name in bpy.data.collections:
                #if collection_name in [c.name for c in obj.users_collection]:
                if len(bpy.context.selected_objects)>0:
                    export_objects(os.path.join(export_folder, collection.name + ".dae"))

        else: ## by Convex

            ## Export convexed objects (original)
            bpy.ops.object.select_all(action='DESELECT')
            for obj in selected_objects:
                if not obj.name.endswith(name_suffex) and (convex_name in obj.data.attributes):
                    obj.select_set(True)

            if len(bpy.context.selected_objects)>0:
                export_objects(os.path.join(export_folder, base_name + ".dae"))

            bpy.ops.object.select_all(action='DESELECT')

            ## Export convex objects
            for obj in selected_objects:
                if obj.name.endswith(name_suffex):
                    obj.select_set(True)
            if len(bpy.context.selected_objects)>0:
                export_objects(os.path.join(export_folder, extend_filename("convex") + ".dae"))

            ## Export the rest if objects not in the list above in one file
            bpy.ops.object.select_all(action='DESELECT')
            for obj in selected_objects:
                if not obj.name.endswith(name_suffex) and not (convex_name in obj.data.attributes):
                    obj.select_set(True)
            if len(bpy.context.selected_objects)>0:
                export_objects(os.path.join(export_folder, extend_filename("rest") + ".dae"))
        
    bpy.ops.object.select_all(action='DESELECT')

    if exported_count>0:
        operator.report({'INFO'}, "Exported: "+str(exported_objects_count)+" into: "+str(exported_count))