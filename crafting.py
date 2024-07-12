import pygame
class CITEM():
    def __init__(self, itemout, tag, amount, recipies):
        self.sprite = pygame.transform.scale(pygame.image.load("sprites/items/"+itemout+".png"), (64, 64))
        self.bigSprite = pygame.transform.scale(pygame.image.load("sprites/items/"+itemout+".png"), (128, 128))
        self.item = itemout
        self.amountOut = amount
        self.itemIn = []
        self.amountIn = []
        self.itemInSprite = []
        self.tag = tag
        for i in range(len(recipies)):
            self.itemIn.append(recipies[i][0])
            self.itemInSprite.append(pygame.transform.scale(pygame.image.load("sprites/items/"+recipies[i][0]+".png"), (64, 64)))
            self.amountIn.append(recipies[i][1])

crafts = [
    # materials
    [CITEM("rope", "resource", 1, [("grass", 5), ("hay", 1)]),
     CITEM("hay", "resource", 1, [("grass", 4)]),
     CITEM("refined wood", "resource", 1, [("wood", 5), ("hay", 1)])
     ],
    # tools
    [CITEM("stone axe", "tool", 1, [("stone", 5), ("rope", 3), ("grass", 10), ("wood", 10)]),
     CITEM("stone pickaxe", "tool", 1, [("stone", 7), ("rope", 3), ("grass", 10), ("wood", 15)]),
     CITEM("stone scythe", "tool", 1, [("stone", 10), ("rope", 3), ("grass", 7), ("wood", 15)]),
     CITEM("stone sword", "tool", 1, [("stone", 15), ("rope", 5), ("grass", 12), ("wood", 5)]),
     CITEM("wood hammer", "tool", 1, [("stone", 2), ("rope", 3), ("wood", 7), ("refined wood", 3)])
     ],
    # armour
    [
    ],
    # special
    [
    ]
    ]

craftedItemDurability = {"wood" : 25,
                         "stone" : 50,
                         "iron" : 100,
                         "steel" : 150,
                         "gold" : 250,
                         "titanium" : 400,
                         "bloktanium" : 900}

dropsDict = {"tree" : [["wood", 200, 500]],
             "grass" : [["grass", 200, 300]],
             "hay" : [["hay", 100, 200]],
             "pebble" : [["stone", 100, 100]]}

weightsdict = {"wood"  : 2,
               "stone" : 5,
               "grass" : 0.25,
               "hay"   : 1,
               "rope"  : 5,
               "refined wood"  : 10,
               "stone axe": 10,
               "stone pickaxe": 10,
               "stone scythe": 10,
               "stone sword": 10,
               "wood hammer": 10}

itemDamages = [["", "stone", 10],
               ["", "herb", 10],
               ["", "wood", 3],
               ["stone", "wood", 10],
               ["stone", "herb", 10],
               ["stone", "stone", 10],
               ["stone axe", "wood", 15],
               ["stone pickaxe", "stone", 10],
               ["stone scythe", "herb", 100],
               ["stone sword", "entity", 100],
               ]

buildingResources = {"floor" : 1,
                     "wall" : 3,
                     "door" : 4}

buildingHealths = {"tree" : 100,
                   "pebble" : 30,
                   "grass" : 30,
                   "hay"  : 50,
                   "wood floor" : 15,
                   "wood wall" : 30,
                   "wood door" : 30,
                   "stone floor" : 45,
                   "stone wall" : 60,
                   "stone door" : 60,
                   "hay floor" : 10,
                   "hay wall" : 25,
                   "hay door" : 25}

buildingTags = {"wood" : "wood",
                "stone" : "stone",
                "hay" : "herb"}


