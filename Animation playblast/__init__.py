import bpy

bl_info = {
    "name": "Animation Toolkit",
    "author": "Erin McManus",
    "version": (1, 0),
    "blender": (3, 50, 0),
    "location": "View3D > Sidebar > ALA Animation",
    "description": "ALA animation toolkit for Blender",
    "category": "3D View"}

from . import ALA_Animation_ui_panel

def register():
    ALA_Animation_ui_panel.register()

def unregister():
    ALA_Animation_ui_panel.unregister()
