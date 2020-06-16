import requests
import json

class Store:
    def __init__(self, name, city, postalCode, storeID):
        self.name = name
        self.city = city
        self.postalCode = postalCode
        self.storeID = storeID

    def __str__(self):
        return self.name + ", " + self.city + ", " + self.postalCode

    __repr__ = __str__
# --- END OF STORE ---

class StoreList:
    loadSuccess = False
    stores = []

    def __init__(self, storeURL):
        response = requests.get(storeURL)
        if response.status_code != 200:
            return
        
        storesJSON = json.loads(response.text)["stores"]

        for store in storesJSON:
            name = store["name"]
            city = store["city"]
            postalCode = store["postalCode"]
            storeID = store["storeId"]
            outletType = store["outletTypeId"]
            if outletType == "outletType_myymalat": #Ignore tilauspalvelupisteet
                self.stores.append(Store(name, city, postalCode, storeID))
        
        self.loadSuccess = True

    def FindStoresByName(self, storeName):
        foundStores = []

        for s in self.stores:
            if storeName.lower() in s.name.lower():
                foundStores.append(s)

        return foundStores
    
    def FindStoresByCity(self, cityName):
        foundStores = []

        for s in self.stores:
            if s.city == cityName.upper():
                foundStores.append(s)

        return foundStores
    
    def FindStoresByPostalCode(self, postalCode):
        foundStores = []

        for s in self.stores:
            if s.postalCode == postalCode:
                foundStores.append(s)

        return foundStores

# --- END OF STORELIST ---

def SelectStores():
    stores = StoreList("https://www.alko.fi/INTERSHOP/web/WFS/Alko-OnlineShop-Site/fi_FI/-/EUR/ALKO_ViewStoreLocator-StoresJSON")
    if not stores.loadSuccess:
        print("Loading stores failed")
        return
    
    print("Search for stores. Type help for all the commands.")

    selectedStores = []

    while True:
        command = input("\n>>> ")

        if command == "help":
            PrintHelp()
        elif "search_by_name" in command:
            name = command.replace("search_by_name", "").strip()
            foundStores = stores.FindStoresByName(name)
            PrintStores(foundStores)
        elif "search_by_city" in command:
            city = command.replace("search_by_city", "").strip()
            foundStores = stores.FindStoresByCity(city)
            PrintStores(foundStores)
        elif "search_by_postal_code" in command:
            postCode = command.replace("search_by_postal_code", "").strip()
            foundStores = stores.FindStoresByPostalCode(postCode)
            PrintStores(foundStores)
        elif command.find("select") == 0:
            try:
                selection = command.replace("select", "").strip()
                selectionInt = int(selection) - 1
                if selectionInt < len(foundStores) and selectionInt >= 0:
                    store = foundStores[selectionInt]
                    if store not in selectedStores:
                        print("Selected: " + str(store))
                        selectedStores.append(store)
                    else:
                        print("Store already selected")
            except:
                print("Selection failed! Try searching and then select <number>")
        elif command == "show_selected":
            print("Selected stores:")
            PrintStores(selectedStores)
        elif command == "clear_selected":
            print("Clearing selected stores")
            selectedStores.clear()
        elif command == "exit":
            return selectedStores

def PrintHelp():
    print("Commands: ")
    print("\tsearch_by_name <name>")
    print("\tsearch_by_city <city>")
    print("\tsearch_by_postal_code <postal_code>")
    print("\tselect <number>")
    print("\tshow_selected")
    print("\tclear_selected")
    print("\texit")

def PrintStores(stores):
    if len(stores) > 0:
        for i in range(0, len(stores)):
            print(str(i+1) + ": " + str(stores[i]))
    else:
        print("No stores found")


def Test():
    selected = SelectStores()

    PrintStores(selected)

   

if __name__ == "__main__":
    Test()