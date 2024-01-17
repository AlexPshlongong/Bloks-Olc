import math, random, pygame
from crafting import *
from perlin_noise import PerlinNoise

tileSize = 50

class STATS():
    def __init__(self):
        self.borderedTextures = False
        self.GODMODE = False
        self.splashMine = 5
        self.itemMomentum = 15
        self.maxStack = 16+self.GODMODE*984
        self.menu = "pregame"
        self.craftingMenu = "materials"
        self.crafting = ""
        self.fullscreen = False
        self.viewDistance = 17+self.GODMODE*50
        self.playerReach = tileSize*2+self.GODMODE*988
stats = STATS()

BLACK = (0, 0, 0)
GREY = (25, 25, 25)
displayHeight = 1040
displayWidth = 1900
displayHalfH = displayHeight/2
displayHalfW = displayWidth/2
pygame.init()
window = pygame.display.set_mode((displayWidth, displayHeight))
pygame.mouse.set_visible(0)
gameFPS = 60
gameClock = pygame.time.Clock()
letters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "-", "=", "colon", "!", "(", ")", ",", "slash", ".", "%"]
letterSprites = []
for letter in letters:
    letterSprites.append(pygame.image.load("sprites/letters/"+letter.lower()+".png").convert_alpha())
hotbarMouseImg = []
hotbarSelectedImg = []
for i in range(9):
    hotbarMouseImg.append(pygame.transform.scale(pygame.image.load("sprites/gui/mouse selected hotbar/"+str(i)+".png").convert_alpha(), (250, 250)))
    hotbarSelectedImg.append(pygame.transform.scale(pygame.image.load("sprites/gui/selected hotbar/"+str(i)+".png").convert_alpha(), (250, 250)))
invButton = pygame.transform.scale(pygame.image.load("sprites/gui/inventory button.png").convert_alpha(), (75, 75))
craftingButton = pygame.transform.scale(pygame.image.load("sprites/gui/crafting button.png").convert_alpha(), (75, 75))
craftingSelection = pygame.transform.scale_by(pygame.image.load("sprites/gui/crafting selection.png").convert_alpha(), 6)
selectedCrafting = pygame.transform.scale_by(pygame.image.load("sprites/gui/selected crafting.png").convert_alpha(), 6)
hotbarImgTR = pygame.transform.scale(pygame.image.load("sprites/gui/transparent hotbar.png").convert_alpha(), (300, 300))
hotbarImg = pygame.transform.scale(pygame.image.load("sprites/gui/hotbar.png").convert_alpha(), (300, 300))
buildingPanel = pygame.transform.scale(pygame.image.load("sprites/gui/building panel.png").convert_alpha(), (300, 300))
inventoryImg = pygame.transform.scale_by(pygame.image.load("sprites/gui/inventory.png").convert_alpha(), 6)
selectedSlotImg = pygame.transform.scale_by(pygame.image.load("sprites/gui/selected slot.png").convert_alpha(), 6)
mouseSlotImg = pygame.transform.scale_by(pygame.image.load("sprites/gui/mouse slot.png").convert_alpha(), 6)
greyScaleImg =  pygame.transform.scale(pygame.image.load("sprites/gui/grey scale.png").convert_alpha(), (1920, 1080))
craftButton = pygame.transform.scale_by(pygame.image.load("sprites/gui/craft button.png").convert_alpha(), 6)
tickImg =  pygame.transform.scale(pygame.image.load("sprites/gui/tick.png").convert_alpha(), (64, 64))
crossImg =  pygame.transform.scale(pygame.image.load("sprites/gui/cross.png").convert_alpha(), (64, 64))
temperatureIndicator = pygame.transform.scale(pygame.image.load("sprites/gui/temp indicator.png").convert_alpha(), (50, 50))

enhancementSprites = {"luck" : pygame.transform.scale(pygame.image.load("sprites/gui/enhancements/luck.png").convert_alpha(), (18, 18)),
                      "damage" : pygame.transform.scale(pygame.image.load("sprites/gui/enhancements/damage.png").convert_alpha(), (18, 18)),
                      "reach" : pygame.transform.scale(pygame.image.load("sprites/gui/enhancements/reach.png").convert_alpha(), (18, 18)),
                      "durability" : pygame.transform.scale(pygame.image.load("sprites/gui/enhancements/durability.png").convert_alpha(), (18, 18))}

pregameBackground = (pygame.transform.scale(pygame.image.load("sprites/gui/pregame background/"+str(random.randint(1, 3))+".png").convert_alpha(), (displayWidth, displayHeight+200)))
nums = [1, 2, 3, 4]
pregameAnimateBackground = []
for i in range(4):
    ind = random.randint(0, 3-i)
    pregameAnimateBackground.append(pygame.transform.scale(pygame.image.load("sprites/gui/pregame animation background/"+str(nums[ind])+".png").convert_alpha(), (displayWidth, displayWidth)))
    del nums[ind]
pregameAnimation = 0
pregameFloatingTexts = ["born in the",
                        "coldest mounains",
                        "raised in the",
                        "harshest forests",
                        "survived as a",
                        "legendary warrior",
                        "and reborn in",
                        "the world of..."]

craftingSelectsDict = {1: "materials",
                       2: "tools",
                       3: "armour",
                       4: "special",
                       "materials" : 0,
                       "tools" : 1,
                       "armour" : 2,
                       "special" : 3}
class CSTATS():
    def __init__(self):
        self.invX = displayHalfW-inventoryImg.get_width()/2+150
        self.invY = displayHalfH-inventoryImg.get_height()/2-100
        self.craftIndex = ""
        self.craftingAnimation = 0
        
cstats = CSTATS()
class CTEMP():
    def __init__(self):
        self.amountNeeded = []
        self.resourcesNeeded = []
ctemp = CTEMP()

buildResourceSprites = {"wood" : pygame.transform.scale(pygame.image.load("sprites/items/wood.png").convert_alpha(), (40, 40)),
    "stone" :  pygame.transform.scale(pygame.image.load("sprites/items/stone.png").convert_alpha(), (40, 40)),
    "hay" :  pygame.transform.scale(pygame.image.load("sprites/items/hay.png").convert_alpha(), (40, 40))}
class BSTATS():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.buildSelected = []
        self.sprite = ""
        
bstats = BSTATS()

# testing
biomes = ["plains",
          "plains",
          "plains"]

# ACTUAL GAME
"""
biomes = ["volcano",
          "icy mountain",
          "river",
          "desert",
          "forest",
          "plains"]
"""
biomeSize = 20 # 50 #HAS TO BE ABOVE 20
worldWidth = 38 # 50 #HAS TO BE ABOVE 40
while biomeSize%4:
    biomeSize+=1
biomeSectionSize = 4


class GLOBAL_KEYS():
    def __init__(self):
        self.key = []
globalKeys = GLOBAL_KEYS()

displayTWidth = int(displayWidth/tileSize)+1
displayTHeight = int(displayWidth/tileSize)+1

tileHalfS = tileSize/2
worldHalfW = worldWidth / 2
worldAccWidth = worldWidth*tileSize
worldHAccWidth = worldAccWidth / 2
worldHeight = len(biomes)*biomeSize
worldHalfH = worldHeight / 2
worldAccHeight = worldHeight*tileSize
worldHAccHeight = worldAccHeight/2
worldSize = worldHeight*worldWidth
menu = "game"
waveAnimation = 0
gameRunning = True

closeTile = pygame.transform.scale(pygame.image.load("sprites/gui/close selected tile.png").convert_alpha(), (tileSize, tileSize))
farTile = pygame.transform.scale(pygame.image.load("sprites/gui/far selected tile.png").convert_alpha(), (tileSize, tileSize))

def wave_sprites(tiles):
    for i in range(len(tiles)):
        if tiles[i].tile == "water" or tiles[i].tile == "shore":
            rng = random.randint(0, 3)
            name = ""
            if worldHeight+1 < i < worldSize-worldHeight-1 and (i+1)%worldHeight:
                
                if not (tiles[i-1].tile == "water" or tiles[i-1].tile == "shore"): # not water top
                    name += "t "
                elif not (tiles[i-1+worldHeight].tile == "water" or tiles[i-1+worldHeight].tile == "shore"): # no water top right
                    if (tiles[i+worldHeight].tile == "water" or tiles[i+worldHeight].tile == "shore"): # water right
                        name += "tr "
                        
                if not (tiles[i+worldHeight].tile == "water" or tiles[i+worldHeight].tile == "shore"): # not water right
                    name += "r "
                elif not (tiles[i+1+worldHeight].tile == "water" or tiles[i+1+worldHeight].tile == "shore"): # no water bottom right
                    if (tiles[i+1].tile == "water" or tiles[i+1].tile == "shore"): # water bottom
                        name += "br "
                        
                if not (tiles[i+1].tile == "water" or tiles[i+1].tile == "shore"): # not water bottom
                    name += "b "
                elif not (tiles[i+1-worldHeight].tile == "water" or tiles[i+1-worldHeight].tile == "shore"): # no water bottom left
                    if (tiles[i-worldHeight].tile == "water" or tiles[i-worldHeight].tile == "shore"): # water left
                        name += "bl "
                if not (tiles[i-worldHeight].tile == "water" or tiles[i-worldHeight].tile == "shore"): # not water left
                    name += "l "
                elif not (tiles[i-1-worldHeight].tile == "water" or tiles[i-1-worldHeight].tile == "shore"): # no water top left
                    if (tiles[i-1].tile == "water" or tiles[i-1].tile == "shore"): # water top
                        name += "tl "
                
            if name != "" and name != "t r b l ":
                tiles[i].waterCons = name
                for j in range(rng):
                    tiles[i].waveSprite.append("")
                for j in range(4):
                    tiles[i].waveSprite.append(pygame.transform.scale(pygame.image.load("sprites/waves/animation "+str(j+1)+"/"+name.strip(" ")+".png"), (tileSize, tileSize)))
                for j in range(3-rng):
                    tiles[i].waveSprite.append("")

coveredTile = pygame.transform.scale(pygame.image.load("sprites/unbordered blocks/cloud/1.png"), (tileSize, tileSize))

class TILE():
    def __init__(self, x, y, tile, specTile):
        self.covered = 255
        self.size = tileSize
        self.x = x*tileSize
        self.y = y*tileSize
        self.floor = ""
        self.building = ""
        self.buildSprite = ""
        self.i = ""

        accY = y+worldHalfH
        self.biome = biomes[int(accY/biomeSize)]
        for i in range(len(biomes)):
            if biomeSize/2 < accY < worldAccHeight-biomeSize/2:
                if biomeSize*(i)-biomeSectionSize < accY < biomeSize*(i)+biomeSectionSize:
                    if accY-(biomeSize*(i)-biomeSectionSize) > random.randint(0, biomeSectionSize*2):
                        biomeIndex = i+1
                    else:
                        biomeIndex = i
                        
                    self.biome = biomes[biomeIndex-1]
        
        self.canwalk = True

        #VOLCANO
        if self.biome == "volcano":
            if tile > biomeSize:
                if specTile > -10:
                    self.tile = "magma"
                else:
                    self.tile = "lava"
            else:
                if specTile > -10:
                    self.tile = "stone"
                else:
                    self.tile = "hardened rock"
        #ICY MOUNTAIN
        if self.biome == "icy mountain":
            if tile > biomeSize*2:
                if specTile > -10:
                    self.tile = "hardened rock"
                else:
                    self.tile = "stone"
            else:
                if specTile > -10:
                    self.tile = "ice"
                else:
                    self.tile = "snow"
        #RIVER
        if self.biome == "river":
            if tile > 27:
                self.tile = "sand"
            elif tile > 12:
                self.tile = "shore"
            else:
                self.tile = "water"
        #DESERT
        if self.biome == "desert":
            if tile > 25:
                self.tile = "stone"
            elif tile > -25:
                self.tile = "sand"
            else:
                self.tile = "shore"
        self.drops = []
        #FOREST
        if self.biome == "forest":
            if tile > 40:
                self.tile = "stone"
            elif tile > -19:
                if specTile > -10 and random.randint(0, 2):
                    self.building = "tree"
                    self.canwalk = False
                    self.health = 100
                    self.col = (122, 62, 10)
                self.tile = "grass"
                    
            elif tile > -20:
                self.tile = "sand"
            elif tile > -25:
                self.tile = "shore"
            else:
                self.tile = "water"
        #PLAINS
        if self.biome == "plains":
            if tile > 30:
                self.tile = "stone"
            elif tile > -5:
                if specTile > 0 and not random.randint(0, 3):
                    self.building = "tree"
                    self.canwalk = False
                    self.health = 100
                    self.col = (122, 62, 10)
                elif not random.randint(0, 100):
                    self.drops.append("stone")
                    self.building = "pebble"
                    self.col = (89, 89, 89)
                    self.health = 2
                if specTile > -20:
                    self.tile = "grass"
                else:
                    self.tile = "dry grass"
            elif tile > -10:
                self.tile = "sand"
                if specTile > 0 and not random.randint(0, 2):
                    self.building = "pebble"
                    self.col = (89, 89, 89)
            elif tile > -15:
                self.tile = "shore"
            else:
                self.tile = "water"

        if self.building == "pebble":
            self.tag = "stone"
            self.health = 30

        if self.tile == "grass" and random.randint(0,1) and self.building == "":
            self.building = "grass"
            self.tag = "herb"
            self.health = 15
            self.col = (60, 158, 11)
        if self.tile == "dry grass" and random.randint(0,1) and self.building == "":
            self.building = "hay"
            self.tag = "herb"
            self.health = 45
            self.col = (227, 143, 41)

        if self.tile == "water":
            self.canwalk = False
        if self.building != "":
            if self.building == "tree":
                self.tag = "wood"
                self.buildSprite = []
                for i in range(11):
                    self.buildSprite.append(pygame.transform.scale(pygame.image.load("sprites/buildings/"+self.building+"/"+str(i)+".png").convert_alpha(), (self.size*2, self.size*4)))
            elif self.building == "hay":
                self.buildSprite = pygame.transform.scale(pygame.image.load("sprites/buildings/"+self.building+"/"+str(random.randint(1, 3))+".png").convert_alpha(), (self.size, self.size*2))
            else:
                self.buildSprite = pygame.transform.scale(pygame.image.load("sprites/buildings/"+self.building+"/"+str(random.randint(1, 3))+".png").convert_alpha(), (self.size, self.size))

            self.i = "tile"
        self.lightLevel = 0
        self.waterCons = ""
        
        if self.tile == "water" or self.tile == "shore":
            self.waveSprite = []
            self.waveChance = random.randint(0, 1)
        self.pregameColour = col_dict[self.tile]

        if stats.borderedTextures:
            self.sprite = pygame.transform.scale(pygame.image.load("sprites/bordered blocks/"+self.tile+"/"+str(random.randint(1,3))+".png").convert_alpha(), (self.size, self.size))
        else:
            self.sprite = pygame.transform.scale(pygame.image.load("sprites/unbordered blocks/"+self.tile+"/"+str(random.randint(1,3))+".png").convert_alpha(), (self.size, self.size))
tiles = []

col_dict = {"lava" : (230, 93, 30),
         "magma" : (145, 70, 0),
         "hardened rock" : (59, 59, 59),
         "ice" : (80, 222, 217),
         "snow" : (245, 245, 245),
         "stone" : (110, 110, 110),
         "grass" : (60, 163, 31),
         "dry grass" : (189, 142, 13),
         "sand" : (240, 218, 19),
         "shore" : (35, 102, 204),
         "water" : (12, 20, 156)}

class DROPPED_ITEM():
    def __init__(self, x, y, item, enhancements, durability):
        self.size = 32
        self.i = "item"
        self.weight = weightsdict[item]
        self.x = x
        self.y = y
        self.enhancements = enhancements
        self.durability = durability
        self.item = item
        self.goingX = random.randint(stats.itemMomentum*-1, stats.itemMomentum)
        self.goingY = random.randint(stats.itemMomentum*-1, stats.itemMomentum)
        self.sprite = pygame.transform.scale(pygame.image.load("sprites/items/"+item+".png").convert_alpha(), (self.size, self.size))
droppedItems = []

class MOUSE():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.tile = 0
        self.right = False
        self.left = False
        self.click = False
        self.release = False
        self.sprite = pygame.transform.scale(pygame.image.load("sprites/gui/cursour.png").convert_alpha(), (32, 32))
        self.selectedSlot = ""
        self.selectedHBSlot = ""
        self.offInvBeat = False
        self.offHBBeat = False
mouse = MOUSE()


class PLAYER():
    def __init__(self, tiles):
        self.i = "player"
        self.x = 0
        self.y = ((worldHeight-30)*tiles[0].size)/2+displayHalfH
        self.tile = int((self.y*-1+worldHAccHeight)/tileSize)+int((self.x+worldHAccWidth)/tileSize)*worldHeight
        self.height = 64
        self.width = self.height/2
        self.halfWidth = self.width/2
        self.fWidth = self.width/4
        self.sprite = pygame.transform.scale(pygame.image.load("sprites/player/player.png").convert_alpha(), (self.width, self.height))
        if stats.GODMODE:
            self.speed = 5
            self.maxSpeed = 20
            self.decSpeed = 5
            self.attackSpeed = 5
            self.reach = tileSize*200
        else:
            self.speed = 0.5
            self.maxSpeed = 3
            self.decSpeed = 5
            self.attackSpeed = 0.6
            self.reach = tileSize*2
        self.sprintMultiplier = 1.5
        self.xAcc = 0
        self.yAcc = 0
        self.punchTurn = 0
        self.inReach = False
        self.damage = 10
        self.inventory = []
        self.inventoryTotalItem = []
        self.inventoryTotalAmount = []
        self.hotbar = []
        self.maxWeight = 400
        self.curWeight = 0
        self.selectedSlot = ""
        self.selectedHBSlot = ""
        self.HBcycle = 7

        self.maxHealth = 5
        self.health = self.maxHealth
        self.defence = 1
        self.stamina = 100
        self.energy = self.stamina
        self.hunger = 500
        self.hydration = 500
        self.temperature = 36
 
        self.xCol_1 = int((self.y+worldHAccHeight)/tileSize)+int((self.x-self.fWidth+worldHAccWidth)/tileSize)*worldHeight
        self.xCol_2 = int((self.y+worldHAccHeight)/tileSize)+int((self.x+self.fWidth+worldHAccWidth)/tileSize)*worldHeight
        while not (tiles[self.xCol_1].canwalk and tiles[self.xCol_2].canwalk):# normal
            self.y -= 1
            self.xCol_1 = int((self.y+worldHAccHeight)/tileSize)+int((self.x-self.fWidth+worldHAccWidth)/tileSize)*worldHeight
            self.xCol_2 = int((self.y+worldHAccHeight)/tileSize)+int((self.x+self.fWidth+worldHAccWidth)/tileSize)*worldHeight            


class INVENTORY_ITEM():
    def __init__(self):
        self.item = ""
        self.tag = ""
        self.weight = 0
        self.sprite = ""
        self.amount = 0
        self.durability = 0
        self.enhancements = []

class PARTICLE():
    def __init__(self, x, y, col):
        self.goingX = random.randint(-10, 10)
        self.goingY = random.randint(-10, 10)
        self.alpha = random.randint(50, 150)
        self.col = col
        self.x = x
        self.y = y
        self.sprite = pygame.Surface((10,10))
        self.sprite.set_alpha(self.alpha)
        self.sprite.fill(col)

particles = []

class PLAYER_ARM():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.ankX = 0
        self.ankY = 0
        self.punching = 1
        self.angle = 0
        self.height = 11*2
        self.width  = 3*2
        self.offset = 5
        self.sprite = pygame.transform.scale(pygame.image.load("sprites/player/arms.png").convert_alpha(), (self.width, self.height))
        self.holdingItem = ""
        self.holdingItemSprite = ""
        self.angleANK = 0
arm = [PLAYER_ARM(), PLAYER_ARM()]

class CAMERA():
    def __init__(self):
        self.x = displayHalfW
        self.y = (worldHeight*tileSize)/2-displayHalfH
        if stats.GODMODE:
            self.smoothness = 1
        else:
            self.smoothness = 1 # usually 10000000 or something
        if stats.GODMODE:
            self.IGSmoothness = 1
        else:
            self.IGSmoothness = 1

objects = []
