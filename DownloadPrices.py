import requests
import os.path
import openpyxl
import datetime


def DownloadPrices():
    filename = "alkon-hinnasto-tekstitiedostona.xlsx"

    downloadFile = True
    if os.path.isfile(filename):
        timestamp = os.path.getmtime(filename)
        date = datetime.datetime.fromtimestamp(timestamp).date()
        now = datetime.datetime.now().date()
        
        if now.toordinal() - date.toordinal() == 0:
            downloadFile = False

    if downloadFile:
        print("Downloading latest prices...")

        response = requests.get("https://www.alko.fi/INTERSHOP/static/WFS/Alko-OnlineShop-Site/-/Alko-OnlineShop/fi_FI/Alkon%20Hinnasto%20Tekstitiedostona/alkon-hinnasto-tekstitiedostona.xlsx")

        if response.status_code == 200:
            print(len(response.content))
            f = open(filename, "wb")
            f.write(response.content)
            print("Download completed")
        else:
            print("Request failed")
            return False

    return True