from Drinks import (Drink, DrinkList, PrintResults)
from Stores import (Store, StoreList, SelectStores)

def PrintBanner():
    file = open("banner.txt", "r")
    text = file.read()
    print(text)
    file.close()


def main():
    # Load and parse excel sheet of prices
    drinkList = DrinkList("alkon-hinnasto-tekstitiedostona.xlsx")
    if not drinkList.loadSuccess:
        print("parsing excel sheet failed")
        return

    # Fetch and parse json of alko stores
    stores = StoreList("https://www.alko.fi/INTERSHOP/web/WFS/Alko-OnlineShop-Site/fi_FI/-/EUR/ALKO_ViewStoreLocator-StoresJSON")
    if not stores.loadSuccess:
        print("Loading stores failed")
        return
    
    print("Loading complete! ^- Ignore that warning\n")

    PrintBanner()
    print("Type search_drinks to find the cheapest drinks!\nFor all commands type help.")

    selectedStores = []
    selectedCategories = []

    while True:
        command = input("\n>>> ")

        if command == "help":
            PrintHelp()

        elif "search_stores" in command:
            searchTerm = command.replace("search_stores", "").strip()
            
            storesByName = stores.FindStoresByName(searchTerm)
            storesByCity = stores.FindStoresByCity(searchTerm)
            storesByPC = stores.FindStoresByPostalCode(searchTerm)

            foundStores = storesByName
            for s in storesByCity:
                if s not in foundStores:
                    foundStores.append(s)            
            for s in storesByPC:
                if s not in foundStores:
                    foundStores.append(s)            

            PrintStores(foundStores)

        elif command.find("select_store") == 0:
            try:
                selection = command.replace("select_store", "").strip()
                selectionInt = int(selection) - 1
                if selectionInt < len(foundStores) and selectionInt >= 0:
                    store = foundStores[selectionInt]
                    if store not in selectedStores:
                        print("Selected: " + str(store))
                        selectedStores.append(store)
                    else:
                        print("Store already selected")
                else:
                    print("Can't select with that index")
            except:
                print("Selection failed! Try searching and then select_store <number>")
        
        elif command == "show_selections":
            print("Selected stores:")
            PrintStores(selectedStores)
            print("\nSelected categories:")
            if len(selectedCategories) == 0:
                print("No categories selected. Search all.")
            else:
                for c in selectedCategories:
                    print("- " + c)

        elif command == "clear_stores":
            print("Clearing selected stores")
            selectedStores.clear()

        elif command == "list_categories":
            drinkList.PrintCategories()

        elif "select_category" in command:
            try:
                selection = command.replace("select_category", "").strip()
                selectionInt = int(selection) - 1
                if selectionInt < len(drinkList.categories) and selectionInt >= 0:
                    category = drinkList.categories[selectionInt]
                    if category not in selectedCategories:
                        print("Selected: " + category)
                        selectedCategories.append(category)
                    else:
                        print("Category already selected")
                else:
                    print("Can't select with that index")
            except:
                print("Selection failed! Try list_categories and then select_category <number>")

        elif command == "clear_categories":
            print("Clearing selected categories")
            selectedCategories.clear()

        elif command == "search_drinks":
            results = drinkList.GetBestDrinks(selectedStores, selectedCategories)
            PrintResults(results)

        elif command == "exit":
            print("Bye bye!")
            exit()

def PrintHelp():
    print("Commands: ")
    
    print("\tsearch_stores <name/city/postal_code>")
    print("\t - Searches from all alko stores. After searching use select_store <number> to select stores.")
    
    print("\n\tselect_store <number>")
    print("\t - Select stores using numbers from latest store search.")
    print("\t - Can be used multiple times, eg.")
    print("\t - >>> select_store 1")
    print("\t - >>> select_store 2")
    
    print("\n\tshow_selections")
    print("\t - Shows selected stores and categories")

    print("\n\tclear_stores")
    
    print("\n\tlist_categories")
    print("\t - Show all possible drink categories")
    
    print("\n\tselect_category <number>")
    print("\t - Select category using numbers from list_categories")

    print("\n\tclear_categories")

    print("\n\tsearch_drinks")
    print("\t - Searches for the cheapest drinks based on price for one liter of pure alcohol")
    print("\t - If you have selected one or more categories, only those will be shown, otherwise it shows all drinks")
    print("\t - If one or more stores are selected, only drinks available in selected stores will be shown.")
    print("\t - (Availability check is little slow because there isn't any proper API to check for it)")

    print("\n\texit")
    print("\t - Cheapest drinks have been found. Alkoon mars!")

def PrintStores(stores):
    if len(stores) > 0:
        for i in range(0, len(stores)):
            print(str(i+1) + ": " + str(stores[i]))
    else:
        print("No stores found")



if __name__ == "__main__":
    main()