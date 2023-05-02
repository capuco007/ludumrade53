import bge 
import random
gd = bge.logic.globalDict

def start(cont):
    own = cont.owner
    own['timePedir'] = 100
    own['pedirAlgo'] = None
    own['pedirReload'] = 100
    own['mesh_icon'] = [o for o in own.childrenRecursive if 'mesh_icon' in o]
    own['timer_mostrar'] = [o for o in own.childrenRecursive if 'timer_mostra' in o]
    own['perdeu'] = False
    #print(own['mesh_icon'])

def timePedir(cont):
    own = cont.owner
    if own['pedirReload'] > 0:
        own['pedirReload'] -=20
    else:
        own['pedirReload'] = 100
        
    if own['pedirReload'] == 0:
        if own['timePedir'] >0:
            own['timePedir'] -=1




def update(cont):
    own = cont.owner
    coll = cont.sensors['Collision']
    scene = own.scene
    grupo = own.groupObject
    #print(own['timePedir'],own['pedirReload'])
    if grupo['ocuped'] :
        if own['timePedir']>0:
            timePedir(cont)
            for o in own['timer_mostrar']:
                o['timer_mostra'] = own['timePedir']
                o.visible = True
    else:
        for o in own['timer_mostrar']:
            o['timer_mostra'] = own['timePedir']
            o.visible = False
            own['mesh_icon'][0].replaceMesh('nada')


    #grupo = own.groupObject
    if gd['game']['reputation'] >= grupo['open']:
        grupo['ocuped'] = True
    if grupo['ocuped'] :
        #print(own['pedirAlgo'],'pedirMesa',own['timePedir'],own['pedirReload'])
        if own['pedirAlgo'] == None:
            for o in own['timer_mostrar']:
                o.visible = False
            if own['timePedir'] == 100:
                own['perdeu'] = False
        
                
                own['mesh_icon'][0].replaceMesh('nada')
                o  = random.choice(gd['game']['itemList'])
                own['pedirAlgo'] = o
                own['mesh_icon'][0].replaceMesh(str(own['pedirAlgo']))
           
     
            
        else:
            #own['mesh_icon'][0].replaceMesh(str(own['pedirAlgo']))
           
            if coll.positive and own['timePedir']>0:
                if str(own['pedirAlgo']) in gd['game']['itemServer']:
                    gd['game']['itemServer'].remove(own['pedirAlgo'])
                    own['mesh_icon'][0].replaceMesh('nada')
                    own['timePedir'] = 80
                    if not 'coin_efect' in scene:
                        scene.addObject('coin_efect',own,150)
                        bge.logic.sendMessage('win')

                   
                    
                    gd['game']['coin']+= gd['game']['itemValue'][own['pedirAlgo']]
                    gd['game']['reputation']+= gd['game']['itemValue'][own['pedirAlgo']]
                    
                    own['pedirAlgo'] = None
                    #grupo['ocuped'] = False
                    

            
    
    if own['timePedir'] <= 2 and own['pedirAlgo']:
        if gd['game']['reputation'] >0 and own['perdeu'] == False:
            own['perdeu'] = True
            scene.addObject('bravo_effect',own,150)
            gd['game']['reputation']-= gd['game']['itemReputation'][own['pedirAlgo']]
            bge.logic.sendMessage('lose')
       
    if own['timePedir'] == 0:
        own['timePedir'] = 100
        grupo['ocuped'] = True
        own['perdeu'] = False
