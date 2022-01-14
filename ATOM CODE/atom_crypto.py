from m5stack import *
from m5ui import *
from uiflow import *
import wifiCfg
import urequests
import time
import json

rgb.set_screen([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])

# sem zadejte údaje k wifi hotspotu/routeru
wifiCfg.doConnect('SSID', 'PASSWORD')

# pokud jsou údaje správné a wifi dostupná, měl by se m5stack připojit hned po spuštění programu

# ---------------------------------------------------------------------------------------

def movingText(text, delay, color):     # definování funkce
  
  symbol_dictionary = {           # kolekce jednotlivých znaků, každý znak je rozdělen na 5 listů, každý list reprezentuje jeden řádek LED na m5stacku
    
    'a': [[0,color,color,0,0],[color,0,0,color,0],[color,color,color,color,0],[color,0,0,color,0],[color,0,0,color,0]],
    'b': [[color,color,color,0,0],[color,0,0,color,0],[color,color,color,color,0],[color,0,0,color,0],[color,color,color,0,0]],
    'c': [[0,color,color,color,0],[color,0,0,0,0],[color,0,0,0,0],[color,0,0,0,0],[0,color,color,color,0]],
    'd': [[color,color,color,0,0],[color,0,0,color,0],[color,0,0,color,0],[color,0,0,color,0],[color,color,color,0,0]],
    'e': [[color,color,color,color,0],[color,0,0,0,0],[color,color,color,0,0],[color,0,0,0,0],[color,color,color,color,0]],
    'f': [[color,color,color,color,0],[color,0,0,0,0],[color,color,color,color,0],[color,0,0,0,0],[color,0,0,0,0]],
    'g': [[0,color,color,0,0],[color,0,0,0,0],[color,0,color,color,0],[color,0,0,color,0],[0,color,color,0,0]],
    'h': [[color,0,0,color,0],[color,0,0,color,0],[color,color,color,color,0],[color,0,0,color,0],[color,0,0,color,0]],
    'i': [[color,color,color,color,0],[0,color,0,0,0],[0,color,0,0,0],[0,color,0,0,0],[color,color,color,color,0]],
    'j': [[0,0,0,color,0],[0,0,0,color,0],[0,0,0,color,0],[color,0,0,color,0],[0,color,color,0,0]],
    'k': [[color,0,0,color,0],[color,0,color,0,0],[color,color,0,0,0],[color,0,color,0,0],[color,0,0,color,0]],
    'l': [[color,0,0,0,0],[color,0,0,0,0],[color,0,0,0,0],[color,0,0,0,0],[color,color,color,color,0]],
    'm': [[color,0,0,color,0],[color,color,color,color,0],[color,0,0,color,0],[color,0,0,color,0],[color,0,0,color,0]],
    'n': [[color,0,0,color,0],[color,color,0,color,0],[color,0,color,color,0],[color,0,0,color,0],[color,0,0,color,0]],
    'o': [[0,color,color,0,0],[color,0,0,color,0],[color,0,0,color,0],[color,0,0,color,0],[0,color,color,0,0]],
    'p': [[color,color,color,0,0],[color,0,0,color,0],[color,color,color,0,0],[color,0,0,0,0],[color,0,0,0,0]],
    'q': [[0,color,color,0,0],[color,0,0,color,0],[color,0,0,color,0],[0,color,color,color,0],[0,0,0,color,0]],
    'r': [[color,color,color,0,0],[color,0,0,color,0],[color,color,color,0,0],[color,0,color,0,0],[color,0,0,color,0]],
    's': [[0,color,color,color,0],[color,0,0,0,0],[0,color,color,0,0],[0,0,0,color,0],[color,color,color,0,0]],
    't': [[color,color,color,color,0],[0,color,0,0,0],[0,color,0,0,0],[0,color,0,0,0],[0,color,0,0,0]],
    'u': [[color,0,0,color,0],[color,0,0,color,0],[color,0,0,color,0],[color,0,0,color,0],[0,color,color,0,0]],
    'v': [[color,0,0,color,0],[color,0,0,color,0],[0,color,0,color,0],[0,color,0,color,0],[0,0,color,0,0]],
    'w': [[color,0,0,color,0],[color,0,0,color,0],[color,0,0,color,0],[color,color,color,color,0],[color,0,0,color,0]],
    'x': [[color,0,0,color,0],[color,0,0,color,0],[0,color,color,0,0],[color,0,0,color,0],[color,0,0,color,0]],
    'y': [[color,0,0,color,0],[color,0,0,color,0],[color,0,0,color,0],[0,color,color,0,0],[0,0,color,0,0]],
    'z': [[color,color,color,color,0],[0,0,0,color,0],[0,color,color,0,0],[color,0,0,0,0],[color,color,color,color,0]],
    '0': [[0,color,color,color,0],[0,color,0,color,0],[0,color,0,color,0],[0,color,0,color,0],[0,color,color,color,0]],
    '1': [[0,0,color,0,0],[0,color,color,0,0],[0,0,color,0,0],[0,0,color,0,0],[0,0,color,0,0]],
    '2': [[0,color,color,color,0],[0,0,0,color,0],[0,color,color,color,0],[0,color,0,0,0],[0,color,color,color,0]],
    '3': [[0,color,color,color,0],[0,0,0,color,0],[0,color,color,color,0],[0,0,0,color,0],[0,color,color,color,0]],
    '4': [[0,color,0,color,0],[0,color,0,color,0],[0,color,color,color,0],[0,0,0,color,0],[0,0,0,color,0]],
    '5': [[0,color,color,color,0],[0,color,0,0,0],[0,color,color,color,0],[0,0,0,color,0],[0,color,color,color,0]],
    '6': [[0,color,color,color,0],[0,color,0,0,0],[0,color,color,color,0],[0,color,0,color,0],[0,color,color,color,0]],
    '7': [[0,color,color,color,0],[0,0,0,color,0],[0,0,0,color,0],[0,0,0,color,0],[0,0,0,color,0]],
    '8': [[0,color,color,color,0],[0,color,0,color,0],[0,color,color,color,0],[0,color,0,color,0],[0,color,color,color,0]],
    '9': [[0,color,color,color,0],[0,color,0,color,0],[0,color,color,color,0],[0,0,0,color,0],[0,color,color,color,0]],
    ' ': [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]
  }

  # utvoření proměnné z textu vloženého do funkce a převedení textu do malých písmen, kdyby bylo do funkce vloženo velké písmeno aby poté šlo vyhledat v kolekci
  screen_output = text.lower() 
  
  # utvoření 5 prázdných listů, 1 pro každý řádek LED na m5stacku
  first_line, second_line, third_line, fourth_line, fifth_line = [0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0]
  
  # pro každé písmeno v textu zadaném do funkce, najde písmeno v kolekci a přířadí listu "first_line" první řádek led ze zadaného písmena, poté druhému listu druhý řádek led ze zadaného písmena, atd.
  for symbol in screen_output:                       
    first_line += symbol_dictionary[symbol][0]
    second_line += symbol_dictionary[symbol][1] 
    third_line += symbol_dictionary[symbol][2]
    fourth_line += symbol_dictionary[symbol][3]
    fifth_line += symbol_dictionary[symbol][4]
  
  # přidání prázdných řádku, aby mohl text na LED displayi "odjet" mimo naši vizi
  first_line += [0,0,0,0,0,0,0,0,0]
  second_line += [0,0,0,0,0,0,0,0,0]
  third_line += [0,0,0,0,0,0,0,0,0]
  fourth_line += [0,0,0,0,0,0,0,0,0]
  fifth_line += [0,0,0,0,0,0,0,0,0]
  
  i = 0
  while True:
    # nastavení LED na m5stacku na první písmeno proto "i až i+5", to je při prvním průchodu cyklem rovno 0 až 5, při dalším průchodu 1 až 6 etc.
    rgb.set_screen(first_line[i:i+5]+second_line[i:i+5]+third_line[i:i+5]+fourth_line[i:i+5]+fifth_line[i:i+5])
    
    wait(delay) # čekat, v sekundách vložené do funkce
    i += 1 # inkrementace i .. neboli posutnutí LED při příštím průchodu cyklem
    
    # pokud je i větší než "délka_textu * 5 + 10" cykl se přeruší. délka textu se násobí se 5, kvůli 5 LED širokému displayi na m5stacku, aby mělo každé písmeno 5 cyklů neboli dost času aby jsme viděli celé písmeno přejet led display
    # přičítá se 10 kvůli prvním 5 a posledním 5 prázdným LED listům 
    if i > len(screen_output) * 5 + 10:
      break

# ---------------------------------------------------------------------------------------

def getCurrency(coinTicker):
  try:

    # získa odpověď API, nastaví LED na zeleno že byla komunikace úspěšná, uloží odpověď do proměnnné
    response = urequests.get('https://api.coinbase.com/v2/exchange-rates?currency=' + coinTicker)
    rgb.set_screen([0,0,0,0,0,0,0,0,0,0,0,0,0x10f815,0,0,0,0,0,0,0,0,0,0,0,0])
    output = json.loads((response.text))
    
    price = output['data']['rates']['USD'] # získá cenu měny zadanné do funkce a vloži ji do proměnné "price"
    currency = output['data']['currency'] # získá značku měny kterou jsme zadali do funkce a vloži ji do proměnné "currency"
    
    string_price = str(int(float(price))) # "60000.123" --> 60000.123 --> 60000 --> "60000" - zbavení se desetinných míst převáděním mezi datovými typy
    
    final_string = currency + " " + string_price # spojí cenu a značku měny s mezerou, např. "BTC 60000", "ETH 4000"
    
    # vrátí finální cenu, prodlevu se kterou se bude text posouvat (0.18 mi přijde jako ideální hodnota), a příslušnou barvu k jednotlivým krytpoměnám (oranžová: BTC, modrá: ETH)
    if currency == "BTC":
      return final_string, 0.18, 0xe67300
    elif currency == "ETH":
      return final_string, 0.18, 0x0080c0

  # pokud se něco pokazí, není přístup k internetu, neodpoví API, nastaví led na červenou    
  except:
    rgb.set_screen([0,0,0,0,0,0,0,0,0,0,0,0,0xe20325,0,0,0,0,0,0,0,0,0,0,0,0])
    wait(1)
    pass

# ---------------------------------------------------------------------------------------

def end():
  # oslavné probliknutí čtverce na konci programu
  rgb.set_screen([0x0080ff,0x0080ff,0x0080ff,0x0080ff,0x0080ff,0x0080ff,0,0x0080ff,0,0x0080ff,0x0080ff,0x0080ff,0x0080ff,0x0080ff,0x0080ff,0x0080ff,0,0x0080ff,0,0x0080ff,0x0080ff,0x0080ff,0x0080ff,0x0080ff,0x0080ff])
  wait(0.5)
  rgb.set_screen([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
  wait(0.5)
  rgb.set_screen([0x0080ff,0x0080ff,0x0080ff,0x0080ff,0x0080ff,0x0080ff,0,0x0080ff,0,0x0080ff,0x0080ff,0x0080ff,0x0080ff,0x0080ff,0x0080ff,0x0080ff,0,0x0080ff,0,0x0080ff,0x0080ff,0x0080ff,0x0080ff,0x0080ff,0x0080ff])
  wait(0.5)
  rgb.set_screen([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])

# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------

# pokud zmáčkeme tlačítko jednou, využije předešlých funkcí a vypíše cenu BTC
def buttonA_wasPressed():
  text_string, delay, color = getCurrency("BTC")  # uloží vrácené hodnoty z funkce getCurrency() do jednotlivých proměnných
  movingText(text_string, delay, color)           # zavolá funkci movingText() a vloží do ni jednotlivé hodnoty
  end()                                           # finální zablikání čtverce na indikování konce programu
btnA.wasPressed(buttonA_wasPressed)


# pokud zmáčkeme tlačítko dvakrát, využije předešlých funkcí a vypíše cenu ETH
def buttonA_wasDoublePress():
  text_string, delay, color = getCurrency("ETH")  # uloží vrácené hodnoty z funkce getCurrency() do jednotlivých proměnných
  movingText(text_string, delay, color)           # zavolá funkci movingText() a vloží do ni jednotlivé hodnoty
  end()                                           # finální zablikání čtverce na indikování konce programu
btnA.wasDoublePress(buttonA_wasDoublePress)
