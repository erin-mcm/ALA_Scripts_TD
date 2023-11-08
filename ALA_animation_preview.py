import bpy
import math
from contextlib import redirect_stdout
import io
from datetime import datetime
#recognise active objects to use later
def make_active(obj):
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    #this will be used later to delete the sphere
def active_object():
    return bpy.context.active_object
def hide_text():
    for txt in bpy.context.scene.objects:
        if txt.type =='FONT':
            print(txt)
            txt.hide_render = True
            print("Text hidden")
def hide_gpencil():
    for gp in bpy.context.scene.objects:
        if gp.type =='GPENCIL':
            print(gp)
            gp.hide_render = True
        print("Grease Pencil hidden")
#get frames with animation start and end 
def get_frames(self, context):
    scene = bpy.context.scene
    frames = []
    end = self.ala_end_frame
    start = self.ala_start_frame
    orig_frame = scene.frame_current
    scene.frame_set(end + 1)
    with redirect_stdout(io.StringIO()):
        while 'FINISHED' in bpy.ops.screen.keyframe_jump(next=False) and scene.frame_current >= start:
            frames.insert(0, scene.frame_current)
    scene.frame_set(orig_frame)
    return frames
    #return frames
#stamps for date, time and frame range
def stampdateframes():
    bpy.context.scene.render.use_stamp = True
    bpy.context.scene.render.use_stamp_date = True
    bpy.context.scene.render.use_stamp_frame_range = True
    bpy.context.scene.render.use_stamp_frame = True
#ability to autoplay
def autoplay():
    bpy.ops.render.play_rendered_anim()
def render(filepath):
#choose where to save render  
    bpy.ops.wm.save_mainfile()  
    try:
        if(bpy.context.scene.hidegpbool == True):
            for gp in bpy.context.scene.objects:
                if gp.type =='GPENCIL':
                    print(gp)
                    gp.hide_render = True
                    print("hid grease pencil")
        if(bpy.context.scene.hidetextbool == True):
            for txt in bpy.context.scene.objects:
                if txt.type =='FONT':
                    print(txt)
                    txt.hide_render = True
                    print("Text hidden")
        print("starting render")
        bpy.context.scene.frame_start = bpy.context.scene.ala_frame_start
        bpy.context.scene.frame_end = bpy.context.scene.ala_frame_end
        bpy.context.scene.render.filepath = filepath.format()
        bpy.context.scene.render.image_settings.file_format = "FFMPEG"
        bpy.context.scene.render.ffmpeg.format = "MPEG4"
        bpy.context.scene.render.engine = "BLENDER_EEVEE"
        #check for bool and stamp on render video before rendering
        bpy.context.scene.render.use_stamp = False
        bpy.context.scene.render.use_stamp_date = False
        bpy.context.scene.render.use_stamp_frame_range = False
        bpy.context.scene.render.use_stamp_frame = False
        if(bpy.context.scene.stampbool == True):
            bpy.context.scene.render.use_stamp = True
            bpy.context.scene.render.use_stamp_date = True
            bpy.context.scene.render.use_stamp_frame_range = True
            bpy.context.scene.render.use_stamp_frame = True
            print("Stamps done")
        bpy.ops.render.render(animation=True)
        print("rendered")
        #if bool checked autoplay render after
        if(bpy.context.scene.autoplaybool == True):
            bpy.ops.render.play_rendered_anim()
        print("autoplay done")
    except Exception as e:
        print(str(e))
    finally:
        bpy.ops.wm.revert_mainfile()
