"""
    @author: Zaher Dirkey
    @licesnse: MPL

    Export all objects that have Face Map = "Convex" as individual files, 
    The rest of objects exported as one file     
"""
import bpy
import os
from bl_ui.utils import PresetPanel
from bpy.types import Panel, Menu

face_map_name = "Convex"
name_suffex =  "-"+face_map_name;
# Replace these with the names of the objects you want to export

def export_opensim(rename_mesh=True, individual=False, by_collections = False, operator=None):

    exported_count = 0;

    if rename_mesh:
        if individual:
            objs = bpy.context.selected_objects
        else: ## All objects
            objs = bpy.data.objects

        ## Correct names of mesh
        for obj in objs:
            ## not a cloned/linked
            #if obj.data.users <= 1:

            ## Only visible objects
            if obj.visible_get():
                obj.data.name = obj.name

        #    else:
        #        obj.transform_apply(location=True, rotation=True, scale=True, isolate_users=True)

    if individual:
        objects = [obj for obj in bpy.context.selected_objects]
    else:                        
        objects = [obj for obj in bpy.data.objects if obj.visible_get() and (face_map_name in obj.face_maps)]
                    
    #export_preset_name = "My"

    ## Replace this with the path to the folder where you want to export the DAE files
    export_folder = os.path.dirname(bpy.data.filepath)+"/output/"
    base_name = os.path.splitext(os.path.basename(bpy.data.filepath))[0]

    if not os.path.exists(export_folder):
        os.makedirs(export_folder)

    ## Create the export folder if it doesn't exist
    if not os.path.exists(export_folder):
        os.makedirs(export_folder)

    def export_objects(export_file):

        nonlocal exported_count

        exported_count = exported_count + 1

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

    ## Export Objects that have Convex face map
    if individual:
        if len(objects) ==0:
            if operator!=None:
                operator.report({'ERROR'}, "Select objects to export!")
        else:
            ## Export Objects file for each one
            for obj in objects:
                bpy.ops.object.select_all(action='DESELECT')
                obj.select_set(True)
                export_objects(os.path.join(export_folder, obj.name + ".dae"))

    else:
        if by_collections:
            for collection in bpy.data.collections:
                bpy.ops.object.select_all(action='DESELECT')
                for obj in collection.all_objects:
                    obj.select_set(True)
            #for collection_name in bpy.data.collections:
                #if collection_name in [c.name for c in obj.users_collection]:
                #    obj.select_set(True)
            #if len(bpy.context.selected_objects)>0:
                if len(bpy.context.selected_objects)>0:
                    export_objects(os.path.join(export_folder, collection.name + ".dae"))

        else:
            ## Export Objects in one files but with end name -Convex in another one files too
            bpy.ops.object.select_all(action='DESELECT')
            for obj in objects:
                if not obj.name.endswith(name_suffex):
                    obj.select_set(True)

            if len(bpy.context.selected_objects)>0:
                export_objects(os.path.join(export_folder, base_name + ".dae"))

            bpy.ops.object.select_all(action='DESELECT')

            for obj in objects:
                if obj.name.endswith(name_suffex):
                    obj.select_set(True)
            if len(bpy.context.selected_objects)>0:
                export_objects(os.path.join(export_folder, base_name + "-"+face_map_name+".dae"))

            ## Export the rest if objects not in the list above in one file
            bpy.ops.object.select_all(action='SELECT')
            for obj in objects:
                obj.select_set(False)
            if len(bpy.context.selected_objects)>0:
                export_objects(os.path.join(export_folder, base_name + "-Rest.dae"))
        
    if not individual: 
        bpy.ops.object.select_all(action='DESELECT')

    if exported_count>0:
        operator.report({'INFO'}, "Exported Objects: "+str(exported_count))