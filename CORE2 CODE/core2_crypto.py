from m5stack import *
from m5stack_ui import *
from uiflow import *
import wifiCfg
import urequests
import time
import json

# úvodní setup
screen = M5Screen()
screen.clean_screen()
screen.set_screen_bg_color(0xffffff)

# -----------------------------------------------------------------------------------

# Zde nastavte údaje k wifi
# Ještě musíte nahrát jednotlivé .png ikonky kryptoměn do m5stacku přes uiflow

SSID = 'm5stackcrypto'
PASSWORD = 'getcryptoprice'

# -----------------------------------------------------------------------------------

# index 0 = Bitcoin, nastavení intenziy vibrací tlačítek
crypto_index = 0
power.setVibrationIntensity(10)

# -----------------------------------------------------------------------------------

# umístění jednotlivých grafických prvků

grey_background = M5Line(x1=0, y1=223, x2=320, y2=223, color=0xcfcfcf, width=36, parent=None)

left_arrow = M5Label('<', x=42, y=203, color=0x7a7979, font=FONT_MONT_32, parent=None)
right_arrow = M5Label('>', x=252, y=203, color=0x7a7979, font=FONT_MONT_32, parent=None)
bottom_crypto_label = M5Label('BTC', x=136, y=208, color=0x7a7979, font=FONT_MONT_24, parent=None)
label_border = M5Line(x1=0, y1=204, x2=320, y2=204, color=0x000, width=2, parent=None)

wifi_label_indicator = M5Line(x1=303, y1=190, x2=311, y2=190, color=0xff0000, width=6, parent=None)
wi_fi_label = M5Label('wi-fi', x=266, y=182, color=0x000, font=FONT_MONT_14, parent=None)

crypto_image_icon = M5Img("res/BTC.png", x=19, y=98, parent=None)
crypto_name = M5Label('Bitcoin (BTC)', x=94, y=122, color=0x000, font=FONT_MONT_14, parent=None)

crypto_price = M5Label('???: ?????$', x=15, y=20, color=0x7a7979, font=FONT_MONT_32, parent=None)
crypto_price_underline = M5Line(x1=-8, y1=70, x2=210, y2=70, color=0x000, width=2, parent=None)

crypto_color_line = M5Line(x1=0, y1=10, x2=320, y2=10, color=0xf7931a, width=2, parent=None)

# -----------------------------------------------------------------------------------

# list možných kryptoměn
crypto_list = ["BTC", "ETH", "LTC", "XMR", "ADA", "SOL", "DOGE", "XRP", "DOT", "XLM"]

# barvy vhodné k jednotlivým krytpoměnám
crypto_color_dict = {
  "BTC": 0xf7931a,
  "ETH": 0x343535,
  "LTC": 0x345d9d,
  "XMR": 0xfa6800,
  "ADA": 0x0133ae,
  "SOL": 0x9766e3,
  "DOGE": 0xba9f33,
  "XRP": 0x23292f,
  "DOT": 0x060606,
  "XLM": 0x000000
}

# dlouhé jména jednotlivých kryptoměn
crypto_name_dict = {
  "BTC": "Bitcoin (BTC)",
  "ETH": "Ethereum (ETH)",
  "LTC": "Litecoin (LTC)",
  "XMR": "Monero (XMR)",
  "ADA": "Cardano (ADA)",
  "SOL": "Solana (SOL)",
  "DOGE": "Dogecoin (DOGE)",
  "XRP": "Ripple (XRP)",
  "DOT": "Polkadot (DOT)",
  "XLM": "Stellar (XLM)"
}

# -------------------------------------------------------------------------

def get_currency(coinTicker):
  global crypto_price
  try:
    # získá cenu z API se zadanou měnou, vyčte JSON data z odpovědi API
    response = urequests.get('https://api.coinbase.com/v2/exchange-rates?currency=' + coinTicker)
    output = json.loads((response.text))
    
    # získá cenu v USD a uloží do proměnné
    price_string = output['data']['rates']['USD']

    # získá krátkou značku měny
    currency_string = output['data']['currency']
    
    # zaokrouhlení ceny na 2 desetiná místa a následné převedení na text
    rounded_price_string = str(round(float(price_string), 2))
    
    # finální, pěkně formátovaný text ceny -> "BTC: 45000$"
    final_currency_ticker_and_price = currency_string + ":" + " " + rounded_price_string + "$"
    
    # nastavení textu ceny kryptoměny na formátovaný text
    crypto_price.set_text(final_currency_ticker_and_price)
  
  except OSError:
    pass

# -------------------------------------------------------------------------

# funkce která zpustí vibrace na 100ms
def vibrate_button():
  power.setVibrationEnable(True)
  wait_ms(100)
  power.setVibrationEnable(False)

# -------------------------------------------------------------------------

def change_selected_crypto(factor):
  global crypto_index

  # pokud jdeme za poslední možnou měnu, vrátit se na začátek
  if crypto_index > len(crypto_list) - 1:
    crypto_index = 0
    factor = 0

  # pokud dojdeme za začátek, vrátit se na konec
  elif crypto_index < -len(crypto_list):
    crypto_index = -1
    factor = -1

  # vybereme novou kryptoměnu z listu dostupných
  new_crypto = crypto_list[factor]
  
  # změnímě příslušné ikonky, texty a barvy na novou kryptoměnu
  crypto_image_icon.set_img_src("res/" + new_crypto + ".png")
  crypto_name.set_text(crypto_name_dict[new_crypto])
  crypto_color_line.set_color(crypto_color_dict[new_crypto])
  bottom_crypto_label.set_text(new_crypto)

# -------------------------------------------------------------------------

# umožní upravit barvy textu, aby jsme mohli naznačit že m5stack pracuje a načítá novou cenu
def change_color(color):
  left_arrow.set_text_color(color)
  right_arrow.set_text_color(color)
  bottom_crypto_label.set_text_color(color)
  crypto_price.set_text_color(color)

# -------------------------------------------------------------------------
# -------------------------------------------------------------------------

# cykl který využívá předešlé funkce
while True:

  # pokud je wifi napojena nastaví wifi indikátor na zelenou
  if wifiCfg.wlan_sta.isconnected():
    wifi_label_indicator.set_color(0x00ff00)
    change_color(0x000)
  # pokud není wifi napojena nastaví wifi indikátor na červenou a pokusí je připojit na wifi
  else:
    wifi_label_indicator.set_color(0xff0000)
    change_color(0x7a7979)
    wifiCfg.doConnect(SSID, PASSWORD)

  # první tlačítko nás posune o 1 index zpět
  if btnA.isPressed():
    vibrate_button()
    crypto_index -= 1
    change_selected_crypto(crypto_index)

  # prostřední tlačitko aktualizuje kryptoměnu, využitím předešlých funkcí
  if btnB.isPressed():
    vibrate_button()
    change_color(0x7a7979)
    get_currency(crypto_list[crypto_index])
    change_color(0x000)

  # třetí tlačítko nás posune o 1 index dopředu
  if btnC.isPressed():
    vibrate_button()
    crypto_index += 1
    change_selected_crypto(crypto_index)

  wait_ms(2)
