import maya.cmds as cmds
def overlay3(currentCameraTransform, *args): #apply to selected camera and look through selected camera
    currentCamera = cmds.listRelatives(currentCameraTransform, type='camera')[0]
    #create rig lines
    crv_v1 = cmds.curve(p=[(-0.25, 0.5, 0), (-0.25, 0.166667, 0), (-0.25, -0.166667, 0), (-0.25, -0.5, 0)], k=[0,0,0,1,1,1], d=3, n='crv_v1')
    crv_v2 = cmds.curve(p=[(0.25, 0.5, 0), (0.25, 0.166667, 0), (0.25, -0.2, 0), (0.25, -0.5, 0)], k=[0,0,0,1,1,1], d=3, n='crv_v2')
    crv_h1 = cmds.curve(p=[(-0.678, 0.11, 0), (-0.678, 0.11, 0), (0.678, 0.11, 0), (0.678, 0.11, 0)], k=[0,0,0,1,1,1], d=3, n='crv_h1')
    crv_h2 = cmds.curve(p=[(-0.678, -0.11, 0), (-0.678, -0.11, 0), (0.678, -0.11, 0), (0.678, -0.11, 0)], k=[0,0,0,1,1,1], d=3, n='crv_h2')
    #create grid and constrain it
    comp_grid = cmds.group(crv_v1, crv_v2, crv_h1, crv_h2, n='comp_grid')
    comp_grid_group = cmds.group(comp_grid, n='comp_grid_'+currentCameraTransform)
    comp_grid = cmds.ls(cmds.listRelatives(comp_grid_group)[0], long=True)[0]
    #print(comp_grid)
    cmds.xform(comp_grid, os=True, piv=[0,0,0])
    cmds.parentConstraint(currentCameraTransform, comp_grid_group)[0]
    cmds.setAttr(comp_grid+'.scaleX', 4)
    cmds.setAttr(comp_grid+'.scaleY', 3)
    cmds.setAttr(comp_grid+'.translateX', 0)
    cmds.setAttr(comp_grid+'.translateY', 0)
    cmds.setAttr(comp_grid+'.translateZ', -0.83)
    cmds.setAttr(comp_grid+'.rotateX', 0)
    cmds.setAttr(comp_grid+'.rotateY', 0)
    cmds.setAttr(comp_grid+'.rotateZ', 0)
    #allowing grid to be an overlay
    cmds.expression(s=comp_grid+'.scaleX= 1.6 * (35/'+currentCamera+'.focalLength); '+comp_grid+'.scaleY = 0.95* (35/'+currentCamera+'.focalLength);')
    cmds.createDisplayLayer(n='Rule_of_ThirdsL', num=1)
    cmds.camera(currentCamera, e=True, dfg=False, dr=True, ovr=1.3)
    cmds.cycleCheck(e=False)

def toggleOL(connections, currentCameraTransform):
    for c in connections:
        if 'comp_grid' in c and c != 'comp_grid_' + currentCameraTransform:
            cmds.rename(c, 'comp_grid_' + currentCameraTransform)
            connections = ['comp_grid_' + currentCameraTransform if x==c else x for x in connections]
    
    if connections != None:
        for comp_grid in [x for x in connections if 'comp_grid' in x]: #Check if overlay exists on the selected camera
            currentVis = cmds.getAttr(comp_grid +'.visibility') 
            if currentVis==1: 
                cmds.setAttr(comp_grid + '.visibility', 0)#If overlay does exist, check if the overlay is currently visible
            else:
                cmds.setAttr(comp_grid + '.visibility', 1)#If the over does not exist, make one

def rule3(*args):
    for o in cmds.ls(sl=True):
        currentCameraTransform = None
        if cmds.objectType(o) == 'transform':
            if cmds.listRelatives(o, type='camera'):
                currentCameraTransform = o
        elif cmds.objectType(o) == 'camera':
            currentCameraTransform = cmds.listRelatives(o, type='transform', parent=True)[0]
        
        if currentCameraTransform:
            try:
                connections = cmds.listRelatives(list(set(cmds.listConnections(currentCameraTransform,s=False))), parent=True)
            except:
                connections = None

            if connections == None or len([x for x in connections if 'comp_grid' in x]) == 0:
                overlay3(currentCameraTransform)
            else:
                toggleOL(connections, currentCameraTransform)
        
        if "comp_grid" in o:#if comp grid is selected also toggle the visibility
            currentCameraTransform = cmds.parentConstraint(q=True, targetList=True)[0]
            cmds.select(currentCameraTransform)
            connections = [o]
            toggleOL(connections, currentCameraTransform)

def linesandpat(currentCameraTransform, *args):
    currentCamera = cmds.listRelatives(currentCameraTransform, type='camera')[0]
    #create rig lines
    crv_v11 = cmds.curve(p=[(-0.22, 0.5, 0), (-0.22, 0.166667, 0), (-0.22, -0.166667, 0), (-0.22, -0.5, 0)], k=[0,0,0,1,1,1], d=3, n='crv_v11')
    crv_v22 = cmds.curve(p=[(-0.12, 0.5, 0), (-0.12, 0.166667, 0), (-0.12, -0.166667, 0), (-0.12, -0.5, 0)], k=[0,0,0,1,1,1], d=3, n='crv_v22')
    crv_v33 = cmds.curve(p=[(0.0, 0.5, 0), (0.0, 0.166667, 0), (0.0, -0.166667, 0), (0.0, -0.5, 0)], k=[0,0,0,1,1,1], d=3, n='crv_v33')
    crv_v44 = cmds.curve(p=[(0.12, 0.5, 0), (0.12, 0.166667, 0), (0.12, -0.166667, 0), (0.12, -0.5, 0)], k=[0,0,0,1,1,1], d=3, n='crv_v44')
    crv_v55 = cmds.curve(p=[(0.22, 0.5, 0), (0.22, 0.166667, 0), (0.22, -0.2, 0), (0.22, -0.5, 0)], k=[0,0,0,1,1,1], d=3, n='crv_v55')
    #create grid and constrain it
    comp_grid2 = cmds.group(crv_v11, crv_v22, crv_v33, crv_v44, crv_v55, n='comp_grid2')
    comp_grid2_group = cmds.group(comp_grid2, n='comp_grid2_'+currentCameraTransform)
    comp_grid2 = cmds.ls(cmds.listRelatives(comp_grid2_group)[0], long=True)[0]
    print(comp_grid2)
    cmds.xform(comp_grid2, os=True, piv=[0,0,0])
    cmds.parentConstraint(currentCameraTransform, comp_grid2_group)[0]
    cmds.setAttr(comp_grid2+'.scaleX', 3)
    cmds.setAttr(comp_grid2+'.scaleY', 0.48)
    cmds.setAttr(comp_grid2+'.translateX', 0)
    cmds.setAttr(comp_grid2+'.translateY', 0)
    cmds.setAttr(comp_grid2+'.translateZ', -0.83)
    cmds.setAttr(comp_grid2+'.rotateX', 0)
    cmds.setAttr(comp_grid2+'.rotateY', 0)
    cmds.setAttr(comp_grid2+'.rotateZ', 0)
    #allowing grid to be an overlay
    #ability to change aspect ratio
    cmds.expression(s=comp_grid2 + '.scaleX = 2.9 * (35/'+currentCamera+'.focalLength); '+comp_grid2+'.scaleY = 0.858* (35/'+currentCamera+'.focalLength);')
    cmds.createDisplayLayer(n='5linesandpatL', num=1)
    cmds.camera(currentCamera, e=True, dfg=False, dr=True, ovr=1.3)
    cmds.cycleCheck(e=False)
#     toggle overlay
#     if comp grid is selected also toggle the visibility
def toggleLP(connections, currentCameraTransform):
    for c in connections:
        if 'comp_grid2' in c and c != 'comp_grid2_' + currentCameraTransform:
            cmds.rename(c, 'comp_grid2_' + currentCameraTransform)
            connections = ['comp_grid2_' + currentCameraTransform if x==c else x for x in connections]
    
    if connections != None:
        for comp_grid2 in [x for x in connections if 'comp_grid2' in x]: #Check if overlay exists on the selected camera
            currentVis = cmds.getAttr(comp_grid2 +'.visibility') 
            if currentVis==1: 
                cmds.setAttr(comp_grid2 + '.visibility', 0)#If overlay does exist, check if the overlay is currently visible
            else:
                cmds.setAttr(comp_grid2 + '.visibility', 1)#If the over does not exist, make one

#     create main function
def landp(*args):
    for o in cmds.ls(sl=True):
        currentCameraTransform = None
        if cmds.objectType(o) == 'transform':
            if cmds.listRelatives(o, type='camera'):
                currentCameraTransform = o
        elif cmds.objectType(o) == 'camera':
            currentCameraTransform = cmds.listRelatives(o, type='transform', parent=True)[0]
        
        if currentCameraTransform:
            try:
                connections = cmds.listRelatives(list(set(cmds.listConnections(currentCameraTransform,s=False))), parent=True)
            except:
                connections = None

            if connections == None or len([x for x in connections if 'comp_grid2' in x]) == 0:
                linesandpat(currentCameraTransform)
            else:
                toggleLP(connections, currentCameraTransform)
        
        if "comp_grid2" in o:#if comp grid is selected also toggle the visibility
            currentCameraTransform = cmds.parentConstraint(q=True, targetList=True)[0]
            cmds.select(currentCameraTransform)
            connections = [o]
            toggleLP(connections, currentCameraTransform)


def cameraUI():
    if cmds.window('cameraUI', exists = True):
        cmds.deleteUI('cameraUI')  
    cmds.window('cameraUI', widthHeight=(10,10), resizeToFitChildren=True)
    cmds.columnLayout(columnAlign="left")
    cmds.separator(h=10)
    cmds.text('Toggle Camera Theory Tools')
    cmds.separator(h=10)
    cmds.rowLayout(numberOfColumns=3)
    cmds.button(label = 'Create Rule of Thirds Camera ', command = rule3, width=200)
    cmds.button(label = 'Create Lines and Patterns Camera', command = landp, width=200)
    cmds.setParent("..")
    cmds.showWindow('cameraUI')
    
#cameraUI()
