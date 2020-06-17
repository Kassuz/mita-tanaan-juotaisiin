import requests
import json
import openpyxl
from time import sleep

from AvailabilityParser import AvailabilityParser
from Stores import (Store, StoreList, SelectStores)
from DownloadPrices import DownloadPrices

# Yeah its a global variable
errors = 0

class Drink:
    def __init__(self, drinkID, name, volume, price, pricePerLiter, category, alcohol, pricePerAlcoholLiter):
        self.drinkID = drinkID
        self.name = name
        self.volume = volume
        self.price = price
        self.pricePerLiter = pricePerLiter
        self.category = category
        self.alcohol = alcohol
        self.pricePerAlcoholLiter = pricePerAlcoholLiter

    def __str__(self):
        return self.name + ", " + str(self.volume) + "l, " + str(self.price) + "€"
    __repr__ = __str__

# --- END OF DRINK ---

def GetDrinkData(sheet, row):
    drinkID = sheet["A" + str(row)].value
    name = sheet["B" + str(row)].value
    volume = float(sheet["D" + str(row)].value.split()[0].replace(',', '.'))
    price = float(sheet["E" + str(row)].value)
    pricePerLiter = float(sheet["F" + str(row)].value)
    category = sheet["I" + str(row)].value
    alcohol = float(sheet["V" + str(row)].value) / 100.0
    return drinkID, name, volume, price, pricePerLiter, category, alcohol

class DrinkList:
    drinks = []
    categories = []
    loadSuccess = False

    def __init__(self, exelName):
        DownloadPrices()

        try:
            workbook = openpyxl.load_workbook(exelName)
            sheet = workbook["Alkon Hinnasto Tekstitiedostona"]
        except:
            print("Loading prices exel sheet failed! Exiting...")
            exit(1)
        
        self.title = sheet["A1"].value
        for row in range(5, sheet.max_row):
            try:
                drinkID, name, volume, price, pricePerLiter, category, alcohol = GetDrinkData(sheet, row)
            except:
               continue
                
            if alcohol == 0.0:
                continue

            if not category:
                category = "uncategorized"

            alcoholPerBottle = volume * alcohol
            pricePerAlcoholLiter = round(price / alcoholPerBottle, 2)

            self.drinks.append(Drink(drinkID, name, volume, price, pricePerLiter, category, alcohol, pricePerAlcoholLiter))
            if category not in self.categories:
                self.categories.append(category)
        self.loadSuccess = True
    # --- END OF __INIT__ ---

    def GetBestDrinks(self, selectedStores, selecetedCategories, amount = 10):
        global errors
        errors = 0
        
        if not self.loadSuccess:
            print("Can't sort drinks because loading failed")
            return []
        
        sortedDrinks = []
        for drink in self.drinks:
            if drink.category in selecetedCategories or len(selecetedCategories) == 0:
                sortedDrinks.append(drink)
        sortedDrinks.sort(key=lambda d: d.pricePerAlcoholLiter)

        bestDrinks = []
        for drink in sortedDrinks:
            if len(selectedStores) == 0:
                bestDrinks.append(drink)
            else:
                stocks = GetStockInStores(drink, selectedStores)
                if len(stocks) > 0:
                    bestDrinks.append((drink, stocks))

            if len(bestDrinks) == amount:
                break

        if errors > 0:
            print("\n" + str(errors) + " error(s) when fetching stock data :(\n")

        return bestDrinks
    # --- END OF GETBESTDRINKS ---
    
    def PrintCategories(self):
        print("Drink categories:")
        for i in range(0, len(self.categories)):
            print(str(i+1) + ": " + self.categories[i].capitalize())
    # --- END OF PRINTCATEGORIES ---
# --- END OF DRINKLIST ---


def GetStockInStores(drink, selectedStores):
    # Not really an api and requests sometimes fail. Try 10 times and if still fails, move on
    global errors
    success = False
    for i in range(0, 10):
        # Shitty error handling. If we get over 10 errors just quit
        if errors > 10:
            print("\n!!! Too many errors fetching stock data !!!")
            print("Maybe alko broke something? Try without selecting stores next time or just try again ¯\\_(ツ)_/¯")
            print("Exiting ...")
            exit()
        
        try:
            sleep(1) # Let's sleep a little
            headers = {"Cache-Control": "max-age=0"} #Seems to create less errors
            url = "https://www.alko.fi/INTERSHOP/web/WFS/Alko-OnlineShop-Site/fi_FI/-/EUR/ViewProduct-Include?SKU="
            response = requests.get(url + drink.drinkID, headers=headers)

            if response.status_code == 200:
                success = True
                break
            elif int(response.status_code / 100) == 4:
                print("\nError fetching stock for " + drink.name + ". Skipping...")
                print(">>> Response code: " + response.status_code)
                errors += 1               
                return []
            elif int(response.status_code / 100) == 5:
                print("\nServer error fetching stock for " + drink.name + ". Skipping...")
                print(">>> Response code: " + str(response.status_code))
                errors += 1             
                return []
        except:
            # errors += 1
            continue

    if not success:
        print("Fetching stock data for " + drink.name + " failed. Alko plz tee api")
        return []

    parser = AvailabilityParser()
    parser.feed(response.text)

    stocks = json.loads(parser.jsonData)

    storeStocks = []
    for s in stocks:
        storeID = s["storeId"]
        for store in selectedStores:
            if storeID == store.storeID:
                storeStocks.append((store, s["stock"]))
    return storeStocks

def PrintResults(res):
    print("")
    if len(res) == 0:
        print("No drinks found")
        return

    for i in range(0, len(res)):
        if type(res[0]) is tuple:
            drink : Drink = res[i][0]
        else:
            drink = res[i]

        print(str(i+1) + ": " + drink.name)
        print("--- https://alko.fi/tuotteet/" + drink.drinkID + "/")
        print("--- Price per 1 liter of pure alcohol: " + str(drink.pricePerAlcoholLiter) + "€")
        print("--- Price: " + str(drink.price) + "€    Size: " + str(drink.volume) + "l    Alcohol: " + str(round(drink.alcohol * 100, 1)) + "%")
        print("--- Category: " + drink.category.capitalize())
        
        if type(res[0]) is tuple:
            print("--- In Stock:")
            stocks = res[i][1]
            for s in stocks:
                store = s[0]
                stock = s[1]
                print("----- " + store.name + ": " + stock)
        print("\n")

