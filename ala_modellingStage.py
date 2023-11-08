import maya.cmds as cmds
import rfm2
import os
def cameraStage():
    cameraShape1 = cmds.camera()
    cmds.viewFit( 'cameraShape1', all=True)
    rfm2.api.nodes.create_and_select('PxrDomeLight')
    cmds.file('/mnt/ala/mav/2023/sandbox/studio1/modelling/20230316/cutcan.obj', i=True, groupReference=True, groupName='Cylinder')
    cmds.select('Cylinder')
    cmds.scale(5,5,5)
    cmds.group('PxrDomeLight', 'Cylinder', n='exclude')
    cmds.lookThru( 'camera1' )
cameraStage()

