from setup import *

#TO DO
"""
fishing
temperature / conduction / insulation
animals
day / night cycle
loads more fckn buildings like anvil, furnace, enhancement station. i want SO MANY OF THESE so let's get it right and easy yeah? cheers, future me!
saving and loading (encoding too maybe, to save storage and prevent cheating)
fishing
chunks
structures (plane crash after certain days, ruins, blah blah blah)
DIMENTIONS!!! (like underground caves, above cloud islands???)
magic like spells and whatever
"upgrading" preexisting tools and armour
zenith type crafting like in terraria
"can't go to next biome without doing / killing so and so"
effects
"""

def move_player(ks):
    playerX_1 = int((player.y+worldHAccHeight)/tileSize)+int((player.x-player.fWidth+worldHAccWidth)/tileSize)*worldHeight
    playerX_2 = int((player.y+worldHAccHeight)/tileSize)+int((player.x+player.fWidth+worldHAccWidth)/tileSize)*worldHeight
    
    sprintX = player.sprintMultiplier
    decSpeed = player.decSpeed
    if ks[pygame.K_LSHIFT]:
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
    if not stats.GODMODE:
        xCol_1 = int((player.y+worldHAccHeight)/tileSize)+int((player.x-player.fWidth+worldHAccWidth)/tileSize)*worldHeight
        xCol_2 = int((player.y+worldHAccHeight)/tileSize)+int((player.x+player.fWidth+worldHAccWidth)/tileSize)*worldHeight
        if not tiles[xCol_1].canwalk or not tiles[xCol_2].canwalk:
            player.y -= player.yAcc
            # make player.yAcc smaller until no collision but for now i make it zero because frick you
            player.yAcc = 0
    player.x += player.xAcc
    if not stats.GODMODE:
        xCol_1 = int((player.y+worldHAccHeight)/tileSize)+int((player.x-player.fWidth+worldHAccWidth)/tileSize)*worldHeight
        xCol_2 = int((player.y+worldHAccHeight)/tileSize)+int((player.x+player.fWidth+worldHAccWidth)/tileSize)*worldHeight
        if not (worldHAccWidth*-1+player.halfWidth < player.x < worldHAccWidth-player.halfWidth):
            player.x -= player.xAcc
            # make player.yAcc smaller until no collision but for now i make it zero because frick you
            player.xAcc = 0
        else:
            if not tiles[xCol_1].canwalk or not tiles[xCol_2].canwalk:
                player.x -= player.xAcc
                # make player.yAcc smaller until no collision but for now i make it zero because frick you
                player.xAcc = 0
                
    player.xCol_1 = int((player.y+worldHAccHeight)/tileSize)+int((player.x-player.fWidth+worldHAccWidth)/tileSize)*worldHeight
    player.xCol_2 = int((player.y+worldHAccHeight)/tileSize)+int((player.x+player.fWidth+worldHAccWidth)/tileSize)*worldHeight
        
def mouseHBCheck():
    if (mouse.x-(displayHalfW))**2+(mouse.y-(displayHeight-150))**2 < 55**2:
        mouse.selectedHBSlot = 0
    else:
        if (mouse.y-(displayHeight-150))*0.485 > (mouse.x-displayHalfW):
            if (mouse.y-(displayHeight-150))*-0.485 < (mouse.x-displayHalfW):
                mouse.selectedHBSlot = 6+player.HBcycle
            elif (mouse.y-(displayHeight-150)) > (mouse.x-displayHalfW)*-0.485:
                mouse.selectedHBSlot = 5+player.HBcycle
            elif (mouse.y-(displayHeight-150)) > (mouse.x-displayHalfW)*0.485:
                mouse.selectedHBSlot = 4+player.HBcycle
            else:
                mouse.selectedHBSlot = 3+player.HBcycle
        else:
            if (mouse.y-(displayHeight-150))*-0.485 > (mouse.x-displayHalfW):
                mouse.selectedHBSlot = 2+player.HBcycle
            elif (mouse.y-(displayHeight-150)) < (mouse.x-displayHalfW)*-0.485:
                mouse.selectedHBSlot = 1+player.HBcycle
            elif (mouse.y-(displayHeight-150)) < (mouse.x-displayHalfW)*0.485:
                mouse.selectedHBSlot = 8+player.HBcycle
            else:
                mouse.selectedHBSlot = 7+player.HBcycle
        if mouse.selectedHBSlot > 8:
            mouse.selectedHBSlot -= 8
        if mouse.selectedHBSlot < 1:
            mouse.selectedHBSlot += 8
            
def mouse_stuff():
    mouse.x, mouse.y = pygame.mouse.get_pos()
    mouse.left = pygame.mouse.get_pressed()[0]
    mouse.right = pygame.mouse.get_pressed()[2]
    if stats.menu != "pregame":
        mouse.tile = int((mouse.y-camera.y+worldHAccHeight)/tileSize)+int((mouse.x-camera.x+worldHAccWidth)/tileSize)*worldHeight
    if stats.menu == "inventory":
        if displayHalfW-inventoryImg.get_width()/2 < mouse.x < displayHalfW+inventoryImg.get_width()/2 and displayHalfH-inventoryImg.get_height()/2-100 < mouse.y < displayHalfH+inventoryImg.get_height()/2-100:
            mouse.selectedSlot = abs(int((displayHalfW-inventoryImg.get_width()/2-mouse.x)/108))+abs(int((displayHalfH-inventoryImg.get_height()/2-100-mouse.y)/108))*5
            if mouse.click:
                if mouse.offInvBeat:
                    if player.selectedHBSlot == "":
                        if player.inventory[player.selectedSlot].item == player.inventory[mouse.selectedSlot].item and (player.inventory[player.selectedSlot].tag == "resource" or player.inventory[player.selectedSlot].item == "stone") and (player.inventory[mouse.selectedSlot].tag == "resource" or player.inventory[mouse.selectedSlot].item == "stone"):
                            if player.selectedSlot != mouse.selectedSlot:
                                if player.inventory[player.selectedSlot].amount+player.inventory[mouse.selectedSlot].amount <= stats.maxStack:
                                    player.inventory[mouse.selectedSlot].amount = player.inventory[player.selectedSlot].amount+player.inventory[mouse.selectedSlot].amount
                                    player.inventory[player.selectedSlot] = INVENTORY_ITEM()
                                else:
                                    player.inventory[player.selectedSlot].amount = 16-(player.inventory[player.selectedSlot].amount+player.inventory[mouse.selectedSlot].amount)
                                    player.inventory[mouse.selectedSlot].amount = stats.maxStack
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
                    mouse.offInvBeat     = False
                else:
                    player.selectedSlot = mouse.selectedSlot
                    mouse.offInvBeat = True
                                        
        else:
            mouse.selectedSlot = ""
            
        if (mouse.x-(displayHalfW))**2+(mouse.y-(displayHeight-150))**2 < 150**2:
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
                        player.selectedSlot = ""
                    mouse.offInvBeat = False
                else:
                    player.selectedHBSlot = mouse.selectedHBSlot
                    mouse.offInvBeat = True
        else:
            mouse.selectedHBSlot = ""
        
        
def display_tiles(animation):
    curTile = int((camera.y*-1+worldHAccHeight)/tileSize)+int((camera.x*-1+worldHAccWidth)/tileSize)*worldHeight
    for i in range(displayTWidth):
        for k in range(displayTHeight):
            if tiles[curTile].covered < 255:
                window.blit(tiles[curTile].sprite, (tiles[curTile].x+camera.x, tiles[curTile].y+camera.y))
                if tiles[curTile].tile == "water" or tiles[curTile].tile == "shore":
                    if tiles[curTile].waterCons != "":
                        if tiles[curTile].waveSprite[animation] != "":
                            if tiles[curTile].waveChance:
                                window.blit(tiles[curTile].waveSprite[animation], (tiles[curTile].x+camera.x, tiles[curTile].y+camera.y))
            if curTile < worldSize-1:
                curTile += 1
        if curTile < worldSize-(worldHeight):
            curTile += worldHeight-displayTHeight

def display_covered_tiles():
    curTile = int((camera.y*-1+worldHAccHeight)/tileSize)+int((camera.x*-1+worldHAccWidth)/tileSize)*worldHeight
    for i in range(displayTWidth):
        for k in range(displayTHeight):
            if tiles[curTile].covered > 0:
                coveredTile.set_alpha(tiles[curTile].covered)
                window.blit(coveredTile, (tiles[curTile].x+camera.x, tiles[curTile].y+camera.y))
            if curTile < worldSize-1:
                curTile += 1
        if curTile < worldSize-(worldHeight):
            curTile += worldHeight-displayTHeight

def uncover_tiles():
    curTile = int((player.y+worldHAccHeight-tileSize*(stats.viewDistance/2))/tileSize)+int((player.x+worldHAccWidth-tileSize*(stats.viewDistance/2))/tileSize)*worldHeight
    for i in range(stats.viewDistance):
        for j in range(stats.viewDistance):
            alphaMax = stats.viewDistance
            if i < stats.viewDistance/2:
                alphaMax -= i
            else:
                alphaMax -= stats.viewDistance-i
            if j < stats.viewDistance/2:
                alphaMax -= j
            else:
                alphaMax -= stats.viewDistance-j
            alphaMax*=25
                
            if (0 <= curTile < worldSize) and abs(tiles[curTile].y-player.y) < stats.viewDistance*tileSize:
                if tiles[curTile].covered > alphaMax:
                    tiles[curTile].covered -=10
                    if tiles[curTile].covered < 100:
                        tiles[curTile].covered = 0
            if curTile < worldSize-1:
                curTile += 1
        if curTile < worldSize-(stats.viewDistance):
            curTile += worldHeight-stats.viewDistance
        
def display_obj():
    for obj in objects:
        if tileSize*-2 < obj.x+camera.x < displayWidth+tileSize and tileSize*-2 < obj.y+camera.y < displayHeight+tileSize*2:
            if obj.i == "tile":
                if obj.building == "tree":
                    if obj.x < player.x < obj.x+tileSize and obj.y-obj.buildSprite[int(obj.health/10)].get_height()+tileSize*2 < player.y < obj.y:
                        obj.buildSprite[int(obj.health/10)].set_alpha(150)
                    else:
                        obj.buildSprite[int(obj.health/10)].set_alpha(255)
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
                if player.hotbar[0].item != "":
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
                               
def display_selected_tile():
    window.blit(closeTile, (tiles[mouse.tile].x+camera.x, tiles[mouse.tile].y+camera.y))
    # eventually i'll expand this out to trees and stuff
    
def check_player_reach():
    player.reach = stats.playerReach
    for enhancement in player.hotbar[0].enhancements:
        if enhancement == "reach":
            player.reach += tileSize/3
    if (mouse.x-(player.x+camera.x))**2+(mouse.y-(player.y+camera.y))**2 < player.reach**2:
        player.inReach = True
    else:
        player.inReach = False
        
        
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
    camera.x-=((camera.x-displayHalfW)-(player.x*-1))/camera.smoothness
    camera.y-=((camera.y-displayHalfH)-(player.y*-1))/camera.smoothness
    
    camera.x=int(camera.x*2)/2
    camera.y=int(camera.y*2)/2

    if camera.x < worldWidth*tileSize/-2+displayWidth+tileSize/2:
        camera.x = worldWidth*tileSize/-2+displayWidth+tileSize/2
    if camera.x > worldWidth*tileSize/2:
        camera.x = worldWidth*tileSize/2
        
    if camera.y < worldHeight*tileSize/-2+displayHeight:
        camera.y = worldHeight*tileSize/-2+displayHeight
    if camera.y > worldHeight*tileSize/2:
        camera.y = worldHeight*tileSize/2

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
            
        if arm[i].punching <= 3 or stats.GODMODE or arm[i].holdingItem == "":
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
            
def rearrange_obj(objs):
    objs = []
    if not stats.GODMODE:
        objs.append(player)
        
    
    curTile = int((camera.y*-1+worldHAccHeight)/tileSize)+int((camera.x*-1+worldHAccWidth)/tileSize)*worldHeight
    for i in range(displayTWidth):
        for k in range(displayTHeight):
            if tiles[curTile].building != "":
                objs.append(tiles[curTile])
            if curTile < worldSize-1:
                curTile += 1
        if curTile < worldSize-(worldHeight):
            curTile += worldHeight-displayTHeight
                        
    for drops in droppedItems:
        objs.append(drops)
        objs[-1].y+=16
        
    for obj in objs:
        if obj.i == "tile":
            if obj.building == "tree" or obj.building == "grass" or obj.building == "hay":
                obj.y+=tileSize
                
    sortedList = sorted(objs, key=lambda objs: objs.y)
    
    if stats.GODMODE:
        sortedList.append(player)
        
    for obj in objs:
        if obj.i == "tile":
            if obj.building == "tree" or obj.building == "grass" or obj.building == "hay":
                obj.y-=tileSize
    for obj in objs:
        if obj.i == "item":
            obj.y-=16

    return sortedList

def wave_rechance():
    for tile in tiles:
        if tileSize*-1 < tile.x+camera.x < displayWidth+tileSize and tileSize*-1 < tile.y+camera.y < displayHeight+tileSize*1:
            if tile.tile == "water" or tile.tile == "shore":
                if tile.waveSprite !=["", "", ""]:
                    tile.waveChance = random.randint(0, 1)

def item_pickup():
    if globalKeys.key[pygame.K_SPACE]:
        pickedUp = False
        space = False
        if player.curWeight <= player.maxWeight or stats.GODMODE:
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
                        if player.inventory[j].amount < stats.maxStack and player.inventory[j].item == droppedItems[i].item and (player.inventory[j].tag == "resource" or player.inventory[j].item == "stone"):
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
                                    player.inventory[j].tag = "tool"
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
            
def display_inventory():
    invX = displayHalfW-inventoryImg.get_width()/2
    invY = displayHalfH-inventoryImg.get_height()/2-100
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

def create_particles(x, y, r, g, b, amount):
    for i in range(amount):
        colChange = random.randint(-5, 5)
        r += colChange
        g += colChange
        b += colChange
        if r < 0:
            r = 0
        if r > 255:
            r = 255
        if g < 0:
            g = 0
        if g > 255:
            g = 255
        if b < 0:
            b = 0
        if b > 255:
            b = 255
        particles.append(PARTICLE(x, y, (r, g, b)) )

def display_particles():
    for particle in particles:
        particle.x += particle.goingX
        particle.y += particle.goingY
        window.blit(particle.sprite, (particle.x, particle.y))
        particle.sprite = pygame.Surface((10,10))
        particle.sprite.set_alpha(particle.alpha)
        particle.sprite.fill(particle.col)
        particle.alpha -= 10
    delIndicies = []
    for i in range(len(particles)):
        if particles[i].alpha <= 0:
            delIndicies.append(i)
    delIndicies.sort(reverse=True)
    for i in range(len(delIndicies)):
        del particles[delIndicies[i]]

def display_crafting():
    if cstats.craftingAnimation:
       cstats.craftingAnimation-=1 
    if stats.crafting == "":
        if cstats.invX < displayHalfW-inventoryImg.get_width()/2+150:
            cstats.invX+=50
    else:
        if cstats.invX > displayHalfW-inventoryImg.get_width()/2-350:
            cstats.invX-=50
    cstats.invY = displayHalfH-inventoryImg.get_height()/2-100
    window.blit(inventoryImg, (cstats.invX, cstats.invY))
    window.blit(craftingSelection, (cstats.invX-150, cstats.invY))
    if mouse.click:
        if cstats.invX-150 < mouse.x < cstats.invX-150+craftingSelection.get_width() and cstats.invY < mouse.y < cstats.invY+craftingSelection.get_height():
            stats.craftingMenu = craftingSelectsDict[int(((mouse.y-cstats.invY)/(cstats.invY+craftingSelection.get_height()))*6)+1]
            cstats.crafting = ""
    selIndex = craftingSelectsDict[stats.craftingMenu]
           
    if mouse.click:
        if not (cstats.invX-150 < mouse.x < cstats.invX-150+craftingSelection.get_width() and cstats.invY < mouse.y < cstats.invY+craftingSelection.get_height()):
            relX = cstats.invX-displayHalfW-inventoryImg.get_width()/2+mouse.x
            relY = mouse.y-cstats.invY
            if cstats.invX < mouse.x < cstats.invX+inventoryImg.get_width() and displayHalfH-inventoryImg.get_height()/2-100 < mouse.y < displayHalfH+inventoryImg.get_height()/2-100:
                ind = int((mouse.x-cstats.invX)/108)+int((mouse.y-cstats.invY)/108)*5
                if ind < len(crafts[selIndex]):
                    stats.crafting = crafts[selIndex][ind].item.strip()
                    cstats.craftIndex = ind
                elif not (108 < relX < 395 and 312 < relY < 406):
                    stats.crafting = ""
            
            elif not (108 < relX < 395 and 312 < relY < 406):
                stats.crafting = ""
        else:
            stats.crafting = ""
            
    pygame.draw.rect(window, (107, 107, 107), (cstats.invX+inventoryImg.get_width()+10, cstats.invY, displayHalfW-cstats.invX-200+110, inventoryImg.get_height()))
    pygame.draw.rect(window, (158, 158, 158), (cstats.invX+inventoryImg.get_width()+15, cstats.invY+5, displayHalfW-cstats.invX-210+110, inventoryImg.get_height()-10))
    window.blit(selectedCrafting, (cstats.invX-150-6, cstats.invY+selIndex*108-6))
    
    for i in range(len(crafts[selIndex])):
        window.blit(crafts[selIndex][i].sprite, (16+cstats.invX+(i%5)*108, 16+cstats.invY+int(i/5)*108))
        if cstats.invX < displayHalfW-inventoryImg.get_width()/2-200 and stats.crafting == crafts[selIndex][i].item:
            window.blit(crafts[selIndex][i].bigSprite, (cstats.invX+displayHalfW-400, cstats.invY))
            write_text(crafts[selIndex][i].item, cstats.invX+displayHalfW-250, cstats.invY+50, 50-len(crafts[selIndex][i].item)*1.8, False, 255)
            for j in range(len(crafts[selIndex][i].itemIn)):
                window.blit(crafts[selIndex][i].itemInSprite[j], (cstats.invX+displayHalfW-400+(j%4)*120, cstats.invY+150+int(j/4)*75))
                write_text(str(crafts[selIndex][i].amountIn[j]), cstats.invX+displayHalfW-350+(j%4)*120, cstats.invY+180+int(j/4)*75, 30, False, 255)
                for k in range(len(player.inventoryTotalItem)):
                    if player.inventoryTotalItem[k] == crafts[selIndex][i].itemIn[j]:
                        if player.inventoryTotalAmount[k] >= crafts[selIndex][i].amountIn[j]:
                            window.blit(tickImg, (cstats.invX+displayHalfW-400+(j%4)*120, cstats.invY+220+int(j/4)*75))
                        else:
                            window.blit(crafts[selIndex][i].itemInSprite[j], (cstats.invX+displayHalfW-400+(j%4)*120, cstats.invY+220+int(j/4)*75))
                            window.blit(crossImg, (cstats.invX+displayHalfW-400+(j%4)*120, cstats.invY+220+int(j/4)*75))
                            write_text(str(crafts[selIndex][i].amountIn[j]-player.inventoryTotalAmount[k]), cstats.invX+displayHalfW-350+(j%4)*120, cstats.invY+220+int(j/4)*75, 30, False, 255)
                        break
                    elif k+1 == len(player.inventoryTotalItem):
                        window.blit(crafts[selIndex][i].itemInSprite[j], (cstats.invX+displayHalfW-400+(j%4)*120, cstats.invY+220+int(j/4)*75))
                        window.blit(crossImg, (cstats.invX+displayHalfW-400+(j%4)*120, cstats.invY+220+int(j/4)*75))
                        write_text(str(crafts[selIndex][i].amountIn[j]), cstats.invX+displayHalfW-350+(j%4)*120, cstats.invY+220+int(j/4)*75, 30, False, 255)
                                    
            window.blit(craftButton, (cstats.invX+displayHalfW-300, cstats.invY+310))
            write_text("craft", cstats.invX+displayHalfW-200, cstats.invY+340, 40-cstats.craftingAnimation, True, 255)
        
    if mouse.click and selIndex != "" and cstats.craftIndex != "" and not (cstats.invX-150 < mouse.x < cstats.invX-150+craftingSelection.get_width() and cstats.invY < mouse.y < cstats.invY+craftingSelection.get_height()):
        relX = cstats.invX-displayHalfW-inventoryImg.get_width()/2+mouse.x
        relY = mouse.y-cstats.invY
        if 108 < relX < 395 and 312 < relY < 406:
            RN = crafts[selIndex][cstats.craftIndex].itemIn
            AN = crafts[selIndex][cstats.craftIndex].amountIn
            craft(crafts[selIndex][cstats.craftIndex], RN, AN)
            
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
        cstats.craftingAnimation = 20
        found = False
        # give player the item
        if craft.tag == "resource":
            for i in range(len(player.inventory)):
                if player.inventory[i].item == craft.item and player.inventory[i].amount < stats.maxStack:
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
    
                
              
def display_hotbar():
    if stats.menu == "inventory":
        ypos = displayHeight-150
    else:
        ypos = displayHeight-50
        
    if (mouse.x-(displayHalfW))**2+(mouse.y-(ypos))**2 > 150**2 or stats.menu == "inventory":
        window.blit(hotbarImgTR, (displayHalfW-150, ypos-150))
    else:
        window.blit(hotbarImg, (displayHalfW-150, ypos-150))
        
    if stats.menu == "inventory":
        if mouse.selectedHBSlot != "":
            if mouse.selectedHBSlot:
                slot = mouse.selectedHBSlot-player.HBcycle
                if slot < 1:
                    slot+=8
            else:
                slot = 0
            window.blit(hotbarMouseImg[slot], (displayHalfW-125, ypos-125))
        if player.selectedHBSlot != "" and mouse.offInvBeat:
            if player.selectedHBSlot:
                slot = player.selectedHBSlot-player.HBcycle
                if slot < 1:
                    slot+=8
            else:
                slot = 0
            window.blit(hotbarSelectedImg[slot], (displayHalfW-125, ypos-125))
        
    for i in range(len(player.hotbar)):
        if i:
            x = displayHalfW-25/2+(math.cos(math.radians(i*45))*130)
            y = ypos-25/2-(math.sin(math.radians(i*45))*130)
            text = i+player.HBcycle
            if text > 8:
                text-=8
            write_text(str((text)), x, y, 25, False, 255)
            
    for i in range(len(player.hotbar)):
        if player.hotbar[i].sprite != "":
            if i == 0:
                window.blit(player.hotbar[i].sprite, (displayHalfW-32, ypos-32))
                if player.hotbar[i].durability:
                    write_text(str(player.hotbar[i].durability)+"%", displayHalfW-32, ypos-32, 25, False, 255)
                for j in range(len(player.hotbar[i].enhancements)):
                    window.blit(enhancementSprites[player.hotbar[i].enhancements[j]], (displayHalfW+3-40+j*20, ypos+30))
            else:
                x = displayHalfW-32+(math.cos(math.radians((i-player.HBcycle)*45))*100)
                y = ypos-32-(math.sin(math.radians((i-player.HBcycle)*45))*100)
                
                window.blit(player.hotbar[i].sprite, (x, y))
                if player.hotbar[i].durability:
                    write_text(str(player.hotbar[i].durability)+"%", x, y+15, 25, False, 255)
                for j in range(len(player.hotbar[i].enhancements)):
                    window.blit(enhancementSprites[player.hotbar[i].enhancements[j]], (x+j*20, y+40))
                            
    
def weight_cal():
    player.curWeight = 0
    for item in player.inventory:
        player.curWeight += item.weight*item.amount
    for item in player.hotbar:
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

def display_preview_world():
    for x in range(worldWidth):
        for y in range(worldHeight):
            index = x*worldHeight+y
            if index < len(tiles):  
                pygame.draw.rect(window, tiles[index].pregameColour, (1200+x*3, y*3, 3, 3))
    

def generate_world():
    window.fill(BLACK)
    global tiles, tileAmount
    write_text("generating world...", displayHalfW, displayHalfH-125, 100, True, 255)
    write_text("this might take a while", displayHalfW, displayHalfH, 100, True, 255)
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
    
def use_item():
    if int(arm[0].punching) <= 1 and int(arm[1].punching) <= 1:
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
            for i in range(stats.GODMODE*stats.splashMine+1):
                for j in range(stats.GODMODE*stats.splashMine+1):
                    if stats.GODMODE:
                        if -1 < int((mouse.y-tileSize+(tileSize*i)-camera.y+worldHAccHeight)/tileSize)+int((mouse.x-tileSize+(tileSize*j)-camera.x+worldHAccWidth)/tileSize)*worldHeight < worldSize:
                            mouse.tile = int((mouse.y-tileSize+(tileSize*i)-camera.y+worldHAccHeight)/tileSize)+int((mouse.x-tileSize+(tileSize*j)-camera.x+worldHAccWidth)/tileSize)*worldHeight
                    
                    if tiles[mouse.tile].building != "":
                        if tiles[mouse.tile].health > 0:
                            for item in itemDamages:
                                if item[0] == player.hotbar[0].item:
                                    if item[1] == tiles[mouse.tile].tag:
                                        tiles[mouse.tile].health -= item[2]+stats.GODMODE*10000
                                        for k in range(len(player.hotbar[0].enhancements)):
                                            if player.hotbar[0].enhancements[k] == "damage":
                                                tiles[mouse.tile].health -= item[2]/3+stats.GODMODE*10000
                                        create_particles(mouse.x, mouse.y, tiles[mouse.tile].col[0], tiles[mouse.tile].col[1], tiles[mouse.tile].col[2], 20)
                    
                        if tiles[mouse.tile].health <= 0:
                            tiles[mouse.tile].health = 0 
                            tiles[mouse.tile].buildingSprite = ""
                            tiles[mouse.tile].tag = ""
                            tiles[mouse.tile].i = ""
                            tiles[mouse.tile].canwalk = True
                            if tiles[mouse.tile].tile == "water":
                                tiles[mouse.tile].canwalk = False
                            for drop in dropsDict[tiles[mouse.tile].building]:
                                luckMin = drop[1]
                                luckMax = drop[2]
                                for enhancement in player.hotbar[0].enhancements:
                                    if enhancement == "luck":
                                        luckMin *= 1.2
                                        luckMax *= 1.5 
                                        
                                for i in range(int(random.randint(int(luckMin), int(luckMax))/100)):
                                    droppedItems.append(DROPPED_ITEM(tiles[mouse.tile].x, tiles[mouse.tile].y, drop[0], [], False))
                            tiles[mouse.tile].building = ""

                        if player.hotbar[0].item != "stone":
                            for enhancement in player.hotbar[0].enhancements:
                                if enhancement != "durability":
                                    player.hotbar[0].durability-=0.2
                            player.hotbar[0].durability-=0.2
                            player.hotbar[0].durability = round(player.hotbar[0].durability, len(str(int(player.hotbar[0].durability)+1)))
                            
                            if player.hotbar[0].durability <= 0:
                                player.hotbar[0] = INVENTORY_ITEM()
                        
        mouse.tile = int((mouse.y-camera.y+worldHAccHeight)/tileSize)+int((mouse.x-camera.x+worldHAccWidth)/tileSize)*worldHeight
        
def nuke():
    for i in range(len(tiles)):
        if tiles[i].building != "":
            tiles[i].building = ""
            tiles[i].buildingSprite = ""
            tiles[i].health = 0
            tiles[i].tag = ""
            tiles[i].i = ""
            tiles[i].canwalk = True
            tiles[i].drops = []


def start_game():
    stats.menu = "game"
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

def display_building():
    displayX = bstats.x
    displayY = bstats.y
    window.blit(buildingPanel, (displayX-buildingPanel.get_width()/2, displayY-buildingPanel.get_height()/2))
    bstats.buildSelected = []
    if displayY-50 > mouse.y:
        bstats.buildSelected.append("wood")
    elif displayY+50 > mouse.y:
        bstats.buildSelected.append("stone")
    else:
        bstats.buildSelected.append("hay")
        
    if displayX-50 > mouse.x:
        bstats.buildSelected.append("floor")
    elif displayX+50 > mouse.x:
        bstats.buildSelected.append("wall")
    else:
        bstats.buildSelected.append("door")
        
def display_ghost_building():
    if bstats.sprite != "" and player.inReach:
        sprite = bstats.sprite
        sprite.set_alpha(200)
        if bstats.buildSelected[1] == "floor":
            window.blit(bstats.sprite, (tiles[mouse.tile].x+camera.x, tiles[mouse.tile].y+camera.y))
        else:
            window.blit(bstats.sprite, (tiles[mouse.tile].x+camera.x, tiles[mouse.tile].y+camera.y-tileHalfS))

def build():
    if stats.GODMODE:
        canBuild = True
    else:
        canBuild = False
        temp = buildingResources[bstats.buildSelected[1]]
        amountNeeded = temp
        amountTaken = 0
        breaking = False
        for i in range(len(player.inventoryTotalItem)):
            if player.inventoryTotalItem[i] == bstats.buildSelected[0]:
                if player.inventoryTotalAmount[i] >= amountNeeded:
                    canBuild = True
                    for j in range(len(player.inventory)):
                        if player.inventory[j].item == bstats.buildSelected[0]:
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
        if bstats.buildSelected[1] == "wall" or bstats.buildSelected[1] == "door":
            tiles[mouse.tile].canwalk = False
        if bstats.buildSelected[1] == "floor":
            tiles[mouse.tile].canwalk = True
        tiles[mouse.tile].col = (122, 62, 10)
        tiles[mouse.tile].building = bstats.buildSelected[1]
        tiles[mouse.tile].buildSprite = bstats.sprite
        tiles[mouse.tile].buildSprite.set_alpha(255)
        tiles[mouse.tile].i = "tile"
        tiles[mouse.tile].health = buildingHealths[bstats.buildSelected[0]+" "+bstats.buildSelected[1]]
        tiles[mouse.tile].tag = buildingTags[bstats.buildSelected[0]]

def player_deenergize(points):
    player.hunger  -= points/5
    player.hydration  -= points/2
    player.energy  -= points*4
    player.stamina -= points/5
    
def player_energize():
    if player.energy < player.stamina:
        player.energy += 0.2
        if player.energy > player.stamina:
            player.energy = player.stamina

bord = 5
cols = [(32, 29, 209), (34, 78, 199), (46, 137, 217), (37, 175, 217), (56, 224, 213), (54, 214, 102), (44, 232, 23), (97, 217, 37), (199, 217, 37), (217, 193, 37), (217, 151, 37), (217, 82, 28), (219, 49, 11)]
def display_player_gui():
    # energy, stamina, hunger, hydration
    pygame.draw.rect(window, BLACK, (50, displayHeight-350, 70, 300))
    pygame.draw.rect(window, (29, 227, 7), (55, displayHeight-55-(player.stamina/100)*290, 30, (player.stamina/100)*290))
    pygame.draw.rect(window, (227, 209, 16), (85, displayHeight-55-(player.energy/100)*290, 30, (player.energy/100)*290))
    pygame.draw.rect(window, BLACK, (150, displayHeight-350, 40, 300))
    pygame.draw.rect(window, (17, 185, 214), (155, displayHeight-55-(player.hydration/500)*290, 30, (player.hydration/500)*290))
    pygame.draw.rect(window, BLACK, (220, displayHeight-350, 40, 300))
    pygame.draw.rect(window, (201, 114, 8), (225, displayHeight-55-(player.hunger/500)*290, 30, (player.hunger/500)*290))

    # health
    pygame.draw.rect(window, BLACK, (displayWidth-150, displayHeight-150, 100, 100))
    pygame.draw.rect(window, (255, 0, 50), (displayWidth-145, displayHeight-55-(player.health/player.maxHealth)*90, 90, (player.health/player.maxHealth)*90))
    write_text(str(player.health)+"/"+str(player.maxHealth), displayWidth-105, displayHeight-120, 50-len(str(player.health)+"/"+str(player.maxHealth))*5, True, 255)

    # temperature
    pygame.draw.polygon(window, BLACK, ((displayHalfW-420, 0), (displayHalfW+420, 0), (displayHalfW+365, 55), (displayHalfW-365, 55)))
    pygame.draw.polygon(window, (255, 255, 255), ((displayHalfW-410, 0), (displayHalfW-360, 0), (displayHalfW-360, 50)))
    pygame.draw.polygon(window, (224, 25, 25), ((displayHalfW+410, 0), (displayHalfW+360, 0), (displayHalfW+360, 50)))
    for i in range(len(cols)):
        pygame.draw.rect(window, cols[i], (displayHalfW-355+55*i, 0, 50, 50))
    window.blit(temperatureIndicator, (displayHalfW-25+(player.temperature-36)*10, 0))
    
    # weight
    pygame.draw.polygon(window, BLACK, ((displayHalfW-330, 70), (displayHalfW+330, 70), (displayHalfW+280, 120), (displayHalfW-280, 120)))
    pygame.draw.polygon(window, (217, 174, 132), ((displayHalfW-330+bord*3, 70+bord), (displayHalfW+330-bord*3, 70+bord), (displayHalfW+280-bord, 120-bord), (displayHalfW-280+bord, 120-bord)))

def temperature_cal():
    if player.temperature < 0:
        player.temperature = 0
    if player.temperature > 72:
        player.temperature = 72
    

alph = 0

tileAmount = 0
generate_world()
start_game()

while gameRunning:
    
    frameTime = gameClock.tick(gameFPS)
    pygame.time.delay(int(frameTime/1000))    
    keyList = pygame.key.get_pressed()
    globalKeys.key = pygame.key.get_pressed()
    mouse.click = False
    mouse.release = False
    
    if stats.menu == "pregame":
        mouse_stuff()
        
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
            window.blit(pregameAnimateBackground[int(pregameAnimation/510)], (0, (displayHeight-displayWidth)+pregameAnimation%510))
            write_text(pregameFloatingTexts[int(pregameAnimation/510)*2], displayHalfW, (pregameAnimation%510)*1.5, 50+(pregameAnimation%510)*0.1, True, alph)
            write_text(pregameFloatingTexts[int(pregameAnimation/510)*2+1], displayHalfW, (pregameAnimation%510)*1.5+70+(pregameAnimation%510)*0.1, 50+(pregameAnimation%510)*0.1, True, alph)
        else:
            # MAIN PREGAME
            pregameBackground.set_alpha((pregameAnimation-2040)/2)
            window.blit(pregameBackground, (0, -175))
            if pregameAnimation < 2500:
                write_text("bloks olc", 750+random.randint(-5, 5), (pregameAnimation-2300)/2-50+random.randint(-2, 2), 150, True, 255)
            else:
                write_text("bloks olc", 750, 50, 150, True, 255)
            if 2500 < pregameAnimation < 2700:
                pygame.draw.rect(window, GREY, ((pregameAnimation-2500)*-2+displayWidth, 0, displayWidth, displayHeight))
                pygame.draw.rect(window, (50, 50, 50), ((pregameAnimation-2500)*-2+displayWidth, 175, 500, 125))
                write_text("start", (pregameAnimation-2500)*-2+displayWidth+200, 200, 75, True, 255)
            elif 3000+displayHalfW-1 > pregameAnimation >= 2700:
                pygame.draw.rect(window, GREY, (displayWidth-400, 0, displayWidth, displayHeight))
                if mouse.x > displayWidth-400 and 175 < mouse.y < 300:
                    pygame.draw.rect(window, (100, 100, 100), (displayWidth-400, 175, 500, 125))
                else:
                    pygame.draw.rect(window, (50, 50, 50), (displayWidth-400, 175, 500, 125))
                write_text("start", displayWidth-200, 200, 75, True, 255)
            if mouse.click and displayWidth-400 < mouse.x and 125 < mouse.y < 275:
                pregameAnimation = 3000
                # world customisation
            if pregameAnimation >= 3000:
                pygame.draw.rect(window, BLACK, (displayHalfW-(pregameAnimation-3000), 0, (pregameAnimation-3000)*2, displayHeight))
                if pregameAnimation-3000 < displayHalfW:
                    pregameAnimation+=30
                else:
                    customise_world()

                
                
            
    else:
        if stats.menu == "game":
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
                if event.key == pygame.K_F1:
                    if gameFPS:
                        gameFPS = 0
                    else:
                        gameFPS = 60
                if event.key == pygame.K_F11:
                    pygame.init()
                    if stats.fullscreen == True:
                        stats.fullscreen = False
                        window = pygame.display.set_mode((displayWidth, displayHeight))
                    else:
                        stats.fullscreen = True
                        window = pygame.display.set_mode((displayWidth, displayHeight), pygame.FULLSCREEN)

                if event.key == pygame.K_TAB:
                    if stats.menu == "inventory":
                        stats.menu = "game"
                    elif stats.menu == "building":
                        stats.menu = "game"
                    else:
                        mouse.offInvBeat = False      
                        stats.menu = "inventory"
                        cstats = CSTATS()
                if event.key == pygame.K_ESCAPE:
                    if stats.menu == "inventory" or stats.menu == "building" or stats.menu == "settings":
                        stats.menu = "game"
                    else:
                        mouse.offInvBeat = False              
                        stats.menu = "settings"
                    
                if event.key == pygame.K_v:
                    update_inventory_total()
                        
                if event.key == pygame.K_r:
                    cycle = player.HBcycle+2
                    if cycle > 8:
                        cycle-=8
                                            
                    temp = player.hotbar[0]
                    player.hotbar[0] = player.hotbar[cycle]
                    player.hotbar[cycle] = temp
                
                if event.key == pygame.K_q or event.key == pygame.K_DELETE:
                    if stats.menu == "inventory":
                        if player.selectedSlot != "":
                            if event.key == pygame.K_q:
                                for i in range(player.inventory[player.selectedSlot].amount):
                                    droppedItems.append(DROPPED_ITEM(tiles[player.tile].x, tiles[player.tile].y, player.inventory[player.selectedSlot].item, player.inventory[player.selectedSlot].enhancements))
                            
                            player.inventory[player.selectedSlot] = INVENTORY_ITEM()
                            player.selectedSlot = ""
                            mouse.offInvBeat = False
                            update_inventory_total()
                        
            if event.type == pygame.MOUSEWHEEL:
                player.HBcycle += event.y
                if player.HBcycle < 0:
                    player.HBcycle = 7
                if player.HBcycle > 7:
                    player.HBcycle = 0
                mouse.click = False
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse.click = True
                if pygame.mouse.get_pressed()[2]:
                     if player.hotbar[0].item == "wood hammer":
                         bstats.x = mouse.x
                         bstats.y = mouse.y
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse.release = True

        check_player_reach()

        if camera.smoothness > camera.IGSmoothness:
            camera.smoothness*=0.9
        else:
            camera.smoothness = camera.IGSmoothness
        mouse_stuff()

        arm[0].holdingItem = player.hotbar[0].item
        if player.hotbar[0].item != "":
            arm[0].holdingItemSprite = pygame.transform.scale(player.hotbar[0].sprite, (32, 32))
            player.punchTurn = 0
        weight_cal()
        temperature_cal()
        if stats.menu == "game":
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
        display_tiles(int(waveAnimation))
        display_obj()
        display_covered_tiles()
        
        if stats.menu == "game":
            if player.hotbar[0].item == "wood hammer":
                if mouse.right:
                    display_building()
                if len(bstats.buildSelected):
                    if mouse.release:
                        bstats.sprite = pygame.transform.scale(pygame.image.load("sprites/buildings/"+bstats.buildSelected[1]+"/"+bstats.buildSelected[0]+"/.png"), (tileSize, tileSize))
                        if bstats.buildSelected[1] == "wall" or bstats.buildSelected[1] == "door":
                            bstats.sprite = pygame.transform.scale(bstats.sprite, (tileSize, tileSize*1.5))

                    if player.inReach and (tiles[mouse.tile].building == "" or (tiles[mouse.tile].building[-5:len(tiles[mouse.tile].building)] == "floor" and (bstats.buildSelected[1] == "wall" or bstats.buildSelected[1] == "door"))):
                        if ((bstats.buildSelected[1] == "wall" or bstats.buildSelected[1] == "door") and (mouse.tile != player.xCol_1 and mouse.tile != player.xCol_2) or bstats.buildSelected[1] in "floor"):
                            display_ghost_building()
                            if mouse.left:
                                build()
            else:
                bstats.buildSelected = []
                if player.inReach:
                    display_selected_tile()
            if bstats.buildSelected != []:
                write_text(str(buildingResources[bstats.buildSelected[1]]), mouse.x+20, mouse.y, 35, False, 200)
                window.blit(buildResourceSprites[bstats.buildSelected[0]], (mouse.x+55, mouse.y))
        
        if stats.menu != "game":
            window.blit(greyScaleImg, (0, 0))
            if stats.menu == "inventory":
                window.blit(craftingButton, (displayWidth-95, 20))
                if mouse.click and displayWidth-95 < mouse.x < displayWidth-20 and 20 < mouse.y < 95:
                    stats.menu = "crafting"
            elif stats.menu == "crafting":
                window.blit(invButton, (displayWidth-95, 20))
                if mouse.click and displayWidth-95 < mouse.x < displayWidth-20 and 20 < mouse.y < 95:
                    stats.menu = "inventory"
            
        display_player_gui()
                
        if stats.menu == "inventory":
            display_inventory()
        if stats.menu == "crafting":
            display_crafting()
        else:
            display_hotbar()
        display_particles()
        if stats.menu != "crafting":
            write_text("x ="+str(int(tiles[player.tile].x/tileSize)), 50, 50, 20, False, 255)
            write_text("y ="+str(int(tiles[player.tile].y/tileSize*-1+worldHalfH)), 50, 100, 20, False, 255)
            write_text("weight:"+str(int(player.curWeight*100)/100)+"/"+str(int(player.maxWeight)), displayHalfW, 75, 35, True, 255)
    window.blit(mouse.sprite, (mouse.x-11, mouse.y-7))
    pygame.display.update()
    window.fill(GREY)

    
pygame.quit()
