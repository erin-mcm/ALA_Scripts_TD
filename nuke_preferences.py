import sys
import os

import nuke

r = nuke.root()

r['colorManagement'].setValue('OCIO')
r['workingSpaceLUT'].setValue('ACES - ACEScg')
r['int8Lut'].setValue('Utility - sRGB - Texture')
r['int16Lut'].setValue('ACES - ACEScc')

from nuke_pipeline import loadPlugins
loadPlugins.loadPlugins()

def init_lg_gizmos():
    nodes = nuke.allNodes('lightGroupGrade')
    nodes += nuke.allNodes('lightGroupCombine')
    nodes += nuke.allNodes('lightGroupMerge')

    for node in nodes:
        node.knob('connect').execute()


nuke.addOnScriptLoad(init_lg_gizmos)

sys.stdout.writelines('\nstartup\n')
print ('\nstartup\n')

try:
    f =  sys.argv[1]
    nuke.scriptOpen(f)
except:
    pass