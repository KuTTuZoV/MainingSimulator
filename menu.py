import json
import requests

class menu:
    structure  = None
    parentNode = None

    currentLayer = None
    parent = list()

    def __init__(self):
        self.structure = json.loads(open("menu",encoding="utf-8-sig").read())
        self.currentLayer = self.structure

        self.structure["Магазин"] = json.loads(open("assortment",encoding="utf-8-sig").read())

    def assortment(self):

        assortment = list()

        for item in self.structure["Магазин"]:
            assortment.append(item)

        return assortment

    def showCurrentLayer(self):
        menuItems = list()

        for item in self.currentLayer:
            menuItems.append(item)

        if len(self.parent) != 0:
            menuItems.append("<-Назад")

        return menuItems

    def backToParent(self):
        self.currentLayer = self.parent[0]
        self.parent.pop(0)

    def selectMenuItem(self, menuItem):
        try:
            self.parent.insert(0, self.currentLayer)
            self.currentLayer = self.currentLayer[menuItem]
            return True
        except:
            return False

# menu = menu()
#
# while(1):
#
#     menuItems = menu.showCurrentLayer()
#     print(menuItems)
#     a = int(input())
#
#     if a == (len(menuItems) - 1):
#         menu.backToParent()
#     else:
#         menu.selectMenuItem(menuItems[a])