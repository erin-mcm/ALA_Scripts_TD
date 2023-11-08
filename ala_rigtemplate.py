import maya.cmds as cmds
import shotgun_utils
import sgtk
import os 
from turret import resolver
from maya_pipeline import utils

    
def ASSET_DETAILS():
    engine = sgtk.platform.current_engine()
    context = engine.context
    ASSET_TYPE = context.source_entity.get('entity.Asset.sg_asset_type')
    ASSET_NAME = context.entity.get('name')
    PROJECT_CODE = shotgun_utils.get_project_code()
    return ASSET_NAME, ASSET_TYPE, PROJECT_CODE

def rootGroup():
    ASSET_NAME, ASSET_TYPE, PROJECT_CODE = ASSET_DETAILS()
    
    if len(cmds.ls(ASSET_NAME)) == 0:
        GEO = cmds.group(em=True, name='GEO')
        cacheable = cmds.addAttr(at='bool', dv=True, ln='Cacheable')
        lookfileURI = cmds.addAttr(dt="string", ln='lookfileUri')
        cmds.setAttr(GEO + '.lookfileUri', 'tank:/'+PROJECT_CODE+'/katana_publish_asset_lookfiles_path?Task=surfacing&extension=klf&Step=surfacing&version=latest&Asset='+ASSET_NAME+'&asset_type='+ASSET_TYPE, type="string") 
        userExportedAttr = cmds.addAttr(dt="string", ln='userExportedAttributesJson')
        cmds.setAttr(GEO + '.userExportedAttributesJson', '{"lookfileUri": {"usdAttrName": "userProperties:lookfileUri"}}', type="string")
        lookfileoverrideasset = cmds.addAttr(dt="string", ln='lookfileOverrideAsset')
        referencein(GEO)
        CONTROLS = cmds.group(em=True, name='CONTROLS')
        cmds.group(GEO, CONTROLS, name=ASSET_NAME)
        utils.check_rig_versions()
    else:
        cmds.confirmDialog(title='Rig Builder', message="Hierarchy already exists. please run on a fresh scene", button='OK')

def referencein(parent_node):
    ASSET_NAME, ASSET_TYPE, PROJECT_CODE = ASSET_DETAILS()
    engine = sgtk.platform.current_engine()
    tk = shotgun_utils.get_tk()
    rig_fields = resolver.filepath_to_fields(cmds.file(q=True, sn=True))
    model_fields = rig_fields
    model_fields['Task'] = 'model'
    model_fields['Step'] = 'model'
    
    model_publish_template = tk.templates['maya_publish_asset_source_path']
    model_path = model_publish_template.apply_fields(model_fields)
    
    ref = cmds.file(
        model_path,
        reference=True,
        lockReference=False,
        loadReferenceDepth="all",
        namespace="mRef",
        returnNewNodes=False
    )
    ref_node = cmds.referenceQuery(ref, referenceNode=True)
    
    nodes_in_reference = cmds.referenceQuery(ref_node, nodes=True, dp=True, n=True) or []
    if nodes_in_reference:
        transforms = cmds.ls(nodes_in_reference, type='transform', l=True)

        top_nodes = [t for t in transforms if not cmds.listRelatives(t, p=True)]
        for node in top_nodes:
            cmds.parent(node, parent_node)
        

#rootGroup()
