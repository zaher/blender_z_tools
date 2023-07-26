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
name_suffex =  "-Convex"
# Replace these with the names of the objects you want to export

def export_all_opensim(rename_mesh=True, individual=False):

    if rename_mesh:
        ## Correct names of mesh
        for obj in bpy.data.objects:
            if obj.data.library is not None:
                obj.data.name = obj.name                
        #    else:
        #        obj.transform_apply(location=True, rotation=True, scale=True, isolate_users=True)
                    
    objects = [obj for obj in bpy.data.objects if face_map_name in obj.face_maps]
                    
    #export_preset_name = "My"

    # Replace this with the path to the folder where you want to export the DAE files
    export_folder = os.path.dirname(bpy.data.filepath)+"/output/"
    base_name = os.path.splitext(os.path.basename(bpy.data.filepath))[0]

    if not os.path.exists(export_folder):
        os.makedirs(export_folder)

    # Create the export folder if it doesn't exist
    if not os.path.exists(export_folder):
        os.makedirs(export_folder)

    def export_objects(export_file):
        bpy.ops.wm.collada_export(
            filepath=export_file,
            selected=True, 
            apply_modifiers=True, 
            open_sim=True, 
            keep_bind_info=True,
            include_children=True,
            # export_object_transformation_type_selection='decomposed', ## ---nop---need it for scale -1 for some linked objects
            # apply_global_orientation=True, ## idk
            use_texture_copies=True,
            #export_texture_type='COPY',
            sort_by_name=True,        
            export_global_forward_selection='Y',
            export_global_up_selection='Z',
            export_mesh_type_selection='view',
            use_object_instantiation=True        
        )        

    ## Export Objects that have Convex face map    
    if individual:        
        ## Export Objects file for each one
        bpy.ops.object.select_all(action='DESELECT')
        for obj in objects:
            obj.select_set(True)
            export_objects(os.path.join(export_folder, obj.name + ".dae"))
            
    else:
        ## Export Objects in one files but with end name -Convex in another one files too
        bpy.ops.object.select_all(action='DESELECT')
        for obj in objects:
            if not obj.name.endswith(name_suffex):
                obj.select_set(True)
        export_objects(os.path.join(export_folder, base_name + ".dae"))

        bpy.ops.object.select_all(action='DESELECT')
        for obj in objects:
            if obj.name.endswith(name_suffex):
                obj.select_set(True)
        export_objects(os.path.join(export_folder, base_name + "-convex.dae"))

    ## Export the rest if objects not in the list above in one file    
    bpy.ops.object.select_all(action='SELECT')
    for obj in objects:
        obj.select_set(False)
    export_objects(os.path.join(export_folder, base_name + "-rest.dae"))
    
    bpy.ops.object.select_all(action='DESELECT')