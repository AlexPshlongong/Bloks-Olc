from setup import *


# TO DO
def TO_DO():
    # CURRENTLY WORKING ON 
    """
    fix particles from damaging buildings
    any item into hotbar
    split 1 stone to be in hotbar, rest stones in inventory

    structure spacing so structures don't spawn in structures

    compatibility with other window resolutions (crafting still bugged)
    dropping items
    horizontal loop (generate world, flip all of it and stick it on the end, then allow player to loop)
    driftwood - wood as a dropped item just spawns at shores
    lighting
    """
    # little things
    """
    terraformer in godmode but actually fun large area and don't do just "change only this tile" change a circle around the mouse
    smoother biome transition -> defo i think but idk how to do just yet
    stone buildings a lot darker or make dark varient
    SHIFT CLICK IN INVENTORY AND HOTBAR (this is a MUST with chests)
    wall sprites darker (definitely outline, idk for everything else)
    optimise displaying tiles (somehow)
    saving and loading (encoding too maybe, to save storage and prevent cheating)
    breaking buildings proper particles and not just black
    minimap
    chunks (good luck mate)
    "can't go to next biome without doing / killing so and so"
    lots of fun wierd achievements
    """
    # CONTENT
    """
    chests 
    animals
    fishing
    bosses
    bow with that really cool and fun mechanic i thoguht of ages ago
    DIMENTIONS!!! (like underground caves, above cloud islands???, setting off to sea in a boat to other islands)
    wiring
    skill tree like in my scratch game and experience points for different activities like running and farming like in valheim
    temperature / conduction / insulation
    magic like spells and whatever (arrow keys like in wynncraft)
    "upgrading" preexisting tools and armour with crystals or whatever
    zenith type crafting like in terraria
    effects
    """

# PLAYER

def move_player(ks):
    player.tile = min(len(tiles)-1, int((player.y+worldHAccHeight)/tileSize)+int((player.x+worldHAccWidth)/tileSize)*worldHeight)
        
    playerX_1 = min(len(tiles)-1, int((player.y+worldHAccHeight)/tileSize)+int((player.x-player.fWidth+worldHAccWidth)/tileSize)*worldHeight)
    playerX_2 = min(len(tiles)-1, int((player.y+worldHAccHeight)/tileSize)+int((player.x+player.fWidth+worldHAccWidth)/tileSize)*worldHeight)
    
    sprintX = player.sprintMultiplier
    decSpeed = player.decSpeed
    if ks[pygame.K_LSHIFT]:
        if not game_settings.GODMODE:
            player_deenergize(0.1)
        accspeed = player.speed*sprintX
        maxSpeed = player.maxSpeed*sprintX
    else:
        accspeed = player.speed
        maxSpeed = player.maxSpeed
    if tiles[playerX_1].tile == "ice" and tiles[playerX_2].tile == "ice":
        decSpeed*=0.05
        accspeed*=0.1
        maxSpeed*=2
    
    player.xAcc += (ks[pygame.K_d] - ks[pygame.K_a])*accspeed
    player.yAcc += (ks[pygame.K_s] - ks[pygame.K_w])*accspeed
    
    if player.yAcc > maxSpeed:
        player.yAcc-=decSpeed*(player.yAcc-maxSpeed)/20
    if player.yAcc < maxSpeed*-1:
        player.yAcc-=decSpeed*(player.yAcc-maxSpeed*-1)/20
    if player.xAcc > maxSpeed:
        player.xAcc-=decSpeed*(player.xAcc-maxSpeed)/20
    if player.xAcc < maxSpeed*-1:
        player.xAcc-=decSpeed*(player.xAcc-maxSpeed*-1)/20

    if (ks[pygame.K_w] and player.yAcc > 0) or (ks[pygame.K_s] and player.yAcc < 0) or not (ks[pygame.K_s] - ks[pygame.K_w]) :
        player.yAcc-=decSpeed*player.yAcc/20
    if (ks[pygame.K_a] and player.xAcc > 0) or (ks[pygame.K_d] and player.xAcc < 0) or not (ks[pygame.K_a] - ks[pygame.K_d]):
        player.xAcc-=decSpeed*player.xAcc/20
            
    
    player.y += player.yAcc
    if not game_settings.GODMODE:
        xCol_1 = int((player.y+worldHAccHeight)/tileSize)+int((player.x-player.fWidth+worldHAccWidth)/tileSize)*worldHeight
        xCol_2 = int((player.y+worldHAccHeight)/tileSize)+int((player.x+player.fWidth+worldHAccWidth)/tileSize)*worldHeight
        if not tiles[xCol_1].canwalk or not tiles[xCol_2].canwalk:
            player.y -= player.yAcc
            # make player.yAcc smaller until no collision but for now i make it zero because yes
            player.yAcc = 0
    player.x += player.xAcc
    if not game_settings.GODMODE:
        xCol_1 = int((player.y+worldHAccHeight)/tileSize)+int((player.x-player.fWidth+worldHAccWidth)/tileSize)*worldHeight
        xCol_2 = int((player.y+worldHAccHeight)/tileSize)+int((player.x+player.fWidth+worldHAccWidth)/tileSize)*worldHeight
        if not (worldHAccWidth*-1+player.halfWidth < player.x < worldHAccWidth-player.halfWidth):
            player.x -= player.xAcc
            # make player.xAcc smaller until no collision but for now i make it zero because yes
            player.xAcc = 0
        else:
            if not tiles[xCol_1].canwalk or not tiles[xCol_2].canwalk:
                player.x -= player.xAcc
                # make player.xAcc smaller until no collision but for now i make it zero because yes
                player.xAcc = 0
                
    player.xCol_1 = int((player.y+worldHAccHeight)/tileSize)+int((player.x-player.fWidth+worldHAccWidth)/tileSize)*worldHeight
    player.xCol_2 = int((player.y+worldHAccHeight)/tileSize)+int((player.x+player.fWidth+worldHAccWidth)/tileSize)*worldHeight   

    #stops oyu from crashing the game with an index tile out of range
    player.x = min(worldHAccWidth, max(-worldHAccWidth, player.x))
    player.y = min(worldHAccHeight, max(-worldHAccHeight, player.y))
def check_player_reach():
    player.reach = game_settings.basePlayerReach
    for enhancement in player.hotbar[0].enhancements:
        if enhancement == "reach":
            player.reach += tileSize/3
    if (mouse.x-(player.x+camera.x))**2+(mouse.y-(player.y+camera.y))**2 < player.reach**2:
        player.inReach = True
    else:
        player.inReach = False    
def pos_arms():
    arm[0].ankX = player.x-player.fWidth-arm[0].width+arm[0].offset
    arm[0].ankY = player.y-arm[0].height-4
    arm[1].ankX = player.x+player.fWidth+arm[1].width-arm[1].offset
    arm[1].ankY = player.y-arm[1].height-4
    for i in range(2):
        if arm[i].punching > 1:
            arm[i].punching-=player.attackSpeed
        elif arm[i].punching < 1:
            arm[i].punching = 1
            
    if arm[player.punchTurn].holdingItem == "":
        arm[0].x = arm[0].ankX+(math.cos(math.radians(arm[0].angleANK+90))*(arm[0].height-4-((4-arm[0].punching/2)**2)))
        arm[0].y = arm[0].ankY-(math.sin(math.radians(arm[0].angleANK+90))*(arm[0].height-4-((4-arm[0].punching/2)**2)))
        arm[1].x = arm[1].ankX+(math.cos(math.radians(arm[1].angleANK+90))*(arm[1].height-4-((4-arm[1].punching/2)**2)))
        arm[1].y = arm[1].ankY-(math.sin(math.radians(arm[1].angleANK+90))*(arm[1].height-4-((4-arm[1].punching/2)**2)))
    else:
        arm[0].x = arm[0].ankX+(math.cos(math.radians(arm[0].angle+90))*(arm[0].height/2-4))
        arm[0].y = arm[0].ankY-(math.sin(math.radians(arm[0].angle+90))*(arm[0].height/2-4))
        arm[1].x = arm[1].ankX+(math.cos(math.radians(arm[1].angle+90))*(arm[1].height/2-4))
        arm[1].y = arm[1].ankY-(math.sin(math.radians(arm[1].angle+90))*(arm[1].height/2-4)) 
def cal_arm_angle():
    for i in range(2):
        armX = arm[i].ankX+camera.x
        armY = arm[i].ankY+camera.y
        arm[i].angle = 0
        if (armX-mouse.x):
            arm[i].angle = math.atan((mouse.y-armY)/(armX-mouse.x))*57.8571428
            arm[i].angle -=90
            arm[i].angle = abs(arm[i].angle)
            if mouse.x < armX:
                arm[i].angle+=180
        else:
            if mouse.y > armY:
                arm[i].angle = 180
            else:
                arm[i].angle = 0
        arm[i].angle*=-1
            
        if arm[i].punching <= 3 or game_settings.GODMODE or arm[i].holdingItem == "":
            arm[i].angleANK = arm[i].angle
        
        if arm[i].holdingItem != "":
            if arm[i].punching > 2:
                if abs(arm[i].angle) > 180:
                    arm[i].angle = arm[i].angleANK-(9**2-(13-arm[i].punching*1.5)**2)
                else:
                    arm[i].angle = arm[i].angleANK+(9**2-(13-arm[i].punching*1.5)**2)
            else:
                if abs(arm[0].angle) > 180:
                    arm[i].angle = arm[i].angleANK
                else:
                    arm[i].angle = arm[i].angleANK      
def craft(craft, resourcesNeeded, amountNeeded):
    # check if player has enough items
    gotItems = []
    for i in range(len(resourcesNeeded)):
        gotItems.append(False)
    for i in range(len(resourcesNeeded)):
        for j in range(len(player.inventoryTotalItem)):
            if player.inventoryTotalItem[j] == resourcesNeeded[i]:
                if player.inventoryTotalAmount[j] >= amountNeeded[i]:
                    gotItems[i] = True
    
    canCraft = True
    for i in range(len(gotItems)):
        if not gotItems[i]:
            canCraft = False
            
                
    # actually craft
    if canCraft:
        crafting_settings.craftingAnimation = 20
        found = False
        # give player the item
        if craft.tag == "resource":
            for i in range(len(player.inventory)):
                if player.inventory[i].item == craft.item and player.inventory[i].amount < game_settings.maxStack:
                    player.inventory[i].amount +=1
                    found = True
                    break
        if not found:
            for i in range(len(player.inventory)):
                if player.inventory[i].item == "":
                    player.inventory[i].amount = 1
                    player.inventory[i].item   = craft.item
                    player.inventory[i].tag    = craft.tag
                    player.inventory[i].weight = weightsdict[craft.item]
                    if craft.tag == "tool":
                        player.inventory[i].durability = craftedItemDurability[player.inventory[i].item.split(" ")[0]]
                    player.inventory[i].sprite = pygame.transform.scale(pygame.image.load("sprites/items/"+craft.item+".png"), (64, 64))
                    break
        
        # remove items needed to make it
        for j in range(len(resourcesNeeded)):
            for i in range(len(player.inventory)):
                needed = amountNeeded[j]
                if player.inventory[i].item == resourcesNeeded[j]:
                    if amountNeeded[j] > 0:
                        for k in range(needed):
                            player.inventory[i].amount-=1
                            needed-=1
                            if player.inventory[i].amount <= 0:
                                player.inventory[i] = INVENTORY_ITEM()
                                break
                    break

    
    update_inventory_total()          
def player_build():
    if game_settings.GODMODE:
        canBuild = True
    else:
        canBuild = False
        temp = buildingResources[building_settings.buildSelected[1]]
        amountNeeded = temp
        amountTaken = 0
        breaking = False
        for i in range(len(player.inventoryTotalItem)):
            if player.inventoryTotalItem[i] == building_settings.buildSelected[0]:
                if player.inventoryTotalAmount[i] >= amountNeeded:
                    canBuild = True
                    for j in range(len(player.inventory)):
                        if player.inventory[j].item == building_settings.buildSelected[0]:
                            for k in range(amountNeeded):
                                amountTaken += 1
                                player.inventory[j].amount -= 1
                                update_inventory_total()
                                if amountTaken >= amountNeeded:
                                     breaking = True
                                     if player.inventory[j].amount <= 0:
                                         player.inventory[j].sprite = ""
                                         player.inventory[j] = INVENTORY_ITEM()
                                     break
                                if player.inventory[j].amount <= 0:
                                     player.inventory[j].sprite = ""
                                     player.inventory[j] = INVENTORY_ITEM()
                                     break
                        if breaking:
                            break
                           
    if canBuild:
        place_building(mouse.tile, building_settings.buildSelected[0], building_settings.buildSelected[1])
        if not game_settings.GODMODE:
            decrease_held_item_durability()
def place_building(tile, building_material, building_type):
    if tile >= len(tiles):
        return
    if building_type == "wall" or building_type == "door":
        tiles[tile].canwalk = False
    if building_type == "floor":
        tiles[tile].canwalk = True
    tiles[tile].building = building_type
    sprite = pygame.image.load("sprites/buildings/"+building_type+"/"+building_material+"/.png")
    tiles[tile].buildSprite = pygame.transform.scale_by(sprite, (tileSize/16))
    tiles[tile].buildSprite.set_alpha(255)
    tiles[tile].i = "tile"
    tiles[tile].health = buildingHealths[building_material+" "+building_type]
    tiles[tile].tag = buildingTags[building_material]
    tiles[tile].material = building_material
    tiles[tile].col = BLACK
    if building_type == "wall" or building_type == "door":
        tiles[tile].buildingMinimapColour = buildings_minimap_dictionary[building_material+" building"]
    elif building_type == "floor":
        tiles[tile].buildingMinimapColour = buildings_minimap_dictionary[building_material+" floor"]
    else:
        tiles[tile].buildingMinimapColour = buildings_minimap_dictionary[building_type]
def destroy_building(index):
    tiles[index].health = 0 
    tiles[index].buildingSprite = ""
    tiles[index].tag = ""
    tiles[index].i = ""
    tiles[index].building = ""
    if tiles[index].tile != "water":
        tiles[index].canwalk = True
    else:
        tiles[index].canwalk = False
def player_deenergize(points):
    player.hunger  -= points/5
    player.hydration  -= points/2
    player.energy  -= points*4
    player.stamina -= points/5
    if player.energy <= 0:
        player.hunger -= points/5*5
        player.hydration -= points/2*5
        player.stamina -= points/5*5
    if player.energy < -5:
        player.energy = -5
    if player.hydration <= 0:
        player.hydration = 100
        player.health -= 1
    if player.hunger <= 0:
        player.hunger = 100
        player.health -= 1
def player_energize():
    if player.energy < player.stamina:
        player.energy += 0.2
        if player.energy > player.stamina:
            player.energy = player.stamina
def passive_deenergize():
    player.hunger  -= 0.01
    player.hydration  -= 0.02
    player.energy  -= 0.01
    player.stamina -= 0.01
def use_item():
    if int(arm[0].punching) <= 1 and int(arm[1].punching) <= 1:
        if not game_settings.GODMODE:
            player_deenergize(1)
        arm[player.punchTurn].punching = 15
        if arm[player.punchTurn].holdingItem == "":
            if player.punchTurn:
                player.punchTurn-=1
            else:
                player.punchTurn+=1

        if tiles[mouse.tile].tile == "water" and (mouse.tile == player.xCol_1 or mouse.tile == player.xCol_2):
            return
        if player.inReach:
            for i in range(game_settings.GODMODE*game_settings.splashMine+1):
                for j in range(game_settings.GODMODE*game_settings.splashMine+1):
                    if game_settings.GODMODE:
                        if -1 < int((mouse.y-tileSize+(tileSize*i)-camera.y+worldHAccHeight)/tileSize)+int((mouse.x-tileSize+(tileSize*j)-camera.x+worldHAccWidth)/tileSize)*worldHeight < worldSize:
                            mouse.tile = int((mouse.y-tileSize+(tileSize*i)-camera.y+worldHAccHeight)/tileSize)+int((mouse.x-tileSize+(tileSize*j)-camera.x+worldHAccWidth)/tileSize)*worldHeight
                    
                    if player.hotbar[0].item != "wood hammer":
                        if tiles[mouse.tile].building != "":
                            if tiles[mouse.tile].health > 0:
                                for item in itemDamages:
                                    if item[0] == player.hotbar[0].item:
                                        if item[1] == tiles[mouse.tile].tag:
                                            tiles[mouse.tile].health -= item[2]+game_settings.GODMODE*10000
                                            for k in range(len(player.hotbar[0].enhancements)):
                                                if player.hotbar[0].enhancements[k] == "damage":
                                                    tiles[mouse.tile].health -= item[2]/3+game_settings.GODMODE*10000
                                            create_particles(tiles[mouse.tile].x-camera.x, tiles[mouse.tile].y-camera.y, tiles[mouse.tile].col[0], tiles[mouse.tile].col[1], tiles[mouse.tile].col[2], 20, 20)
                                            
                            if tiles[mouse.tile].health <= 0:
                                if tiles[mouse.tile].building == "floor" or tiles[mouse.tile].building == "door" or tiles[mouse.tile].building == "wall":
                                    for k in range(0, buildingResources[tiles[mouse.tile].building]):
                                        droppedItems.append(DROPPED_ITEM(tiles[mouse.tile].x, tiles[mouse.tile].y, tiles[mouse.tile].material, [], False))
                                else:
                                    for drop in dropsDict[tiles[mouse.tile].building]:
                                    
                                        luckMin = drop[1]
                                        luckMax = drop[2]
                                        for enhancement in player.hotbar[0].enhancements:
                                            if enhancement == "luck":
                                                luckMin *= 1.2
                                                luckMax *= 1.5 
                                                
                                        for k in range(int(random.randint(int(luckMin), int(luckMax))/100)):
                                            droppedItems.append(DROPPED_ITEM(tiles[mouse.tile].x, tiles[mouse.tile].y, drop[0], [], False))
                                destroy_building(mouse.tile)

                            if player.hotbar[0].item != "stone":
                                for enhancement in player.hotbar[0].enhancements:
                                    if enhancement != "durability":
                                        player.hotbar[0].durability-=0.2
                                player.hotbar[0].durability-=0.2
                                player.hotbar[0].durability = round(player.hotbar[0].durability, len(str(int(player.hotbar[0].durability)+1)))
                                decrease_held_item_durability()
        
        mouse.tile = int((mouse.y-camera.y+worldHAccHeight)/tileSize)+int((mouse.x-camera.x+worldHAccWidth)/tileSize)*worldHeight 
def nuke():
    curTile = int((camera.y*-1+mouse.y)/tileSize)+int((camera.x*-1+mouse.x)/tileSize)*worldHeight
    for i in range(20):
        for k in range(20):
            if tiles[curTile].building != "":
                tiles[curTile].building = ""
                tiles[curTile].buildingSprite = ""
                tiles[curTile].health = 0
                tiles[curTile].tag = ""
                tiles[curTile].i = ""
                tiles[curTile].canwalk = True
                tiles[curTile].drops = []
            if curTile < worldSize-1:
                curTile += 1
        if curTile < worldSize-(worldHeight):
            curTile += worldHeight-displayTHeight
def display_held_item():
    arm[0].holdingItem = player.hotbar[0].item
    if player.hotbar[0].item != "":
        arm[0].holdingItemSprite = pygame.transform.scale(player.hotbar[0].sprite, (32, 32))
        player.punchTurn = 0  
def handle_building():
    if player.hotbar[0].item == "wood hammer":
        if mouse.right:
            display_building_panel()
        if len(building_settings.buildSelected):
            if mouse.release:
                building_settings.sprite = pygame.transform.scale(pygame.image.load("sprites/buildings/"+building_settings.buildSelected[1]+"/"+building_settings.buildSelected[0]+"/.png"), (tileSize, tileSize))
                if building_settings.buildSelected[1] == "wall" or building_settings.buildSelected[1] == "door":
                    building_settings.sprite = pygame.transform.scale(building_settings.sprite, (tileSize, tileSize*1.5))

            if player.inReach and (tiles[mouse.tile].building == "" or (tiles[mouse.tile].building[-5:len(tiles[mouse.tile].building)] == "floor" and (building_settings.buildSelected[1] == "wall" or building_settings.buildSelected[1] == "door"))):
                if ((building_settings.buildSelected[1] == "wall" or building_settings.buildSelected[1] == "door") and (mouse.tile != player.xCol_1 and mouse.tile != player.xCol_2) or building_settings.buildSelected[1] in "floor"):
                    display_ghost_building(frame)
                    if mouse.left:
                        player_build()
    else:
        building_settings.buildSelected = []
        if player.inReach:
            display_selected_tile()
    if building_settings.buildSelected != []:
        write_text(str(buildingResources[building_settings.buildSelected[1]]), mouse.x+20, mouse.y, 35, False, 200)
        window.blit(buildResourceSprites[building_settings.buildSelected[0]], (mouse.x+55, mouse.y))
        playerHasEnough = False
        for i in range(len(player.inventoryTotalAmount)):
            if player.inventoryTotalItem[i] == building_settings.buildSelected[0]:
                if buildingResources[building_settings.buildSelected[1]] <= player.inventoryTotalAmount[i]:
                    playerHasEnough = True
        if not playerHasEnough:
            window.blit(crossImg, (mouse.x+55, mouse.y))

# MOUSE

def mouseHBCheck():
    if (mouse.x-(game_settings.displayHalfWidth))**2+(mouse.y-(game_settings.displayHeight-150))**2 < 55**2:
        mouse.selectedHBSlot = 0
    else:
        if (mouse.y-(game_settings.displayHeight-150))*0.485 > (mouse.x-game_settings.displayHalfWidth):
            if (mouse.y-(game_settings.displayHeight-150))*-0.485 < (mouse.x-game_settings.displayHalfWidth):
                mouse.selectedHBSlot = 6+player.HBcycle
            elif (mouse.y-(game_settings.displayHeight-150)) > (mouse.x-game_settings.displayHalfWidth)*-0.485:
                mouse.selectedHBSlot = 5+player.HBcycle
            elif (mouse.y-(game_settings.displayHeight-150)) > (mouse.x-game_settings.displayHalfWidth)*0.485:
                mouse.selectedHBSlot = 4+player.HBcycle
            else:
                mouse.selectedHBSlot = 3+player.HBcycle
        else:
            if (mouse.y-(game_settings.displayHeight-150))*-0.485 > (mouse.x-game_settings.displayHalfWidth):
                mouse.selectedHBSlot = 2+player.HBcycle
            elif (mouse.y-(game_settings.displayHeight-150)) < (mouse.x-game_settings.displayHalfWidth)*-0.485:
                mouse.selectedHBSlot = 1+player.HBcycle
            elif (mouse.y-(game_settings.displayHeight-150)) < (mouse.x-game_settings.displayHalfWidth)*0.485:
                mouse.selectedHBSlot = 8+player.HBcycle
            else:
                mouse.selectedHBSlot = 7+player.HBcycle
        if mouse.selectedHBSlot > 8:
            mouse.selectedHBSlot -= 8
        if mouse.selectedHBSlot < 1:
            mouse.selectedHBSlot += 8          
def set_mouse_vars():
    mouse.x, mouse.y = pygame.mouse.get_pos()
    mouse.left = pygame.mouse.get_pressed()[0]
    mouse.right = pygame.mouse.get_pressed()[2]
    if game_settings.menu != "pregame":
        mouse.tile = int((mouse.y-camera.y+worldHAccHeight)/tileSize)+int((mouse.x-camera.x+worldHAccWidth)/tileSize)*worldHeight
def inventory_mouse():
    if game_settings.displayHalfWidth-inventoryImg.get_width()/2 < mouse.x < game_settings.displayHalfWidth+inventoryImg.get_width()/2 and game_settings.displayHalfHeight-inventoryImg.get_height()/2-100 < mouse.y < game_settings.displayHalfHeight+inventoryImg.get_height()/2-100:
        mouse.selectedSlot = abs(int((game_settings.displayHalfWidth-inventoryImg.get_width()/2-mouse.x)/108))+abs(int((game_settings.displayHalfHeight-inventoryImg.get_height()/2-100-mouse.y)/108))*5
        if mouse.click:
            if mouse.offInvBeat:
                if player.selectedHBSlot == "":
                    if player.inventory[player.selectedSlot].item == player.inventory[mouse.selectedSlot].item and (player.inventory[player.selectedSlot].tag == "resource" or player.inventory[player.selectedSlot].item == "stone") and (player.inventory[mouse.selectedSlot].tag == "resource" or player.inventory[mouse.selectedSlot].item == "stone"):
                        if player.selectedSlot != mouse.selectedSlot:
                            if player.inventory[player.selectedSlot].amount+player.inventory[mouse.selectedSlot].amount <= game_settings.maxStack:
                                player.inventory[mouse.selectedSlot].amount = player.inventory[player.selectedSlot].amount+player.inventory[mouse.selectedSlot].amount
                                player.inventory[player.selectedSlot] = INVENTORY_ITEM()
                            else:
                                player.inventory[player.selectedSlot].amount = game_settings.maxStack-(player.inventory[player.selectedSlot].amount+player.inventory[mouse.selectedSlot].amount)
                                player.inventory[mouse.selectedSlot].amount = game_settings.maxStack
                    else:
                        temp = player.inventory[player.selectedSlot]
                        player.inventory[player.selectedSlot] = player.inventory[mouse.selectedSlot]
                        player.inventory[mouse.selectedSlot] = temp
                    player.selectedSlot = ""
                else:
                    temp = player.hotbar[player.selectedHBSlot]
                    player.hotbar[player.selectedHBSlot] = player.inventory[mouse.selectedSlot]
                    player.inventory[mouse.selectedSlot] = temp
                    player.selectedHBSlot = ""
                mouse.offInvBeat = False
            else:
                player.selectedSlot = mouse.selectedSlot
                mouse.offInvBeat = True     
    else:
        mouse.selectedSlot = ""
def inventory_mouse_hotbar():
    if (mouse.x-(game_settings.displayHalfWidth))**2+(mouse.y-(game_settings.displayHeight-150))**2 < 150**2:
        mouseHBCheck()
        if mouse.click:
            if mouse.offInvBeat:
                Mslot = mouse.selectedHBSlot
                if player.selectedHBSlot != "":
                    Pslot = player.selectedHBSlot
                    if Pslot > 8:
                        Pslot-=8
                if Mslot > 8:
                    Mslot-=8
                if player.selectedSlot == "":
                    temp = player.hotbar[Pslot]
                    player.hotbar[Pslot] = player.hotbar[Mslot]
                    player.hotbar[Mslot] = temp
                    player.selectedHBSlot = ""
                else:
                    if player.inventory[player.selectedSlot].tag == "tool":
                        temp = player.inventory[player.selectedSlot]
                        player.inventory[player.selectedSlot] = player.hotbar[Mslot]
                        player.hotbar[Mslot] = temp
                    if player.inventory[player.selectedSlot].item == "stone":
                        if player.hotbar[Mslot].item == "":
                            if player.inventory[player.selectedSlot].amount > 1:
                                temp = player.inventory[player.selectedSlot]
                                temp.amount -= 1
                                player.inventory[player.selectedSlot] = player.hotbar[Mslot]
                                player.hotbar[Mslot] = temp
                        elif player.inventory[player.selectedSlot].amount == 1:
                            temp = player.hotbar[Pslot]
                            player.hotbar[Pslot] = player.hotbar[Mslot]
                            player.hotbar[Mslot] = temp

                    player.selectedSlot = ""
                mouse.offInvBeat = False
            else:
                player.selectedHBSlot = mouse.selectedHBSlot
                mouse.offInvBeat = True
    else:
        mouse.selectedHBSlot = ""     

# GAME MECHANICS

def move_items():
    for item in droppedItems:
        if item.goingX > 0:
            item.x+=item.goingX
            item.goingX-=1
        if item.goingX < 0:
            item.x+=item.goingX
            item.goingX+=1
        if item.goingY > 0:
            item.y+=item.goingY
            item.goingY-=1
        if item.goingY < 0:
            item.y+=item.goingY
            item.goingY+=1                   
def write_text(text, x, y, size, align, alpha):
    if align:
        x-=len(text)*size*0.4
    for i in range(len(text)):
        if text[i].lower() == ":":
            letterSprites[38].set_alpha(alpha)
            window.blit(pygame.transform.scale(letterSprites[38], (size, size)), (x+i*size*0.8, y))
        elif text[i].lower() == "/":
            letterSprites[43].set_alpha(alpha)
            window.blit(pygame.transform.scale(letterSprites[43], (size, size)), (x+i*size*0.8, y))
        elif text[i].lower() != " ":
            for j in range(len(letters)):
                if text[i].lower() == letters[j]:
                    letterIndex = j
            letterSprites[letterIndex].set_alpha(alpha)
            window.blit(pygame.transform.scale(letterSprites[letterIndex], (size, size)), (x+i*size*0.8, y))
def repos_camera():
    camera.x-=((camera.x-game_settings.displayHalfWidth)-(player.x*-1))/camera.smoothness
    camera.y-=((camera.y-game_settings.displayHalfHeight)-(player.y*-1))/camera.smoothness
    
    camera.x=int(camera.x*2)/2
    camera.y=int(camera.y*2)/2

    if camera.x < worldWidth*tileSize/-2+game_settings.displayWidth:
        camera.x = worldWidth*tileSize/-2+game_settings.displayWidth
    if camera.x > worldWidth*tileSize/2:
        camera.x = worldWidth*tileSize/2
        
    if camera.y < worldHeight*tileSize/-2+game_settings.displayHeight:
        camera.y = worldHeight*tileSize/-2+game_settings.displayHeight
    if camera.y > worldHeight*tileSize/2:
        camera.y = worldHeight*tileSize/2
def rearrange_obj(objs):
    objs = []
    if not game_settings.GODMODE:
        objs.append(player)
        
    
    curTile = int((camera.y*-1+worldHAccHeight)/tileSize)+int((camera.x*-1+worldHAccWidth)/tileSize)*worldHeight
    for i in range(displayTWidth):
        for k in range(displayTHeight):
            if curTile >= len(tiles):
                break
            if tiles[curTile].building != "":
                objs.append(tiles[curTile])
            curTile += 1
        if curTile >= len(tiles):
            break
        curTile += worldHeight-displayTHeight
                        
    for drops in droppedItems:
        objs.append(drops)
        objs[-1].y+=16
        
    for obj in objs:
        if obj.i == "tile":
            if obj.building == "tree" or obj.building == "grass" or obj.building == "hay":
                obj.y+=tileSize
                
    sortedList = sorted(objs, key=lambda objs: objs.y)
    
    if game_settings.GODMODE:
        sortedList.append(player)
        
    for obj in objs:
        if obj.i == "tile":
            if obj.building == "tree" or obj.building == "grass" or obj.building == "hay":
                obj.y-=tileSize
    for obj in objs:
        if obj.i == "item":
            obj.y-=16

    return sortedList
def item_pickup():
    if globalKeys.key[pygame.K_SPACE]:
        pickedUp = False
        space = False
        if player.curWeight <= player.maxWeight or game_settings.GODMODE:
            for i in range(len(player.inventory)):
                if player.inventory[i].item == "":
                    space = True
                    break
        if space:
            for i in range(len(droppedItems)):
                if (droppedItems[i].x-player.x)**2+(droppedItems[i].y-player.y)**2 < player.reach**2:
                    droppedItems[i].x -= (droppedItems[i].x-player.x)/100
                    droppedItems[i].y -= (droppedItems[i].y-player.y)/100
                if (droppedItems[i].x-player.x)**2+(droppedItems[i].y-player.y)**2 < (player.reach/2)**2:
                    droppedItems[i].x -= (droppedItems[i].x-player.x)/10
                    droppedItems[i].y -= (droppedItems[i].y-player.y)/10

            delIndicies = []
            for i in range(len(droppedItems)):
                pickedUp = False
                if (droppedItems[i].x-player.x)**2+(droppedItems[i].y-player.y)**2 < 300:
                    for j in range(len(player.inventory)):
                        if player.inventory[j].amount < game_settings.maxStack and player.inventory[j].item == droppedItems[i].item and (player.inventory[j].tag == "resource" or player.inventory[j].item == "stone"):
                            player.inventory[j].amount +=1
                            pickedUp = True
                            break
                    if not pickedUp:
                        for j in range(len(player.inventory)):
                            if player.inventory[j].item == "":
                                tool = False
                                for k in range(len(itemDamages)):
                                    if droppedItems[i].item == itemDamages[k][0]:
                                        tool = True
                                        break
                                if tool or droppedItems[i].item == "wood hammer":
                                    breaking = False
                                    for k in range(9):
                                        if (player.hotbar[k].item == "" and k == 0) or (player.hotbar[k].item == "" and droppedItems[i].item != "stone"):
                                            player.hotbar[k].tag = "tool"
                                            player.hotbar[k].amount +=1
                                            player.hotbar[k].item = droppedItems[i].item
                                            player.hotbar[k].weight = weightsdict[droppedItems[i].item]
                                            player.hotbar[k].enhancements = droppedItems[i].enhancements
                                            player.hotbar[k].durability = droppedItems[i].durability
                                            player.hotbar[k].sprite = pygame.transform.scale(pygame.image.load("sprites/items/"+droppedItems[i].item+".png"), (64, 64))
                                            pickedUp = True
                                            breaking = True
                                            break
                                    if breaking:
                                        break
                                        
                                else:
                                    player.inventory[j].tag = "resource"
                                player.inventory[j].amount +=1
                                player.inventory[j].item = droppedItems[i].item
                                player.inventory[j].weight = weightsdict[droppedItems[i].item]
                                player.inventory[j].enhancements = droppedItems[i].enhancements
                                player.inventory[j].durability = droppedItems[i].durability
                                player.inventory[j].sprite = pygame.transform.scale(pygame.image.load("sprites/items/"+droppedItems[i].item+".png"), (64, 64))
                                pickedUp = True
                                break
                    update_inventory_total()
                if pickedUp:
                    delIndicies.append(i)

            delIndicies.sort(reverse=True)
            for i in range(len(delIndicies)):
                del droppedItems[delIndicies[i]]          
def kill_dropped_items():
    global droppedItems
    while len(droppedItems) > game_settings.maxItemsOnFloor:
        del droppedItems[0]
    for i in range(len(droppedItems)-1):
        droppedItems[i].lifetime += 1
        if droppedItems[i].lifetime > game_settings.itemDeathClock:
            del droppedItems[i]
            break
    if len(droppedItems) == 1:
        droppedItems[0].lifetime += 1
        if droppedItems[0].lifetime > game_settings.itemDeathClock:
            droppedItems = []
def weight_cal():
    player.curWeight = 0
    for item in player.inventory:
        player.curWeight += item.weight*item.amount
    for item in player.hotbar:
        if item.item == "stone":
            player.curWeight += item.weight*item.amount
        else:
            player.curWeight += item.weight
def customise_world():
    global biomeSize, worldHeight, worldWidth
    if 100 < mouse.y < 150 and mouse.x < 700:
        write_text("biome size  :"+str(biomeSize), 50, 100, 50, False, 255)
    else:
        write_text("biome size  :"+str(biomeSize), 50, 100, 50, False, 150)
    if 175 < mouse.y < 225 and mouse.x < 700:
        write_text("world height:"+str(worldHeight), 50, 175, 50, False, 255)
    else:
        write_text("world height:"+str(worldHeight), 50, 175, 50, False, 150)
    if 250 < mouse.y < 325 and mouse.x < 700:
        write_text("world width :"+str(worldWidth), 50, 250, 50, False, 255)
    else:
        write_text("world width :"+str(worldWidth), 50, 250, 50, False, 150)
        
    if 400 < mouse.y < 500 and mouse.x < 1200:
        write_text("generate world", 50, 400, 100, False, 255)
        if mouse.click:
            generate_world()
    else:
        write_text("generate world", 50, 400, 100, False, 150)
        
    if 550 < mouse.y < 700 and mouse.x < 700:
        write_text("play", 50, 550, 150, False, 255)
        if mouse.click:
            wave_sprites(tiles)
            start_game()
            
    else:
        write_text("play", 50, 550, 150, False, 150)
    if tiles != []:
        display_preview_world()
def start_game():
    game_settings.menu = "game"
    global tiles, player, camera
    player = PLAYER(tiles)
    for i in range(4*5):
        player.inventory.append(INVENTORY_ITEM())
    for i in range(9):
        player.hotbar.append(INVENTORY_ITEM())
    camera = CAMERA()
def update_inventory_total():
    player.inventoryTotalItem = []
    player.inventoryTotalAmount = []
    for i in range(len(player.inventory)):
        if player.inventory[i].item != "":
            found = False
            for j in range(len(player.inventoryTotalItem)):
                if player.inventory[i].item == player.inventoryTotalItem[j]:
                    player.inventoryTotalAmount[j] += player.inventory[i].amount
                    found = True
                    break
            
            if not found:
                player.inventoryTotalItem.append(player.inventory[i].item)
                player.inventoryTotalAmount.append(player.inventory[i].amount)                
def temperature_cal():
    player.temperature = max(-50, min(50, player.temperature))
    if -20 < player.temperature < 20:
        player.temperature_damage_cd += 1
    else: 
        player.temperature_damage_cd -= 1
    if player.temperature_damage_cd <= 0:
        player.temperature_damage_cd = 5*60
        player.health -= 1
def smooth_camera():
    if camera.smoothness > camera.IGSmoothness:
        camera.smoothness*=0.9
    else:
        camera.smoothness = camera.IGSmoothness
def decrease_held_item_durability():
    if player.hotbar[0].item != "":
        for enhancement in player.hotbar[0].enhancements:
            if enhancement != "durability":
                player.hotbar[0].durability-=0.2
        player.hotbar[0].durability-=0.2
        player.hotbar[0].durability = round(player.hotbar[0].durability, len(str(int(player.hotbar[0].durability)+1)))

        if player.hotbar[0].durability <= 0:
            player.hotbar[0] = INVENTORY_ITEM()
            create_particles(mouse.x, mouse.y, 255, 0, 0, 250,  5)

# TILES

def wave_rechance():
    for tile in tiles:
        if tileSize*-1 < tile.x+camera.x < game_settings.displayWidth+tileSize and tileSize*-1 < tile.y+camera.y < game_settings.displayHeight+tileSize*1:
            if tile.tile == "water" or tile.tile == "shore":
                if tile.waveSprite !=["", "", ""]:
                    tile.waveChance = random.randint(0, 1)
def display_tiles(animation):
    curTile = int((camera.y*-1+worldHAccHeight)/tileSize)+int((camera.x*-1+worldHAccWidth)/tileSize)*worldHeight
    for i in range(displayTWidth):
        for k in range(displayTHeight):
            if curTile >= len(tiles):
                return
            if tiles[curTile].covered < 255:
                if tiles[curTile].building != "floor":
                    window.blit(tiles[curTile].sprite, (tiles[curTile].x+camera.x, tiles[curTile].y+camera.y))
                    if tiles[curTile].tile == "water" or tiles[curTile].tile == "shore":
                        if tiles[curTile].waterCons != "":
                            if tiles[curTile].waveSprite[animation] != "":
                                if tiles[curTile].waveChance:
                                    window.blit(tiles[curTile].waveSprite[animation], (tiles[curTile].x+camera.x, tiles[curTile].y+camera.y))
            
            curTile += 1
        curTile += worldHeight-displayTHeight
def display_covered_tiles():
    curTile = int((camera.y*-1+worldHAccHeight)/tileSize)+int((camera.x*-1+worldHAccWidth)/tileSize)*worldHeight
    for i in range(displayTWidth):
        for k in range(displayTHeight):
            if curTile >= worldSize:
                return
            if tiles[curTile].covered > 0:
                coveredTile.set_alpha(tiles[curTile].covered)
                window.blit(coveredTile, (tiles[curTile].x+camera.x, tiles[curTile].y+camera.y))
                
            curTile += 1
        curTile += worldHeight-displayTHeight
def uncover_tiles():
    curTile = int((player.y+worldHAccHeight-tileSize*(game_settings.viewDistance/2))/tileSize)+int((player.x+worldHAccWidth-tileSize*(game_settings.viewDistance/2))/tileSize)*worldHeight
    for i in range(game_settings.viewDistance):
        for j in range(game_settings.viewDistance):
            alphaMax = abs(i-game_settings.viewDistance/2)**2+abs(j-game_settings.viewDistance/2)**2
            alphaMax*=255/game_settings.viewDistance
                
            if (0 <= curTile < worldSize) and abs(player.y-tiles[curTile].y) <= game_settings.viewDistance*tileSize:
                if tiles[curTile].covered > alphaMax:
                    tiles[curTile].covered -= 30
                    if tiles[curTile].covered < 100:
                        tiles[curTile].covered = 0
            curTile += 1
            if curTile > worldSize:
                return
        curTile += worldHeight-game_settings.viewDistance
        if curTile > worldSize:
            return
def display_obj():
    for obj in objects:
        if tileSize*-2 < obj.x+camera.x < game_settings.displayWidth+tileSize and tileSize*-2 < obj.y+camera.y < game_settings.displayHeight+tileSize*2:
            if obj.i == "tile":
                if obj.building == "tree":
                    if obj.x < player.x < obj.x+tileSize and obj.y-obj.buildSprite[int(obj.health/10)].get_height()+tileSize*2 < player.y < obj.y:
                        obj.buildSprite[int(obj.health/10)].set_alpha(150)
                    else:
                        obj.buildSprite[int(obj.health/10)].set_alpha(255)
                elif obj.building == "hay":
                    if obj.x < player.x < obj.x+tileSize and obj.y-obj.buildSprite.get_height()+tileSize*2 < player.y < obj.y+tileSize:
                        obj.buildSprite.set_alpha(150)
                    else:
                        obj.buildSprite.set_alpha(255)
                else:
                    if obj.x < player.x < obj.x+tileSize and obj.y-obj.buildSprite.get_height()+tileSize < player.y < obj.y:
                        obj.buildSprite.set_alpha(150)
                    else:
                        obj.buildSprite.set_alpha(255)
                            
                if obj.building == "tree":
                    window.blit(obj.buildSprite[int(obj.health/10)], (obj.x+camera.x-tileHalfS, obj.y+camera.y-tileSize*2))
                elif obj.building == "hay":
                    window.blit(obj.buildSprite, (obj.x+camera.x, obj.y+camera.y-tileSize))
                elif obj.building == "wall" or obj.building == "door":
                    window.blit(obj.buildSprite, (obj.x+camera.x, obj.y+camera.y-tileHalfS))
                elif obj.building != "":
                    window.blit(obj.buildSprite, (obj.x+camera.x, obj.y+camera.y))
            if obj.i == "player":
                window.blit(obj.sprite, (obj.x+camera.x-obj.width/2, obj.y+camera.y-obj.height))
                for i in range(2):
                    temp = pygame.transform.rotate(arm[i].sprite, arm[i].angle)
                    window.blit(temp, (arm[i].x+camera.x-temp.get_width()/2, arm[i].y+camera.y-temp.get_height()/2))
                if player.hotbar[0].item != "" and arm[0].holdingItemSprite != "" and arm[0].holdingItemSprite != "":
                    temp = arm[0].holdingItemSprite
                    
                    if mouse.x > player.x+camera.x:
                        angle = arm[0].angle-45
                        temp = pygame.transform.flip(temp, True, True)
                    else:
                        angle = arm[0].angle-135
                        temp = pygame.transform.flip(temp, True, False)
                            
                    temp = pygame.transform.rotate(temp, angle)
                    window.blit(temp, (arm[0].ankX+camera.x-temp.get_width()/2-(math.cos(math.radians(angle))*arm[0].height), arm[0].ankY+camera.y-temp.get_height()/2+(math.sin(math.radians(angle))*arm[0].height)))
                    
            if obj.i == "item":
                window.blit(obj.sprite, (obj.x+camera.x-obj.size/2, obj.y+camera.y-obj.size/2))
def display_selected_tile():
    window.blit(closeTile, (tiles[mouse.tile].x+camera.x, tiles[mouse.tile].y+camera.y))
    # eventually i'll expand this out to trees and stuff
def update_tile_darkness():
    curTile = int((camera.y*-1+worldHAccHeight)/tileSize)+int((camera.x*-1+worldHAccWidth)/tileSize)*worldHeight
    for i in range(displayTWidth):
        for k in range(displayTHeight):
            tiles[curTile].darkness = (game_settings.time-game_settings.darkeningtime)/game_settings.timetransitiontime*255
            if game_settings.time >= game_settings.timetransitiontime+game_settings.darkeningtime+game_settings.nightlength:
                tiles[curTile].darkness = 255-(game_settings.time-(game_settings.timetransitiontime+game_settings.darkeningtime+game_settings.nightlength))/game_settings.timetransitiontime*255
            if curTile < worldSize-1:
                curTile += 1
        if curTile < worldSize-(worldHeight):
            curTile += worldHeight-displayTHeight
def display_darkness():
    sprite = pygame.Surface((tileSize, tileSize))
    sprite.fill(BLACK)
    curTile = int((camera.y*-1+worldHAccHeight)/tileSize)+int((camera.x*-1+worldHAccWidth)/tileSize)*worldHeight
    for i in range(displayTWidth):
        for k in range(displayTHeight):
            if game_settings.time >= game_settings.timetransitiontime:
                sprite.set_alpha(tiles[curTile].darkness)
                window.blit(sprite, (tiles[curTile].x+camera.x, tiles[curTile].y+camera.y))
            if curTile < worldSize-1:
                curTile += 1
        if curTile < worldSize-(worldHeight):
            curTile += worldHeight-displayTHeight
def generate_structure(structure, x, y, ruinedness):
    global tiles
    file_lines = open("structures/"+structure+".txt", "r").readlines()
    building_dictionary = []
    for i in range(len(file_lines)-1):
        file_lines[i] = file_lines[i].replace("\n", "")
        if file_lines[i] == "~":
            blueprint_start_line = i+1
            break
        building_dictionary.append([file_lines[i].split("=")[0].strip(" "), file_lines[i].split("=")[1].strip(" ").strip("\n")])
    
    y -= blueprint_start_line+int(abs(blueprint_start_line-len(file_lines))/2)
    x -= int(len(file_lines[blueprint_start_line])/2)
    for i in range(blueprint_start_line, len(file_lines)):
        file_lines[i] = file_lines[i].replace("\n", "")
        for j in range(len(file_lines[i])):
            if file_lines[i][j] != ".":
                what_building = ""
                # check the dictionary for what correlates with it
                for k in range(len(building_dictionary)):
                    if building_dictionary[k][0] == file_lines[i][j]:
                        what_building = building_dictionary[k][1].split(" ")
                        break
                
                # don't place 100% tiles to give a ruined effect
                if random.randint(1, 100) > ruinedness:
                    place_building((x+j)*worldHeight+(y+i), what_building[0], what_building[1])
def generate_world():
    window.fill(BLACK)
    global tiles, tileAmount
    write_text("generating world...", game_settings.displayHalfWidth, game_settings.displayHalfHeight-125, 100, True, 255)
    write_text("this might take a while", game_settings.displayHalfWidth, game_settings.displayHalfHeight, 100, True, 255)
    pygame.display.update()
    noise1 = PerlinNoise(octaves=int(worldWidth/20)+2, seed=random.randint(1,1000))
    tiles = []
    for x in range(worldWidth):
        for y in range(worldHeight):
            if y > worldHeight-20:
                tiles.append(TILE(x-worldHalfW, y-worldHalfH, (noise1([x/worldWidth, y/worldWidth])*100-abs((worldHeight-20)-y)*3), (noise1([(x+100)/worldWidth, y/worldWidth])*100) ))
            else:
                if y < biomeSize:
                    tiles.append(TILE(x-worldHalfW, y-worldHalfH, (noise1([x/worldWidth, y/worldWidth])*100)+abs(y-biomeSize)*2, (noise1([(x+100)/worldWidth, y/worldWidth])*100) ))
                else:
                    tiles.append(TILE(x-worldHalfW, y-worldHalfH, (noise1([x/worldWidth, y/worldWidth])*100), (noise1([(x+100)/worldWidth, y/worldWidth])*100) ))
    tileAmount = len(tiles)
    tiles = wave_sprites(tiles)
    post_processing_generation()
def post_processing_generation():
    global tiles
    for i in range(worldSize-1):
        if tiles[i].tile == "grass":
            needForProcessing = False
            indicies = [i-1, i+1, i-worldHeight, i+worldHeight]
            for index in indicies:
                index = min(worldSize-1, index)
                if tiles[index].tile == "water" or tiles[index].tile == "shore":
                    tiles[i].tile = "sand"
                    destroy_building(i)
            
            if game_settings.borderedTextures:
                tiles[i].sprite = pygame.transform.scale(pygame.image.load("sprites/bordered blocks/"+tiles[i].tile+"/"+str(random.randint(1,3))+".png").convert_alpha(), (tileSize, tileSize))
            else:
                tiles[i].sprite = pygame.transform.scale(pygame.image.load("sprites/unbordered blocks/"+tiles[i].tile+"/"+str(random.randint(1,3))+".png").convert_alpha(), (tileSize, tileSize))

# DISPLAY MISC

def display_inventory():
    invX = game_settings.displayHalfWidth-inventoryImg.get_width()/2
    invY = game_settings.displayHalfHeight-inventoryImg.get_height()/2-100
    window.blit(inventoryImg, (invX, invY))
    
    for i in range(len(player.inventory)):
        if player.inventory[i].sprite != "":
            window.blit(player.inventory[i].sprite, (16+invX+(i%5)*108, 16+invY+int(i/5)*108))
        if i == mouse.selectedSlot:
            window.blit(mouseSlotImg, (invX+(i%5)*108-6, invY+int(i/5)*108-6))
        if i == player.selectedSlot:
            window.blit(selectedSlotImg, (invX+(i%5)*108-6, invY+int(i/5)*108-6))
        if player.inventory[i].tag == "tool" and player.inventory[i].item != "stone":
            write_text(str(player.inventory[i].durability)+"%", 16+invX+(i%5)*108, 16+invY+int(i/5)*108, 20, False, 255)
        elif player.inventory[i].amount > 0:
            write_text(str(player.inventory[i].amount), 16+invX+(i%5)*108, 16+invY+int(i/5)*108, 20, False, 255)
        for j in range(len(player.inventory[i].enhancements)):
            window.blit(enhancementSprites[player.inventory[i].enhancements[j]], (16+invX+(i%5)*108+j*20, 16+invY+int(i/5)*108+45))
def create_particles(x, y, r, g, b, amount, deathspeed):
    for i in range(amount):
        alphaChange = 0 #random.randint(-5, 5)
        r += alphaChange
        g += alphaChange
        b += alphaChange

        r = min(255, max(0, r+alphaChange))
        g = min(255, max(0, g+alphaChange))
        b = min(255, max(0, b+alphaChange))
        
        particles.append(PARTICLE(x, y, (r, g, b), deathspeed))
def display_particles():
    for particle in particles:
        particle.x += particle.goingX
        particle.y += particle.goingY
        window.blit(particle.sprite, (particle.x, particle.y))
        particle.sprite = pygame.Surface((10,10))
        particle.sprite.set_alpha(particle.alpha)
        particle.sprite.fill(particle.col)
        particle.alpha -= particle.deathspeed
    delIndicies = []
    for i in range(len(particles)):
        if particles[i].alpha <= 0:
            delIndicies.append(i)
    delIndicies.sort(reverse=True)
    for i in range(len(delIndicies)):
        del particles[delIndicies[i]]
def display_crafting():
    # animation
    if crafting_settings.craftingAnimation:
       crafting_settings.craftingAnimation-=1 
    if game_settings.crafting == "":
        if crafting_settings.invX < crafting_settings.ankInvX:
            crafting_settings.invX+=50
    elif crafting_settings.invX > crafting_settings.ankInvX-600:
        crafting_settings.invX-=50
    crafting_settings.invY = game_settings.displayHalfHeight-inventoryImg.get_height()/2-100
    
    window.blit(inventoryImg, (crafting_settings.invX, crafting_settings.invY))
    window.blit(craftingSelection, (crafting_settings.invX-150, crafting_settings.invY))
    if mouse.click:
        if crafting_settings.invX-150 < mouse.x < crafting_settings.invX-150+craftingSelection.get_width() and crafting_settings.invY < mouse.y < crafting_settings.invY+craftingSelection.get_height():
            game_settings.craftingMenu = craftingSelectsDict[min(4, int(((mouse.y-crafting_settings.invY)/(crafting_settings.invY+craftingSelection.get_height()))*5)+1)]
            crafting_settings.crafting = ""
    selIndex = craftingSelectsDict[game_settings.craftingMenu]
           
    if mouse.click:
        if not (crafting_settings.invX-150 < mouse.x < crafting_settings.invX-150+craftingSelection.get_width() and crafting_settings.invY < mouse.y < crafting_settings.invY+craftingSelection.get_height()):
            relX = crafting_settings.invX-game_settings.displayHalfWidth-inventoryImg.get_width()/2+mouse.x
            relY = mouse.y-crafting_settings.invY
            if crafting_settings.invX < mouse.x < crafting_settings.invX+inventoryImg.get_width() and game_settings.displayHalfHeight-inventoryImg.get_height()/2-100 < mouse.y < game_settings.displayHalfHeight+inventoryImg.get_height()/2-100:
                ind = int((mouse.x-crafting_settings.invX)/108)+int((mouse.y-crafting_settings.invY)/108)*5
                if ind < len(crafts[selIndex]):
                    game_settings.crafting = crafts[selIndex][ind].item.strip()
                    crafting_settings.craftIndex = ind
                elif not (108 < relX < 395 and 312 < relY < 406):
                    game_settings.crafting = ""
            
            elif not (108 < relX < 395 and 312 < relY < 406):
                game_settings.crafting = ""
        else:
            game_settings.crafting = ""
            
    pygame.draw.rect(window, (107, 107, 107), (crafting_settings.invX+inventoryImg.get_width()+10, crafting_settings.invY, game_settings.displayHalfWidth-crafting_settings.invX-200+110, inventoryImg.get_height()))
    pygame.draw.rect(window, (158, 158, 158), (crafting_settings.invX+inventoryImg.get_width()+15, crafting_settings.invY+5, game_settings.displayHalfWidth-crafting_settings.invX-210+110, inventoryImg.get_height()-10))
    window.blit(selectedCrafting, (crafting_settings.invX-150-6, crafting_settings.invY+selIndex*108-6))
    
    for i in range(len(crafts[selIndex])):
        window.blit(crafts[selIndex][i].sprite, (16+crafting_settings.invX+(i%5)*108, 16+crafting_settings.invY+int(i/5)*108))
        if game_settings.crafting == crafts[selIndex][i].item:

            window.blit(crafts[selIndex][i].bigSprite, (crafting_settings.invX+inventoryImg.get_width()+20, crafting_settings.invY))
            write_text(crafts[selIndex][i].item, crafting_settings.invX+inventoryImg.get_width()+crafts[selIndex][i].bigSprite.get_width()+20, crafting_settings.invY+50, 50-len(crafts[selIndex][i].item)*1.8, False, 255)
            for j in range(len(crafts[selIndex][i].itemIn)):
                window.blit(crafts[selIndex][i].itemInSprite[j], (crafting_settings.invX+inventoryImg.get_width()+10+(j%4)*120, crafting_settings.invY+150+int(j/4)*75))
                write_text(str(crafts[selIndex][i].amountIn[j]), crafting_settings.invX+inventoryImg.get_width()+26+(j%4)*120, crafting_settings.invY+140+int(j/4)*75, 30, True, 255)
                for k in range(len(player.inventoryTotalItem)):
                    if player.inventoryTotalItem[k] == crafts[selIndex][i].itemIn[j]:
                        if player.inventoryTotalAmount[k] >= crafts[selIndex][i].amountIn[j]:
                            # display tick
                            window.blit(tickImg, (crafting_settings.invX+inventoryImg.get_width()+(j%4)*120, crafting_settings.invY+220+int(j/4)*75))
                        else:
                            # display how much more you need
                            window.blit(crafts[selIndex][i].itemInSprite[j], (crafting_settings.invX+inventoryImg.get_width()+(j%4)*120, crafting_settings.invY+220+int(j/4)*75))
                            window.blit(crossImg, (crafting_settings.invX+inventoryImg.get_width()+(j%4)*120, crafting_settings.invY+220+int(j/4)*75))
                            write_text(str(crafts[selIndex][i].amountIn[j]-player.inventoryTotalAmount[k]), crafting_settings.invX+inventoryImg.get_width()+(j%4)*120, crafting_settings.invY+220+int(j/4)*75, 30, False, 255)
                        break
                    elif k+1 == len(player.inventoryTotalItem):
                        # display how much you need
                        window.blit(crafts[selIndex][i].itemInSprite[j], (crafting_settings.invX+inventoryImg.get_width()+20+(j%4)*120, crafting_settings.invY+220+int(j/4)*75))
                        window.blit(crossImg, (crafting_settings.invX+inventoryImg.get_width()+(j%4)*120, crafting_settings.invY+220+int(j/4)*75))
                        write_text(str(crafts[selIndex][i].amountIn[j]), crafting_settings.invX+inventoryImg.get_width()-50+(j%4)*120, crafting_settings.invY+220+int(j/4)*75, 30, False, 255)
                                    
            window.blit(craftButton, (crafting_settings.invX+inventoryImg.get_width()+20, crafting_settings.invY+310))
            write_text("craft", crafting_settings.invX+inventoryImg.get_width()+craftButton.get_width()/2, crafting_settings.invY+340, 40-crafting_settings.craftingAnimation, True, 255)
        
    if mouse.click and selIndex != "" and crafting_settings.craftIndex != "" and not (crafting_settings.invX-150 < mouse.x < crafting_settings.invX-150+craftingSelection.get_width() and crafting_settings.invY < mouse.y < crafting_settings.invY+craftingSelection.get_height()):
        relX = crafting_settings.invX-game_settings.displayHalfWidth-inventoryImg.get_width()/2+mouse.x
        relY = mouse.y-crafting_settings.invY
        if 108 < relX < 395 and 312 < relY < 406:
            RN = crafts[selIndex][crafting_settings.craftIndex].itemIn
            AN = crafts[selIndex][crafting_settings.craftIndex].amountIn
            craft(crafts[selIndex][crafting_settings.craftIndex], RN, AN)    
def display_hotbar():
    if game_settings.menu == "inventory":
        ypos = game_settings.displayHeight-150
    else:
        ypos = game_settings.displayHeight-50
        
    if (mouse.x-(game_settings.displayHalfWidth))**2+(mouse.y-(ypos))**2 > 150**2 or game_settings.menu == "inventory":
        window.blit(hotbarImgTR, (game_settings.displayHalfWidth-150, ypos-150))
    else:
        window.blit(hotbarImg, (game_settings.displayHalfWidth-150, ypos-150))
        
    if game_settings.menu == "inventory":
        if mouse.selectedHBSlot != "":
            if mouse.selectedHBSlot:
                slot = mouse.selectedHBSlot-player.HBcycle
                if slot < 1:
                    slot+=8
            else:
                slot = 0
            window.blit(hotbarMouseImg[slot], (game_settings.displayHalfWidth-125, ypos-125))
        if player.selectedHBSlot != "" and mouse.offInvBeat:
            if player.selectedHBSlot:
                slot = player.selectedHBSlot-player.HBcycle
                if slot < 1:
                    slot+=8
            else:
                slot = 0
            window.blit(hotbarSelectedImg[slot], (game_settings.displayHalfWidth-125, ypos-125))
        
    for i in range(len(player.hotbar)):
        if i:
            x = game_settings.displayHalfWidth-25/2+(math.cos(math.radians(i*45))*130)
            y = ypos-25/2-(math.sin(math.radians(i*45))*130)
            text = i+player.HBcycle
            if text > 8:
                text-=8
            write_text(str((text)), x, y, 25, False, 255)
            
    for i in range(len(player.hotbar)):
        if player.hotbar[i].sprite != "":
            if i == 0:
                window.blit(player.hotbar[i].sprite, (game_settings.displayHalfWidth-32, ypos-32))
                if player.hotbar[i].durability:
                    write_text(str(player.hotbar[i].durability)+"%", game_settings.displayHalfWidth-32, ypos-32, 25, False, 255)
                for j in range(len(player.hotbar[i].enhancements)):
                    window.blit(enhancementSprites[player.hotbar[i].enhancements[j]], (game_settings.displayHalfWidth+3-40+j*20, ypos+30))
            else:
                x = game_settings.displayHalfWidth-32+(math.cos(math.radians((i-player.HBcycle)*45))*100)
                y = ypos-32-(math.sin(math.radians((i-player.HBcycle)*45))*100)
                
                window.blit(player.hotbar[i].sprite, (x, y))
                if player.hotbar[i].durability:
                    write_text(str(player.hotbar[i].durability)+"%", x, y+15, 25, False, 255)
                for j in range(len(player.hotbar[i].enhancements)):
                    window.blit(enhancementSprites[player.hotbar[i].enhancements[j]], (x+j*20, y+40)) 
def display_preview_world():
    for x in range(worldWidth):
        for y in range(worldHeight):
            index = x*worldHeight+y
            if index < len(tiles):  
                pygame.draw.rect(window, tiles[index].minimapColour, (1200+x*3, y*3, 3, 3))
def display_minimap():
    scale = 2
    if mouse.x > game_settings.displayWidth-worldWidth*scale-10-scale and mouse.y < game_settings.displayHeight+10+scale:
        scale = 5
    pygame.draw.rect(window, (BLACK), (game_settings.displayWidth-10-(worldWidth+1)*scale, 10-scale, worldWidth*scale+scale*2, worldHeight*scale+scale*2))
    pygame.draw.rect(window, (255, 255, 255), (game_settings.displayWidth-10-(worldWidth)*scale, 10, worldWidth*scale, worldHeight*scale))
    for x in range(worldWidth):
        for y in range(worldHeight):
            index = x*worldHeight+y
            if index < len(tiles) and tiles[index].covered != 255:
                if tiles[index].building == "":
                    pygame.draw.rect(window, tiles[index].tileMinimapColour, (game_settings.displayWidth-10-worldWidth*scale+x*scale, 10+y*scale, scale, scale))
                else:
                    pygame.draw.rect(window, tiles[index].buildingMinimapColour, (game_settings.displayWidth-10-worldWidth*scale+x*scale, 10+y*scale, scale, scale))
    #pygame.draw.rect(window, (255, 0, 0), (game_settings.displayWidth-worldWidth-10+player.x, 10+player.y, 3, 3))
def display_building_panel():
    displayX = building_settings.x
    displayY = building_settings.y
    window.blit(buildingPanel, (displayX-buildingPanel.get_width()/2, displayY-buildingPanel.get_height()/2))
    building_settings.buildSelected = []
    if displayY-50 > mouse.y:
        building_settings.buildSelected.append("wood")
    elif displayY+50 > mouse.y:
        building_settings.buildSelected.append("stone")
    else:
        building_settings.buildSelected.append("hay")
        
    if displayX-50 > mouse.x:
        building_settings.buildSelected.append("floor")
    elif displayX+50 > mouse.x:
        building_settings.buildSelected.append("wall")
    else:
        building_settings.buildSelected.append("door")  
def display_ghost_building(f):
    if building_settings.sprite != "" and player.inReach:
        sprite = building_settings.sprite
        sprite.set_alpha(180+abs(f-30))
        if building_settings.buildSelected[1] == "floor":
            window.blit(building_settings.sprite, (tiles[mouse.tile].x+camera.x, tiles[mouse.tile].y+camera.y))
        else:
            window.blit(building_settings.sprite, (tiles[mouse.tile].x+camera.x, tiles[mouse.tile].y+camera.y-tileHalfS))
def display_player_gui(f):
    if game_settings.menu != "crafting":
        # warnings
        intensity = abs(f-30)*10
        if intensity > 255:
            intensity = 255
        # stamina
        if player.stamina <= 0:
            pygame.draw.rect(window, (intensity, intensity/4, 0), (50, game_settings.displayHeight-350, 35, 300))
        else:
            pygame.draw.rect(window, BLACK, (50, game_settings.displayHeight-350, 35, 300))
        pygame.draw.rect(window, (29, 227, 7), (55, game_settings.displayHeight-55-(player.stamina/100)*290, 30, (player.stamina/100)*290))
        # energy
        if player.energy <= 0:
            pygame.draw.rect(window, (intensity, intensity/4, 0), (85, game_settings.displayHeight-350, 35, 300))
        else:
            pygame.draw.rect(window, BLACK, (85, game_settings.displayHeight-350, 35, 300))
        pygame.draw.rect(window, (227, 209, 16), (85, game_settings.displayHeight-55-(player.energy/100)*290, 30, (player.energy/100)*290))
        #hydration
        if player.hydration <= 0:
            pygame.draw.rect(window, (intensity, intensity/4, 0), (150, game_settings.displayHeight-350, 40, 300))
        else:
            pygame.draw.rect(window, BLACK, (150, game_settings.displayHeight-350, 40, 300))
        pygame.draw.rect(window, (17, 185, 214), (155, game_settings.displayHeight-55-(player.hydration/500)*290, 30, (player.hydration/500)*290))
        #hunger
        if player.hunger <= 0:
            pygame.draw.rect(window, (intensity, intensity/4, 0), (220, game_settings.displayHeight-350, 40, 300))
        else:
            pygame.draw.rect(window, BLACK, (220, game_settings.displayHeight-350, 40, 300))
        pygame.draw.rect(window, (201, 114, 8), (225, game_settings.displayHeight-55-(player.hunger/500)*290, 30, (player.hunger/500)*290))

    # health
    if player.health  < player.maxHealth/3:
        pygame.draw.rect(window, (intensity, intensity/4, 0), (game_settings.displayWidth-150, game_settings.displayHeight-150, 100, 100))
    else:
        pygame.draw.rect(window, BLACK, (game_settings.displayWidth-150, game_settings.displayHeight-150, 100, 100))
    pygame.draw.rect(window, (255, 0, 50), (game_settings.displayWidth-145, game_settings.displayHeight-55-(player.health/player.maxHealth)*90, 90, (player.health/player.maxHealth)*90))
    write_text(str(player.health)+"/"+str(player.maxHealth), game_settings.displayWidth-105, game_settings.displayHeight-120, 50-len(str(player.health)+"/"+str(player.maxHealth))*5, True, 255)

    if game_settings.menu == "game":
        # temperature
        if player.temperature < -20:
            pygame.draw.polygon(window, (0, intensity*(abs(20+player.temperature)/30), intensity*((player.temperature+20)*-1)/30), ((game_settings.displayHalfWidth-420, 0), (game_settings.displayHalfWidth+420, 0), (game_settings.displayHalfWidth+365, 55), (game_settings.displayHalfWidth-365, 55)))
        elif player.temperature > 20:
            pygame.draw.polygon(window, (intensity*((intensity-20)/255), 0, 0), ((game_settings.displayHalfWidth-420, 0), (game_settings.displayHalfWidth+420, 0), (game_settings.displayHalfWidth+365, 55), (game_settings.displayHalfWidth-365, 55)))
        else:
            pygame.draw.polygon(window, BLACK, ((game_settings.displayHalfWidth-420, 0), (game_settings.displayHalfWidth+420, 0), (game_settings.displayHalfWidth+365, 55), (game_settings.displayHalfWidth-365, 55)))
        pygame.draw.polygon(window, (255, 255, 255), ((game_settings.displayHalfWidth-410, 0), (game_settings.displayHalfWidth-360, 0), (game_settings.displayHalfWidth-360, 50)))
        pygame.draw.polygon(window, (224, 25, 25), ((game_settings.displayHalfWidth+410, 0), (game_settings.displayHalfWidth+360, 0), (game_settings.displayHalfWidth+360, 50)))
        for i in range(len(cols)):
            pygame.draw.rect(window, cols[i], (game_settings.displayHalfWidth-355+55*i, 0, 50, 50))
        window.blit(temperatureIndicator, (game_settings.displayHalfWidth-25+(player.temperature)*7, 0))
    
        # weight
        pygame.draw.polygon(window, BLACK, ((game_settings.displayHalfWidth-330, 70), (game_settings.displayHalfWidth+330, 70), (game_settings.displayHalfWidth+280, 120), (game_settings.displayHalfWidth-280, 120)))
        pygame.draw.polygon(window, (255-(min(1, player.curWeight/player.maxWeight))*38, 174-(min(1, player.curWeight/player.maxWeight))*150, 132-(min(1, player.curWeight/player.maxWeight))*132), ((game_settings.displayHalfWidth-330+bord*3, 70+bord), (game_settings.displayHalfWidth+330-bord*3, 70+bord), (game_settings.displayHalfWidth+280-bord, 120-bord), (game_settings.displayHalfWidth-280+bord, 120-bord)))
        write_text("weight:"+str(int(player.curWeight*100)/100)+"/"+str(int(player.maxWeight)), game_settings.displayHalfWidth, 75, 35, True, 255)
    elif game_settings.displayWidth == 1366 and game_settings.menu == "inventory":
        pygame.draw.polygon(window, BLACK, ((game_settings.displayHalfWidth-330, 0), (game_settings.displayHalfWidth+330, 0), (game_settings.displayHalfWidth+280, 50), (game_settings.displayHalfWidth-280, 50)))
        pygame.draw.polygon(window, (255-(min(1, player.curWeight/player.maxWeight))*38, 174-(min(1, player.curWeight/player.maxWeight))*150, 132-(min(1, player.curWeight/player.maxWeight))*132), ((game_settings.displayHalfWidth-330+bord*3, bord), (game_settings.displayHalfWidth+330-bord*3, bord), (game_settings.displayHalfWidth+280-bord, 50-bord), (game_settings.displayHalfWidth-280+bord, 50-bord)))
        write_text("weight:"+str(int(player.curWeight*100)/100)+"/"+str(int(player.maxWeight)), game_settings.displayHalfWidth, 10, 35, True, 255)
    
    # F3 menu
    if game_settings.menu != "crafting":
        if game_settings.f3_toggled:
            f3_display("x ="+str(int(player.x/tileSize)), 20)
            f3_display("y ="+str(abs(int((player.y-worldHAccHeight)/tileSize))), 70)
            f3_display("time ="+str(game_settings.time), 120)
            f3_display("day ="+str(game_settings.day), 170)
            f3_display("player tile ="+str(player.tile), 220)
def f3_display(text, y):
    background = pygame.Surface((20+len(text)*20, 50))
    background.fill((50, 50, 50))
    background.set_alpha(150)
    window.blit(background, (10, y-10))
    write_text(text, 20, y, 20, False, 150)
def display_settings():
    write_text("WASD  - move", 20, 20, 30, False, 255)
    write_text("SHIFT - run", 20, 70, 30, False, 255)
    write_text("TAB   - inventory", 20, 120, 30, False, 255)
    write_text("ESC   - settings menu / escape", 20, 170, 30, False, 255)
    write_text("Q     - drop item", 20, 220, 30, False, 255)
    write_text("G     - god mode", 20, 270, 30, False, 255)
    write_text("1     - infinite fps", 20, 320, 30, False, 255)
    write_text("2     - change resolution", 20, 370, 30, False, 255)
    write_text("3     - advanced settings", 20, 420, 30, False, 255)
def handle_change_menu():
    if game_settings.menu == "inventory":
        window.blit(craftingButton, (game_settings.displayWidth-95, 20))
        if mouse.click and game_settings.displayWidth-95 < mouse.x < game_settings.displayWidth-20 and 20 < mouse.y < 95:
            game_settings.menu = "crafting"
    elif game_settings.menu == "crafting":
        window.blit(invButton, (game_settings.displayWidth-95, 20))
        if mouse.click and game_settings.displayWidth-95 < mouse.x < game_settings.displayWidth-20 and 20 < mouse.y < 95:
            game_settings.menu = "inventory"
    elif game_settings.menu == "settings":
        display_settings()
def menu_display():
    if game_settings.menu == "inventory":
        display_inventory()
    if game_settings.menu == "crafting":
        display_crafting()
    else:
        display_hotbar()      

if __name__ == "__main__":
    generate_world()
    start_game()
    frame = 0

    generate_structure("shipwreck", int((player.x+worldHAccWidth)/tileSize), int((player.y+worldHAccHeight)/tileSize), 40)
    for i in range(5):
        generate_structure("ruins", random.randint(0, worldWidth), random.randint(0, worldHeight), 40)

    droppedItems.append(DROPPED_ITEM(player.x, player.y, "wood hammer", ["reach"], random.randint(100, 150)/10))
    for i in range(random.randint(5, 10)):
        droppedItems.append(DROPPED_ITEM(player.x, player.y, "wood", [], False))
    for i in range(random.randint(1, 3)):
        droppedItems.append(DROPPED_ITEM(player.x, player.y, "stone", [], False))
    for i in range(random.randint(2, 5)):
        droppedItems.append(DROPPED_ITEM(player.x, player.y, "rope", [], False))

    while gameRunning:
        frameTime = gameClock.tick(gameFPS)
        pygame.time.delay(int(frameTime/1000))    
        keyList = pygame.key.get_pressed()
        globalKeys.key = pygame.key.get_pressed()
        mouse.click = False
        mouse.release = False
        
        if game_settings.menu == "pregame":
            set_mouse_vars()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameRunning = False
                if event.type == pygame.MOUSEWHEEL:
                    if 3000 < pregameAnimation:
                        
                        if (100 < mouse.y < 150 and mouse.x < 700) or (175 < mouse.y < 225 and mouse.x < 700):
                            if biomeSize+event.y >= 20:
                                biomeSize+=event.y*4
                            worldHeight=len(biomes)*biomeSize
                            
                        if 250 < mouse.y < 325 and mouse.x < 700:
                            if worldWidth+event.y >= 38:
                                worldWidth+=event.y
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse.click = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE and pregameAnimation > 2700:
                        pregameAnimation = 2500
                        
                    
            if pregameAnimation < 2700:
                pregameAnimation+=1+3*mouse.left+15*globalKeys.key[pygame.K_LSHIFT]
            if pregameAnimation < 2040:
                # ANIMATION
                if 255 < pregameAnimation%510:
                    alph = 255-(pregameAnimation%510-255)
                else:
                    alph = pregameAnimation%510
                pregameAnimateBackground[int(pregameAnimation/510)].set_alpha(alph)
                window.blit(pregameAnimateBackground[int(pregameAnimation/510)], (0, (game_settings.displayHeight-game_settings.displayWidth)+pregameAnimation%510))
                write_text(pregameFloatingTexts[int(pregameAnimation/510)*2], game_settings.displayHalfWidth, (pregameAnimation%510)*1.5, 50+(pregameAnimation%510)*0.1, True, alph)
                write_text(pregameFloatingTexts[int(pregameAnimation/510)*2+1], game_settings.displayHalfWidth, (pregameAnimation%510)*1.5+70+(pregameAnimation%510)*0.1, 50+(pregameAnimation%510)*0.1, True, alph)
            else:
                # MAIN PREGAME
                pregameBackground.set_alpha((pregameAnimation-2040)/2)
                window.blit(pregameBackground, (0, -175))
                if pregameAnimation < 2500:
                    write_text("bloks olc", 750+random.randint(-5, 5), (pregameAnimation-2300)/2-50+random.randint(-2, 2), 150, True, 255)
                else:
                    write_text("bloks olc", 750, 50, 150, True, 255)
                if 2500 < pregameAnimation < 2700:
                    pygame.draw.rect(window, GREY, ((pregameAnimation-2500)*-2+game_settings.displayWidth, 0, game_settings.displayWidth, game_settings.displayHeight))
                    pygame.draw.rect(window, (50, 50, 50), ((pregameAnimation-2500)*-2+game_settings.displayWidth, 175, 500, 125))
                    write_text("start", (pregameAnimation-2500)*-2+game_settings.displayWidth+200, 200, 75, True, 255)
                elif 3000+game_settings.displayHalfWidth-1 > pregameAnimation >= 2700:
                    pygame.draw.rect(window, GREY, (game_settings.displayWidth-400, 0, game_settings.displayWidth, game_settings.displayHeight))
                    if mouse.x > game_settings.displayWidth-400 and 175 < mouse.y < 300:
                        pygame.draw.rect(window, (100, 100, 100), (game_settings.displayWidth-400, 175, 500, 125))
                    else:
                        pygame.draw.rect(window, (50, 50, 50), (game_settings.displayWidth-400, 175, 500, 125))
                    write_text("start", game_settings.displayWidth-200, 200, 75, True, 255)
                if mouse.click and game_settings.displayWidth-400 < mouse.x and 125 < mouse.y < 275:
                    pregameAnimation = 3000
                    # world customisation
                if pregameAnimation >= 3000:
                    pygame.draw.rect(window, BLACK, (game_settings.displayHalfWidth-(pregameAnimation-3000), 0, (pregameAnimation-3000)*2, game_settings.displayHeight))
                    if pregameAnimation-3000 < game_settings.displayHalfWidth:
                        pregameAnimation+=30
                    else:
                        customise_world()
        
        else:
            if game_settings.menu == "game":
                frame += 1
                if frame == 60:
                    frame = 0
                    game_settings.time += 1
                    if not game_settings.GODMODE:
                        passive_deenergize()
                if game_settings.time >= game_settings.nightlength+game_settings.timetransitiontime*2+game_settings.darkeningtime:
                    game_settings.time = 0
                    game_settings.day += 1

                player.selectedSlot = ""
                mouse.slot = ""
                waveAnimation += 0.1
                if waveAnimation >= 7:
                    waveAnimation = 0
                    wave_rechance()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameRunning = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_n:
                        nuke()
                    if event.key == pygame.K_g:
                        game_settings.GODMODE = not game_settings.GODMODE
                        if game_settings.GODMODE:
                            player.speed = 5
                            player.maxSpeed = 20
                            player.decSpeed = 5
                            player.attackSpeed = 5
                            game_settings.basePlayerReach = tileSize*200
                        else:
                            player.speed = 0.5
                            player.maxSpeed = 3
                            player.decSpeed = 5
                            player.attackSpeed = 0.6
                            game_settings.basePlayerReach = tileSize*2
                        game_settings.maxStack = 16+game_settings.GODMODE*984
                        game_settings.viewDistance = 17+game_settings.GODMODE*50
                    if event.key == pygame.K_1:
                        if gameFPS == 60:
                            gameFPS = 1000
                        else:
                            gameFPS = 60
                    if event.key == pygame.K_2:
                        if game_settings.displayWidth == 1900:
                            game_settings.displayWidth = 1366
                            game_settings.displayHeight = 768
                            crafting_settings = CRAFTING_SETTINGS()
                        else:
                            game_settings.displayWidth = 1900
                            game_settings.displayHeight = 1040
                            crafting_settings = CRAFTING_SETTINGS()
                        game_settings.displayHalfHeight = game_settings.displayHeight/2
                        game_settings.displayHalfWidth = game_settings.displayWidth/2
                        displayTHeight = int(game_settings.displayHeight/tileSize)+2
                        displayTWidth = int(game_settings.displayWidth/tileSize)+2
                        
                        window = pygame.display.set_mode((game_settings.displayWidth, game_settings.displayHeight))

                    if event.key == pygame.K_3:
                        game_settings.f3_toggled = not game_settings.f3_toggled
                    if event.key == pygame.K_4:
                        pygame.init()
                        if game_settings.fullscreen == True:
                            game_settings.fullscreen = False
                            window = pygame.display.set_mode((game_settings.displayWidth, game_settings.displayHeight))
                        else:
                            game_settings.fullscreen = True
                            window = pygame.display.set_mode((game_settings.displayWidth, game_settings.displayHeight), pygame.FULLSCREEN)

                    if event.key == pygame.K_TAB:
                        if game_settings.menu == "inventory":
                            game_settings.menu = "game"
                        elif game_settings.menu == "building":
                            game_settings.menu = "game"
                        else:
                            mouse.offInvBeat = False      
                            game_settings.menu = "inventory"
                            crafting_settings = CRAFTING_SETTINGS()
                    if event.key == pygame.K_ESCAPE:
                        if game_settings.menu == "inventory" or game_settings.menu == "building" or game_settings.menu == "settings":
                            game_settings.menu = "game"
                        else:
                            mouse.offInvBeat = False              
                            game_settings.menu = "settings"
                        
                    if event.key == pygame.K_q or event.key == pygame.K_DELETE:
                        droppedItems.append(DROPPED_ITEM(tiles[player.tile].x, tiles[player.tile].y, "stone", [], False))
                        if game_settings.menu == "inventory":
                            if player.selectedSlot != "":
                                if event.key == pygame.K_q:
                                    for i in range(player.inventory[player.selectedSlot].amount):
                                        droppedItems.append(DROPPED_ITEM(tiles[player.tile].x, tiles[player.tile].y, player.inventory[player.selectedSlot].item, player.inventory[player.selectedSlot].enhancements, player.inventory[player.selectedSlot].durability))
                                
                                player.inventory[player.selectedSlot] = INVENTORY_ITEM()
                                player.selectedSlot = ""
                                mouse.offInvBeat = False
                                update_inventory_total()
                    if event.key == pygame.K_r:
                        correctedHB = player.HBcycle + 2
                        if correctedHB >= 9:
                            correctedHB -= 8
                        temp = player.hotbar[0]
                        player.hotbar[0] = player.hotbar[correctedHB]
                        player.hotbar[correctedHB] = temp
                        correctedHB -= 2

                if event.type == pygame.MOUSEWHEEL:
                    player.HBcycle += event.y
                    game_settings.time += event.x
                    if player.HBcycle < 0:
                        player.HBcycle = 7
                    if player.HBcycle > 7:
                        player.HBcycle = 0
                    mouse.click = False
                    
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse.click = True
                    if pygame.mouse.get_pressed()[2]:
                        if player.hotbar[0].item == "wood hammer":
                            building_settings.x = mouse.x
                            building_settings.y = mouse.y
                elif event.type == pygame.MOUSEBUTTONUP:
                    mouse.release = True

            set_mouse_vars()
            check_player_reach()
            if camera.smoothness != camera.IGSmoothness:
                smooth_camera()
            display_held_item()
            weight_cal()
            if game_settings.menu == "game":
                temperature_cal()
                move_player(keyList)
                if not keyList[pygame.K_LSHIFT]:
                    player_energize()
                cal_arm_angle()
                pos_arms()
                repos_camera()
                if mouse.left:
                    use_item()
                move_items()
                objects = rearrange_obj(objects)
                item_pickup()

                uncover_tiles()
                kill_dropped_items()
                update_tile_darkness()
            display_tiles(int(waveAnimation))
            display_obj()
            display_covered_tiles()
            display_darkness()
            
            if game_settings.menu == "game":
                handle_building()
            else:
                inventory_mouse()
                inventory_mouse_hotbar()
                window.blit(greyScaleImg, (0, 0))
                handle_change_menu()
            if game_settings.menu != "settings":
                display_player_gui(frame)
                menu_display()
            display_particles()
            display_minimap()
        window.blit(mouse.sprite, (mouse.x-11, mouse.y-7))
        pygame.display.update()
        window.fill(GREY)

        
    pygame.quit()
