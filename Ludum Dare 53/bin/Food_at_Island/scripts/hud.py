import bge
gd = bge.logic.globalDict
def start(cont):
    own = cont.owner
    scene = own.scene
    own['coins'] = [o for o in scene.objects if 'coin' in o]

def update(cont):
    own = cont.owner
    own['reputation'] = gd['game']['reputation']
    for o in own['coins']:
        o['coin'] = gd['game']['coin']
   