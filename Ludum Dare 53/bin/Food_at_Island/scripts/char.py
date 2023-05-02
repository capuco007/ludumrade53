import bge
from mathutils import Vector
gd = bge.logic.globalDict

def start(cont):
    own = cont.owner
    gd['game']['itemServer'] = []
    gd['game']['coin'] = 10
    own['itemServer'] = gd['game']['itemServer']
    own['limite'] = 3
    gd['game']['reputation'] = 50
    gd['game']['itemList'] = ['suco']
   


def update(cont):
    own = cont.owner
    movement(cont)
    getItem(cont)
    gameOver(cont)
    own['itemServer'] = gd['game']['itemServer']
    #print(gd['game']['itemServer'],gd['game']['itemList'])
    if gd['game']['reputation'] >=100:
        bge.logic.sendMessage('winGame')

def getItem(cont):
    own = cont.owner
    Collision = cont.sensors['Collision']
    scene = own.scene
    if Collision.positive:
        #print(gd['game']['reputation'])
        for o in Collision.hitObjectList:
            if 'getItem' in o:
                if len(own['itemServer'])< own['limite'] and o.groupObject['ativa']:
                    
                    if o['reload'] == 100:
                        if not o.groupObject['tipo'] in gd['game']['itemServer']:
                            own['itemServer'].append(o.groupObject['tipo'])
                            if o.groupObject['tipo'] in scene.objects:
                                scene.objects[o.groupObject['tipo']].endObject()
                            bge.logic.sendMessage('getItem')
                            if o['reload'] == 100:
                                o['reload'] = 0
                        
                       
    
def gameOver(cont):
    own = cont.owner
    scene = own.scene
    water = cont.sensors['water']
    if water.positive:
        bge.logic.sendMessage('gameOver')


def movement(cont):
    own = cont.owner
    tc = bge.logic.keyboard.inputs
    ms = bge.logic.mouse.inputs
    speed = 0.08

    char = bge.constraints.getCharacter(own)
    x = tc[bge.events.DKEY].active - tc[bge.events.AKEY].active
    y = tc[bge.events.WKEY].active - tc[bge.events.SKEY].active

    char.walkDirection = Vector([x,y,0]).normalized()*speed

    if char.onGround:
        if tc[bge.events.SPACEKEY].activated or ms[bge.events.LEFTMOUSE].activated:
            char.jump()
    dir = char.walkDirection
    arm = own.childrenRecursive.get('Armature')
    
    arm.alignAxisToVect( dir,2,1.0 ) 
    if char.onGround:
        if dir.length != 0:
            arm.playAction('run',1,22,play_mode = 2,blendin = 5)
        else:
            arm.playAction('idle',1,251,play_mode = 2,blendin = 5)
    else:
        arm.playAction('fall',1,33,play_mode = 2,blendin = 5)
