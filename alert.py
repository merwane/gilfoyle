import requests
import schedule
import time
from pydub import AudioSegment
from pydub.playback import play
import os
import sys

def cls():
    os.system('cls' if os.name=='nt' else 'clear')
    print("")

cls()

coin = input("Select a cryptocurrency: BTC | BCH | ETH | LTC | ZEC ")
if coin.upper() not in ["BTC", "BCH", "ETH", "LTC", "ZEC"]:
    print("Cryptocurrency not supported.")
    exit()

cls()

value = input("Enter the price you bought your "+coin.upper()+" in USD: ")

cls()

print("Worker launched, you can leave it in background.")

BELLOW = float(value)

song = AudioSegment.from_mp3('suffer.mp3')

inc = 1

def req_price():
    r = requests.get('https://api.coinbase.com/v2/exchange-rates?currency='+coin.upper())
    return float(r.json()['data']['rates']['USD'])

def alert(price):
    if price < float(BELLOW):
        # mac notification
        if sys.platform == 'darwin':
            os.system("""
                    osascript -e 'display notification "{}" with title "{}"'
                    """.format("Current price: $"+str(price), coin.upper()+" price dropped bellow $"+str(BELLOW)))
        play(song)

def main():
    global inc

    if inc == 1:
        alert(req_price())
        inc += 1

    if float(BELLOW) < req_price():
        inc -= 1

schedule.every(30).seconds.do(main)

while True:
    schedule.run_pending()
    time.sleep(1)
