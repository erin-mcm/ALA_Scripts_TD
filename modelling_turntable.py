import bpy
import datetime
import functools
import math
import pathlib
from mathutils import Vector
import sys
import os
import addon_utils
from bpy.app.handlers import persistent

def make_active(obj):
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    #this will be used later to delete the sphere
def active_object():
    return bpy.context.active_object

#create floor
def create_floor(world_bounds):
    #bpy.ops.mesh.primitive_plane_add(enter_editmode=False, align='WORLD', location=(0, 0, object_world_bounds[1][2]-0.01))
    object_center = Vector(((world_bounds[0][0]+world_bounds[1][0])/2.0,(world_bounds[0][1]+world_bounds[1][1])/2.0,(world_bounds[0][2]+world_bounds[1][2])/2.0))
    bpy.ops.mesh.primitive_uv_sphere_add(location=object_center)
    floor = active_object()
    floor.scale[0] = 10000
    floor.scale[1] = 10000
    floor.scale[2] = 10000
    material = bpy.data.materials.new(name="floor_material")
    material.diffuse_color = (0.1, 0.1, 0, 1.0)
    material.specular_intensity = 0
    floor.data.materials.append(material)
    
#figure out the max and min coords of selected
def get_max_and_min_coords(objects):
    total_world_bounds = []
    for obj in objects:
        vertices = obj.data.vertices
        obj_world_bounds = []
        
        for v in vertices:
            obj_world_bounds.append(obj.matrix_world @ v.co)
        
        total_world_bounds.append(obj_world_bounds)
    
    max_bounds = []
    min_bounds = []
    
    for bounds in total_world_bounds:
        max_bounds.append(get_max_vector(bounds))
        min_bounds.append(get_min_vector(bounds))
    
    vector_max = get_max_vector(max_bounds)
    vector_min = get_min_vector(min_bounds)
    
    return (vector_max, vector_min)

def get_max_vector(world_coords):
    vector_max = Vector((max(world_coords[i][0] for i in range(len(world_coords))), max(world_coords[i][1] for i in range(len(world_coords))), max(world_coords[i][2] for i in range(len(world_coords)))))
    return vector_max

def get_min_vector(world_coords):
    vector_min = Vector((min(world_coords[i][0] for i in range(len(world_coords))), min(world_coords[i][1] for i in range(len(world_coords))), min(world_coords[i][2] for i in range(len(world_coords)))))
    return vector_min

def create_cameracontrol(world_bounds):
    #create empty at object center
    
    object_center = Vector(((world_bounds[0][0]+world_bounds[1][0])/2.0,(world_bounds[0][1]+world_bounds[1][1])/2.0,(world_bounds[0][2]+world_bounds[1][2])/2.0))
    empty = bpy.ops.object.empty_add(type="PLAIN_AXES", location=(object_center))
    empty = active_object()
    #create camera
    cam = bpy.ops.object.camera_add()
    cam = active_object()    
    #parent camera to move with empty
    bpy.ops.object.parent_set(type='OBJECT')
    cam.parent = empty
    #constrain camera to look at object
    longest_side = (world_bounds[0] - world_bounds[1]).length
    cam.location = (0,-1,0)
    bpy.ops.object.constraint_add(type="TRACK_TO")
    cam.constraints["Track To"].target = empty
    cam.constraints["Track To"].use_target_z = True
    #create sphere to ensure the whole object is in the frame and can be views
    sphere = bpy.ops.mesh.primitive_uv_sphere_add()
    sphere = active_object()
    sphere.dimensions = (longest_side,longest_side,longest_side)
    sphere.location = empty.location
    #fit the view of the camera with the model
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            with bpy.context.temp_override(area=area, region=[x for x in area.regions if x.type == 'WINDOW'][0]):
                make_active(cam)
                bpy.ops.view3d.object_as_camera()
                make_active(sphere)
                bpy.ops.view3d.camera_to_view_selected()
                #remove sphere
                bpy.ops.object.delete()
            break
    make_active(empty)
    
def light_controls():
    empty = bpy.context.active_object
    #add tri lighting to make it look spicy
    bpy.ops.preferences.addon_enable(module="lighting_tri_lights")
    tlights = bpy.ops.object.trilighting()
    #change the settings of the lights
    bpy.data.lights["TriLamp-Key"].energy = 2
    bpy.data.lights["TriLamp-Fill"].energy = 2
    bpy.data.lights["TriLamp-Back"].energy = 2
    bpy.data.lights["TriLamp-Key"].type = "SUN"
    bpy.data.lights["TriLamp-Fill"].type = "SUN"
    bpy.data.lights["TriLamp-Back"].type = "SUN"
#    TriLamp-Key.parent = empty
#    TriLamp-Fill.parent = empty
#    TriLamp-Back.parent = empty
    
def animate_rotation(model_parent):
    empty = bpy.context.active_object
    bpy.data.scenes["Scene"].frame_start = 1
    bpy.data.scenes["Scene"].frame_end = 300
    # insert keyframe at frame one
    start_frame = 1
    #frame inserts
    empty.keyframe_insert("rotation_euler", frame=start_frame)
    #rotation
    degrees = 360
    # convert degrees to radians to caculate circle animation
    radians = math.radians(degrees)
    empty.rotation_euler.z = radians
    #insert at end frame
    end_frame = 100
    #frame inserts
    empty.keyframe_insert("rotation_euler", frame=end_frame)
    
    # insert keyframe at frame one
    start_frame = 101
    #frame inserts
    empty.keyframe_insert("rotation_euler", frame=start_frame)
    #rotation
    # convert degrees to radians to caculate circle animation
    empty.rotation_euler.x = radians
    #insert at end frame
    end_frame = 200
    #frame inserts
    empty.keyframe_insert("rotation_euler", frame=end_frame)
    
    start_frame = 201
    #frame inserts
    empty.rotation_euler.z = 0
    empty.keyframe_insert("rotation_euler", frame=start_frame)
    model_parent.keyframe_insert("rotation_euler", frame=start_frame)
    #rotation
    # convert degrees to radians to caculate circle animation
    empty.rotation_euler.z = radians
    model_parent.rotation_euler.z = radians
    #insert at end frame
    end_frame = 300
    #frame inserts
    empty.keyframe_insert("rotation_euler", frame=end_frame)
    model_parent.keyframe_insert("rotation_euler", frame=end_frame)
    #could loop this animation but will take more time
    #fcurve to make it nice
    #for fcurve in obj.animation_data.action.fcurves:
        #fcurve.extrapolation = "LINEAR"
    
def render_model():
    time_stamp = datetime.datetime.now().strftime("%H-%M-%S")
    output_folder_path = "A:\\mav\\2023\\sandbox\\studio2\\s223\\departments\\modelling\\Dailies\\20230621\\"
    path = str(output_folder_path + f'modelling_turntable_{time_stamp}.mp4')
    bpy.context.scene.render.filepath = path.format()
    bpy.context.scene.render.image_settings.file_format = "FFMPEG"
    bpy.context.scene.render.ffmpeg.format = "MPEG4"
    bpy.context.scene.render.engine = "BLENDER_EEVEE"
    light_controls()
    bpy.ops.render.render(animation=True)
    

def run_turntable():
    bpy.ops.wm.save_mainfile()
    selected_objects = bpy.context.selected_objects
    
    bpy.ops.object.select_all(action='INVERT')
    bpy.ops.object.delete()
        
    model_world_bounds = get_max_and_min_coords(selected_objects)
    
    #create_floor(model_world_bounds)
    object_center = Vector(((model_world_bounds[0][0]+model_world_bounds[1][0])/2.0,(model_world_bounds[0][1]+model_world_bounds[1][1])/2.0,(model_world_bounds[0][2]+model_world_bounds[1][2])/2.0))
    empty = bpy.ops.object.empty_add(type="PLAIN_AXES", location=object_center)
    empty = active_object()
    for obj in selected_objects:
        if obj.parent == None:
            obj.parent = empty
            obj.location = (obj.location - object_center)
    
    create_cameracontrol(model_world_bounds)
    
    animate_rotation(empty)
    
    render_model()
    bpy.ops.wm.revert_mainfile()
    
#if __name__ == "__main__":
#    main()
#    
