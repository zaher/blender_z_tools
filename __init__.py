"""Module Blender Z Tools."""
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

import bpy
from bpy.types import Operator
from bpy.props import FloatVectorProperty

from . import rename
from . import align

def register():
    rename.register()
    align.register()

def unregister():
    rename.unregister()
    align.unregister()

if __name__ == "__main__":
    register()
