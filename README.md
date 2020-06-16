
# Mitä tänään juotaisiin                                   

Find the cheapest drinks from Alko

## Usage

* Download dependencies:
```
pip install openpyxl
pip install requests
```
* Run main.py

  * Script will download an excel sheet of prices from the Alko website
  * Type **search_drinks** to find the cheapest drinks
  * Type **help** for all commands

* Example session:
```
>>> search_stores kajaani
1: Alko Kajaani Prisma, KAJAANI, 87100
2: Alko Kajaani keskusta Citymarket, KAJAANI, 87100

>>> select_store 1
Selected: Alko Kajaani Prisma, KAJAANI, 87100

>>> search_drinks
1: Gambina muovipullo
--- https://alko.fi/tuotteet/319027/
--- Price per 1 liter of 100% alcohol: 63.43€
--- Price: 9.99€    Size: 0.75l    Alcohol-%: 21.0%
--- Category: Jälkiruokaviinit, väkevöidyt ja muut viinit
--- Alko Kajaani Prisma: 11-15

```

**When stores are selected, stock for each drink is checked by scraping the Alko website. It is slow and can cause errors. If it fails, don't choose any stores**

**If you work at Alko, please create a public API for this stuff**
