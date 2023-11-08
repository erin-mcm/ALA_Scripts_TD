import bpy
from . import ALA_animation_preview
from bpy_extras.io_utils import ImportHelper
from bpy.types import Operator, Panel
from bpy.types import Menu, AddonPreferences
from bpy.props import (StringProperty, EnumProperty, CollectionProperty, FloatProperty, BoolProperty, IntProperty)

class ALAAnimationToolkit(bpy.types.Panel):
    bl_idname = "ALA_PT_Animation_Toolkit"
    bl_label = "ALA Animation Toolkit"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "ALA Animation"
    bl_options = {"DEFAULT_CLOSED"}
    bl_context_mode = "OBJECT"


    def draw(self, context):
        layout = self.layout
        scene = context.scene
        layout.label(text="Animation toolkit panel")
class ALA_PG_renderoptions(bpy.types.PropertyGroup):
    hidegpbool : BoolProperty(name="Hide Grease Pencil", description="Hides grease pencil", default=False)
    hidetextbool : BoolProperty(name="Hide Text", description="Hides text", default=False)
    autoplaybool : BoolProperty(name="Autoplay", description="Autoplays preview after render", default=False)
    stampbool : BoolProperty(name="Stamp date, time and frames", description="Stamps the date, time and frames", default=False)
class ALA_PT_animation_renderoptions(ALAAnimationToolkit, bpy.types.Panel):
    bl_idname = "ALA_PT_animation_renderoptions"
    bl_space_type = "VIEW_3D"
    bl_description = "Hide grease pencil in the preview"
    bl_label = "Render options"
    bl_region_type = "UI"
    bl_category = "ALA Animation"
    bl_options = {"DEFAULT_CLOSED"}
    bl_context_mode = "OBJECT"

    def draw(self, context):
        scene = context.scene
        layout = self.layout
        layout.label(text="Choose preferences before rendering")
        col = layout.column(align=True)
        col.prop(scene, 'hidegpbool', text="Hide Grease Pencil")
        col.prop(scene, 'hidetextbool', text="Hide Text")
        col.prop(scene, 'autoplaybool', text="Autoplay after Render")
        col.prop(scene, 'stampbool', text="Stamp Date, Time and Frame Range")
        
class ALA_PG_framerange(bpy.types.PropertyGroup):
    ala_frame_start:IntProperty(name='Frame Start')
    ala_frame_end:IntProperty(name='Frame End')

class ALA_PT_animation_framerange(ALAAnimationToolkit, bpy.types.Panel):
    bl_label = "Frame Range"
    bl_idname = "ALA_PT_animation_framerange"
    bl_space_type = "VIEW_3D"
    bl_description = "Choose frames to render"
    bl_region_type = "UI"
    bl_category = "ALA Animation"
    bl_options = {"DEFAULT_CLOSED"}
    bl_context_mode = "OBJECT"

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False
        scene = context.scene
        col = layout.column(align=True)
        col.prop(scene, 'ala_frame_start', text="Frame Start")
        col.prop(scene, 'ala_frame_end', text="End")
        col1 = layout.column(align=True)
        col1.label(text="Create animation preview")
        col1.operator(ALA_OT_render.bl_idname, text="Render preview")

class ALA_OT_hidegp(bpy.types.Operator):
    bl_idname = "ala_animation_toolkit.ala_hide_gp"
    bl_description = "Hide grease pencil in the preview"
    bl_label = "Hide Grease Pencil"
    def execute(self, context):
        ALA_animation_preview.hide_gpencil()
        return {'FINISHED'}

class ALA_OT_hidetext(bpy.types.Operator):
    bl_idname = "ala_animation_toolkit.ala_hide_text"
    bl_description = "Hide text in the preview"
    bl_label = "Hide text"
    def execute(self, context):
        ALA_animation_preview.hide_text()
        return {'FINISHED'}

class ALA_OT_stampdatetime(bpy.types.Operator):
    bl_idname = "ala_animaiton_toolkit.ala_stamp_datetimeframe"
    bl_description = "Stamp the date, time and frame range on the preview"
    bl_label = "Stamp date, time and frame range"
    def execute(self, context):
        ALA_animation_preview.stampdateframes()
        return {'FINISHED'}

class ALA_OT_autoplay(bpy.types.Operator):
    bl_idname = "ala_animation_toolkit.ala_autoplay"
    bl_description = "Autoplay preview after render"
    bl_label = "Autoplay after render"
    def execute(self, context):
        ALA_animation_preview.autoplay()
        return {'FINISHED'}

class ALA_OT_render(bpy.types.Operator, ImportHelper):
    bl_idname = "ala_animation_toolkit.ala_render"
    bl_description = "Renders with any options chosen"
    bl_label = "Render preview"
    def execute(self, context):
        ALA_animation_preview.render(self.filepath)
        return {'FINISHED'}

classes = (
    ALAAnimationToolkit,
    ALA_PG_renderoptions,
    ALA_PT_animation_renderoptions,
    ALA_PG_framerange,
    ALA_PT_animation_framerange,
    ALA_OT_hidegp,
    ALA_OT_hidetext,
    ALA_OT_stampdatetime,
    ALA_OT_autoplay,
    ALA_OT_render
)

def register():
    bpy.types.Scene.ala_frame_start = IntProperty(name="ala_frame_start")
    bpy.types.Scene.ala_frame_end = IntProperty(name="ala_frame_end")
    bpy.types.Scene.hidegpbool = BoolProperty(name="hidegpbool")
    bpy.types.Scene.hidetextbool = BoolProperty(name="hidetextbool")
    bpy.types.Scene.autoplaybool = BoolProperty(name="autoplaybool")
    bpy.types.Scene.stampbool = BoolProperty(name="stampbool")
    for cls in classes:
        bpy.utils.register_class(cls)
def unregister():
    del bpy.types.Scene.ala_frame_start
    del bpy.types.Scene.ala_frame_end
    del bpy.types.Scene.hidegpbool
    del bpy.types.Scene.hidetextbool
    del bpy.types.Scene.autoplaybool
    del bpy.types.Scene.stampbool
    for cls in classes:
        bpy.utils.unregister_class(cls)
if __name__ == "__main__":
    register()
    
     