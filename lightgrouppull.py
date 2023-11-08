from Katana import NodegraphAPI
from PyQt5 import QtGui
import Nodes3DAPI
from Katana import NodegraphAPI
from Katana import ScenegraphManager
from Katana import DrawingModule
from Katana import Utils
from Katana import Imath
from PyQt5 import QtGui
from Katana import Plugins

GafferThreeAPI = Plugins.GafferThreeAPI

def CalculateNodeDepth(node):
    depth = 0
    parent = node.getParent()
    while parent is not None:
        depth += 1
        parent = parent.getParent()
    return depth

def GetAllNodesByTypeSortedByDepth():
    # Find all nodes of a certain type.
    #in the button put node.name()
    #nodes = NodegraphAPI.GetAllNodesByType('GafferThree', includeDeleted=False,
                                            #sortByName=False)
    # Compute depth of every node.
    nodesAndDepths = []
    for node in nodes:
        depth = CalculateNodeDepth(node)
        nodesAndDepths.append((node, depth))
    # Sort by depth aka reverse as it gets the first input
    nodesAndDepths = sorted(nodesAndDepths, key=lambda elem: elem[1], reverse=True)
    nodessorted = [node for node, depth in nodesAndDepths]
    return nodessorted

def findChildren(groupPackage, packageClass):
    result = []
    #Get the children of groupPackage
    for childPackage in groupPackage.getChildPackages():
        #Check the package we are in - if it is of type packageClass, then add to result, if not, continue
        #Get children of each child
        if isinstance(childPackage, packageClass):
            result += [childPackage]
        result += findChildren(childPackage,packageClass)
    return result

def populateLightGroups(node):
    #node = NodegraphAPI.GetNode('tst01_010_main')
    stream = NodegraphAPI.Util.GetAllConnectedInputs([node])
    gaffers = []
    for n in stream:
        if(n.getType()=="GafferThree"):
            gaffers.append(n)
    lgNames = []
    mutedlgs = []
    for g in gaffers:
        parents = findChildren(g.getRootPackage(),
                                GafferThreeAPI.PackageClasses.RigPackage)

        for rig in parents:
            if("lg_" in rig.getName()):
                #if not rig.isMuted():       REMOVING THIS FEATURE as it was complicating the hierarchy of collecting muted nodes - if updated please check the chain of hierarchy muted rigs as you ned to check the most recent state of the light and then compare
                    #if not rig.isMuteOverrideEnabled():
                        lghts = findChildren(rig, GafferThreeAPI.PackageClasses.PrmanLightPackage)
                        for l in lghts:
                            if l.getMaterialNode().getParameter('shaders.prmanLightParams.lightGroup.value'):
                                l.getMaterialNode().getParameter('shaders.prmanLightParams.lightGroup.value').setValue(rig.getName().split("lg_")[1], 0.0)
                                l.getMaterialNode().getParameter('shaders.prmanLightParams.lightGroup.enable').setValue(True, 0.0)

                                if rig.getName().split("lg_")[1] not in lgNames:
                                    lgNames.append(rig.getName().split("lg_")[1])
                # else:
                #     mutedlgs.append(rig.getName().split("lg_")[1])
                #     print(mutedlgs)
    lgNames = list(set(lgNames))
    # for lg in lgNames:
    #     if lg in mutedlgs:
    #         print(lg)
    #         lgNames.remove(lg)     
    #main = NodegraphAPI.GetNode('tst01_010_main')
    #print(main)
    array = []
    param_group = 'user.lightGroups'
    button = node.getParameter(param_group)
    for s in button.getChildren():
        #print(s)
        if s.getType() == 'string':
            if("lg" in s.getName()):
                array += [s]
                s.setValue("",0)
                if node.getParameter(param_group+"."+s.getName()+"LPEs"):
                    node.getParameter(param_group+"."+s.getName()+"LPEs").setValue(False,0.0)
    for i,lg in enumerate(lgNames):
        array[i].setValue(lg,0)
        if node.getParameter(param_group+"."+array[i].getName()+"LPEs"):
            node.getParameter(param_group+"."+array[i].getName()+"LPEs").setValue(True,0.0)
    print(lgNames)

def clearlgs(node):
    #node = NodegraphAPI.GetNode('seq01_010_main1')
    array=[]
    param_group = 'user.lightGroups'
    button = node.getParameter(param_group)
    for s in button.getChildren():
        if s.getType()== 'string':
            array += [s]
            s.setValue("",0)
