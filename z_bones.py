"""
    @author: Zaher Dirkey
    @licesnse: MPL

    Module Blender Z Tools Rename Bones.
    Beta
"""

#* https://docs.blender.org/api/2.79/bpy.ops.object.html
#* https://blenderartists.org/t/renaming-bone-script/1299862/5

import bpy
from bpy.types import Operator
#from bpy.props import FloatVectorProperty
#from bpy_extras.object_utils import AddObjectHelper, object_data_add
#from mathutils import Vector

class OBJ_Z_Bones(bpy.types.Menu):
    bl_idname = "OBJ_Z_Bones" #same as class name
    bl_label = "Z Tools"

    def draw(self, context):
        layout = self.layout

def OBJ_Z_Bones_menu(self, context):
    self.layout.menu(
        OBJ_Z_Bones.bl_idname,
        text=OBJ_Z_Bones.bl_label
    )

## Rename Bones

class Rename_bones(Operator):

    bl_idname = "object.z_rename_bones"
    bl_label = "Rename VRoid Bones"
    bl_options = {'REGISTER', 'UNDO'}

    def draw(self, context):
        layout = self.layout

        layout.operator("wm.open_mainfile")
        layout.operator("wm.save_as_mainfile")

    def execute(self, context):

        vroid_dict = {
            'Root': 'mPelvis', # mabye leave it as Root
            'J_Bip_C_Hips': '',  # maybe is mPelvis
            'J_Bip_C_Spine': 'mTorso',
            'J_Bip_C_Chest': 'mChest',
            'J_Bip_C_UpperChest': '',     #delete it or it is a chest or delete C_Chest idk
            'J_Sec_L_Bust1': 'LEFT_PEC',
            'J_Sec_L_Bust2': '',
            'J_Sec_R_Bust1': 'RIGHT_PEC',
            'J_Sec_R_Bust2': '',
            'J_Bip_C_Neck': 'mNeck',
            'J_Bip_C_Head': 'mHead',
            'J_Adj_L_FaceEye': 'mEyeLeft',
            'J_Adj_R_FaceEye': 'mEyeRight',
            'J_Bip_L_Shoulder': 'mCollarLeft',
            'J_Bip_R_Shoulder': 'mCollarRight',
            'J_Bip_L_UpperArm': 'mShoulderLeft',
            'J_Bip_R_UpperArm': 'mShoulderRight',
            'J_Bip_L_LowerArm': 'mElbowLeft',
            'J_Bip_R_LowerArm': 'mElbowRight',
            'J_Bip_L_Hand': 'mWristLeft',
            'J_Bip_R_Hand': 'mWristRight',

            'J_Bip_L_UpperLeg': 'mHipLeft',
            'J_Bip_L_LowerLeg': 'mKneeLeft',
            'J_Bip_R_UpperLeg': 'mHipRight',
            'J_Bip_R_LowerLeg': 'mKneeRight',

            'J_Bip_L_Foot': 'mAnkleLeft',
            'J_Bip_R_Foot': 'mAnkleRight',
            'J_Bip_L_ToeBase': 'mFootLeft',
            'J_Bip_L_ToeBase_end': '',
            'J_Bip_R_ToeBase': 'mFootRight',
            'J_Bip_R_ToeBase_end': '',

            'J_Bip_L_Index1': '',
            'J_Bip_L_Index2': '',
            'J_Bip_L_Index3': '',
            'J_Bip_L_Index3_end': '',
            'J_Bip_L_Little1': '',
            'J_Bip_L_Little2': '',
            'J_Bip_L_Little3': '',
            'J_Bip_L_Little3_end': '',
            'J_Bip_L_Middle1': '',
            'J_Bip_L_Middle2': '',
            'J_Bip_L_Middle3': '',
            'J_Bip_L_Middle3_end': '',
            'J_Bip_L_Ring1': '',
            'J_Bip_L_Ring2': '',
            'J_Bip_L_Ring3': '',
            'J_Bip_L_Ring3_end': '',
            'J_Bip_L_Thumb1': '',
            'J_Bip_L_Thumb2': '',
            'J_Bip_L_Thumb3': '',
            'J_Bip_L_Thumb3_end': '',

            'J_Sec_L_TipSleeve': '',
            'J_Sec_L_TipSleeve_end': '',

            'J_Bip_R_Index1': '',
            'J_Bip_R_Index2': '',
            'J_Bip_R_Index3': '',
            'J_Bip_R_Index3_end': '',
            'J_Bip_R_Little1': '',
            'J_Bip_R_Little2': '',
            'J_Bip_R_Little3': '',
            'J_Bip_R_Little3_end': '',
            'J_Bip_R_Middle1': '',
            'J_Bip_R_Middle2': '',
            'J_Bip_R_Middle3': '',
            'J_Bip_R_Middle3_end': '',
            'J_Bip_R_Ring1': '',
            'J_Bip_R_Ring2': '',
            'J_Bip_R_Ring3': '',
            'J_Bip_R_Ring3_end': '',
            'J_Bip_R_Thumb1': '',
            'J_Bip_R_Thumb2': '',
            'J_Bip_R_Thumb3': '',
            'J_Bip_R_Thumb3_end': '',

            'J_Sec_R_TipSleeve': '',
            'J_Sec_R_TipSleeve_end': '',
        }

        if hasattr(context.object.data, 'bones'):
            bones_dict = vroid_dict
            for b in context.object.data.bones:
                if b.name in bones_dict.keys():
                    toname = bones_dict[b.name]
                    if toname != "":
                        print("renamed: " + b.name + " -> " + bones_dict[b.name])
                        b.name = bones_dict[b.name]

        return {'FINISHED'}

def rename_bones_menu(self, context):
    self.layout.operator(
        Rename_bones.bl_idname,
        text=Rename_bones.bl_label
    )

## Export Bones Names

class Export_bones(Operator):

    bl_idname = "object.z_export_bones"
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

def export_bones_menu(self, context):
    self.layout.operator(
        Export_bones.bl_idname,
        text=Export_bones.bl_label
    )

## Registration

def register():
    bpy.utils.register_class(OBJ_Z_Bones)
    bpy.types.VIEW3D_MT_object.append(OBJ_Z_Bones_menu)

    bpy.utils.register_class(Rename_bones)
    bpy.types.OBJ_Z_Bones.append(rename_bones_menu)

    bpy.utils.register_class(Export_bones)
    bpy.types.OBJ_Z_Bones.append(export_bones_menu)

def unregister():
    bpy.types.OBJ_Z_Bones.remove(export_bones_menu)
    bpy.utils.unregister_class(Export_bones)

    bpy.types.OBJ_Z_Bones.remove(rename_bones_menu)
    bpy.utils.unregister_class(Rename_bones)

    bpy.types.VIEW3D_MT_object.remove(OBJ_Z_Bones_menu)
    bpy.utils.unregister_class(OBJ_Z_Bones)