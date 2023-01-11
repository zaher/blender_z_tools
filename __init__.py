"""Module Blender Z Tools."""
import bpy
from bpy.types import Operator
from bpy.props import FloatVectorProperty

from . import z_rename
from . import z_uv

bl_info = {
    "name": "Z Tools",
    "author": "Zaher Dirkey",
    "version": (1, 0),
    "blender": (2, 70, 0),
    "location": "View3D > Object > Z Tools > ",
    "description": "Rename, Export Bones (VRoid)",
    "warning": "",
    "wiki_url": "",
    "category": "User"
}

def register():
    z_rename.register()
    z_uv.register()

def unregister():
    z_rename.unregister()
    z_uv.unregister()

if __name__ == "__main__":
    register()
