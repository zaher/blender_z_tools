"""
    @author: Zaher Dirkey
    @licesnse: MPL

    Create mesh objects from objects that have a convex faces,
    it copy all faces in Convex face map into another new object, moving it to `Convex` collection

    https://blender.stackexchange.com/questions/316391/how-can-i-access-and-modify-a-boolean-attribute-in-edit-mode
    https://blender.stackexchange.com/questions/266991/manually-setting-custom-attributes-per-edge-vertex-etc
"""

import bpy
import bmesh
import os
from bl_ui.utils import PresetPanel
from bpy.types import Panel, Menu

def convert_from_3x(del_facemaps = False):
    objs = bpy.context.scene.objects
    for obj in objs:
        if obj.type == "MESH":
            attr = obj.data.attributes.get("Convex")
            if attr != None:
                bpy.context.view_layer.objects.active = obj
                obj.data.attributes.active = attr
                attr.name = "z_convex"
                bpy.ops.geometry.attribute_convert(domain='FACE', data_type='INT')
            if del_facemaps:
                attr = obj.data.attributes.get("face_maps")
                if attr != None:
                    obj.data.attributes.remove(attr)

            #bpy.ops.geometry.attribute_convert(domain='FACE', data_type='INT')

## Must be called in Edit mode

def select_convex_faces(value):
    mesh = bpy.context.object.data
    bm = bmesh.from_edit_mesh(mesh)
    layer = bm.faces.layers.int.get("z_convex")
    count = 0
    if layer != None:
        bm.faces.ensure_lookup_table();
        for f in bm.faces:
            if bm.faces[f.index][layer] == True:
                f.select = value
            if bm.faces[f.index][layer] == True:
                count = count + 1
        bmesh.update_edit_mesh(mesh)
    return count

## Must be called in Edit mode

def assign_convex_faces(value):
    mesh = bpy.context.object.data
    bm = bmesh.from_edit_mesh(mesh)
    layer = bm.faces.layers.int.get("z_convex")
    if layer == None:
        layer = bm.faces.layers.int.new("z_convex")

    bm.faces.ensure_lookup_table();
    count = 0
    for f in bm.faces:
        if f.select:
            bm.faces[f.index][layer] = value
        if bm.faces[f.index][layer] == True:
            count = count + 1
    #run ensure_lookup_table()
    if (count == 0):
        bm.faces.layers.int.remove(layer)
    bmesh.update_edit_mesh(mesh)
    return count

## Must be called in Edit mode

def count_convex_faces():
    mesh = bpy.context.object.data
    bm = bmesh.from_edit_mesh(mesh)
    layer = bm.faces.layers.int.get("z_convex")
    if layer == None:
        return 0

    count = 0
    for f in bm.faces:
        if bm.faces[f.index][layer] == True:
            count = count + 1
    return count

def has_convex():
    mesh = bpy.context.object.data
    bm = bmesh.from_edit_mesh(mesh)
    layer = bm.faces.layers.int.get("z_convex")
    return layer != None

##########################
##  create_convex_mesh  ##
##########################

def create_convex_mesh(selected_only = False, operator=None, dissolve_limited = True):
    convex_name = "z_convex"
    collection_convex_name = 'Convex'
    name_suffex = "-Convex"

    ## Collect objects that have "z_convex"
    if selected_only:
        objs = bpy.context.selected_objects
    else:
        objs = bpy.context.scene.objects
        #objs = bpy.data.objects

    convexObjects = [obj for obj in objs if (obj.type == "MESH") and (not obj.name.endswith(name_suffex)) and (convex_name in obj.data.attributes)]

    if len(convexObjects)>0:

        ## Create _Convex collection
        if collection_convex_name in bpy.data.collections:
            convex_collection = bpy.data.collections[collection_convex_name]
        else:
            convex_collection = bpy.data.collections.new(collection_convex_name)
            bpy.context.scene.collection.children.link(convex_collection)

        ## Switch to Object Mode

        if bpy.context.mode != "OBJECT":
            bpy.ops.object.mode_set(mode='OBJECT')

        #bpy.ops.object.select_all(action='DESELECT')

        for obj in convexObjects:

            new_name = obj.name + name_suffex
            ## Find the new name if exists we will delete the old one
            if new_name in bpy.data.objects:
                new_obj = bpy.data.objects[new_name]
                bpy.data.objects.remove(new_obj, do_unlink=True)

            bpy.ops.object.select_all(action='DESELECT')
            bpy.context.view_layer.objects.active = obj
            obj.select_set(True)

            mesh = obj.data

            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.select_all(action='DESELECT')

            count = select_convex_faces(True)

            if count > 0:
                ## to find the new object that separated we save old objects
                old_selected = [o for o in bpy.context.scene.objects]

                #bpy.ops.object.mode_set(mode='EDIT')
                bpy.ops.mesh.duplicate(mode=1)
                if dissolve_limited:
                    bpy.ops.mesh.dissolve_limited(angle_limit=0.001, use_dissolve_boundaries=False, delimit={'NORMAL'})
                bpy.ops.mesh.separate(type='SELECTED')

                ## now we compare new objects with old to find new object created by separate
                cur_selected = [o for o in bpy.context.scene.objects]
                new_obj = [o for o in cur_selected if o not in old_selected][0]
 
                new_obj.data.materials.clear()

                for uv in new_obj.data.uv_layers:
                    new_obj.data.uv_layers.remove(uv)                

                #for material in new_obj.data.materials:
                #    material.user_clear()
                #    new_obj.data.materials.remove(material, do_unlink=True)

                #for m in range(len(new_obj.material_slots)):
                #    new_obj.material_slot_remove({'object': ob})                

                ## Moving it to new collection
                for coll in new_obj.users_collection:
                    coll.objects.unlink(new_obj)

                attr = new_obj.data.attributes.get(convex_name)
                if attr != None:
                    new_obj.data.attributes.remove(attr)

                new_obj.name = new_name
                new_obj.data.name = new_obj.name
                convex_collection.objects.link(new_obj)
                bpy.ops.object.mode_set(mode='OBJECT')
