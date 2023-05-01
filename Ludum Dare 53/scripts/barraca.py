import bge
gd = bge.logic.globalDict

def start(cont):
    own = cont.owner
    own['reload'] = 100
    own['timeReload'] = 0
    own['proportionReload'] = 0
    own['mostValue'] = [o for o in own.childrenRecursive if 'cash' in o]
    own['bar_time'] = [o for o in own.childrenRecursive if 'bar_time' in o]
    own['addObject'] = [o for o in own.childrenRecursive if 'addObj' in o]
    own['added'] = False

   

def timeReload(cont):
    own = cont.owner
    speed = 25 #own.groupObject['speed']
    if own['timeReload'] >0:
        own['timeReload'] -= speed
    if own['timeReload'] == 0:

        own['timeReload'] = 100
        if own['reload'] < 100:
            own['reload'] +=1
    
        

def update(cont):
    own = cont.owner
    scene = own.scene
    coll = cont.sensors['Collision']
    tc = bge.logic.keyboard.inputs
    ms = bge.logic.mouse.inputs
    #print(own['reload'],own['bar_time'])
    if own.groupObject['ativa']:
        if own['reload'] == 99 and own['added'] == True:
            own['added']= False
        if own['reload'] == 100 and own['added'] == False:
            own['added'] = True
            print('ok')
            scene.addObject(own.groupObject['tipo'],own['addObject'][0],0)

        for o in own['bar_time']:
            o['bar_time'] = own['reload']
            o.visible = True
        for o in own['mostValue']:
            o.visible = False
        if coll.positive:
            if own['reload'] == 100 and own.groupObject['tipo'] in gd['game']['itemList']:
                pass
                #own['reload'] = 0
        

        if own['reload'] < 100:
            timeReload(cont)
    else:
        for o in own['mostValue']:
            o.visible = True
            o['cash'] = own.groupObject['value']
        if coll.positive:
            if gd['game']['coin'] >= own.groupObject['value']:
                if tc[bge.events.EKEY].activated:
                    gd['game']['coin'] -= own.groupObject['value']
                    gd['game']['itemList'].append(own.groupObject['tipo'])
                    own.groupObject['ativa'] = True
                    own['added'] = False
                    
                    
