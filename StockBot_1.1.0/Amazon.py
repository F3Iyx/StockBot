import time
import datetime
from beep import *


class Amazon:
    def __init__(self, browser):
        # Ein Amazon-Link wird geöffnet
        browser.get('https://www.amazon.de/')

        # Der Benutzer wird durch die Anmeldung geführt
        signIn = browser.find_element_by_id("nav-link-accountList")
        signIn.click()
        x = str(datetime.datetime.now())
        print('\033[2;37m'+ x + '\033[2;33m' + " Please login. When logged in successfully, the program should continue.")
        loginFinished = False
        i = 0
        while not loginFinished:
            try:
                searchbar = browser.find_element_by_id("twotabsearchtextbox")
                x = str(datetime.datetime.now())
                print('\033[2;37m'+ x + '\033[2;33m' + " Program continues.")
                loginFinished = True

            except:
                time.sleep(1)
                i += 1
                if i == 10:
                    x = str(datetime.datetime.now())
                    print('\033[2;37m'+ x + '\033[2;33m' + " You're still signing in")
                    i = 0

        # Hier wird versucht, die Cookies zu deaktivieren. Kommt kein Popup, wird nur 1 Sekunde gewartet.
        try:
            acceptCookies = browser.find_element_by_id("sp-cc-accept")
            acceptCookies.click()
        except:
            time.sleep(0)

    def check(self, browser, link, maxPrice):
        # Die Seite wird geöffnet
        browser.get(link)

        #Initialisierung einer Fehler-variable
        amountError = False

        # Der Gegenstand wird wenn möglich zum Warenkorb hinzugefügt.
        try:
            title = str(browser.title)
            addToCart = browser.find_element_by_id("add-to-cart-button")
            addToCart.click()
            x = str(datetime.datetime.now())
            print('\033[2;37m'+ x + '\033[2;32m' + " Button was clicked: " + title)

            # Wenn man nur einen Gegenstand im Warenkorb hat, geht wenn möglich weiter zum Checkout (zur Kasse).
            try:
                productCount = browser.find_element_by_id('nav-cart-count')
                productCount = int(productCount.text)
                x = str(datetime.datetime.now())
                print('\033[2;37m'+ x + '\033[2;32m' + ' Product Count: ' + str(productCount))
                if productCount == 1:
                    proceedToCheckout = browser.find_element_by_id("hlb-ptc-btn-native")
                    proceedToCheckout.click()
                    x = str(datetime.datetime.now())
                    print('\033[2;37m'+ x + '\033[2;32m' + " Proceeding to checkout")
                elif productCount < 1:
                    print(1 + 'This brings an error message')
                elif productCount > 1:
                    x = str(datetime.datetime.now())
                    print('\033[2;37m'+ x + '\033[2;33m' + ' change amount in your cart and continue manually')
                    cart = browser.find_element_by_id('hlb-view-cart-announce')
                    cart.click()
                    beep(4)
                    try:
                        amount = browser.find_element_by_id('a-autoid-1-announce')
                        while amount is not None:
                            amount = browser.find_element_by_id('a-autoid-1-announce')
                            beep(4)
                            time.sleep(4)
                    except:
                        x = str(datetime.datetime.now())
                        print('\033[2;37m'+ x + '\033[2;33m' + 'Please configure your cart properly and continue by ordering manually.')
                    x = str(datetime.datetime.now())
                    print('\033[2;37m'+ x + '\033[2;33m' + ' Type anything to continue')
                    input()
                    browser.get(link)
                    amountError = True

                # Der Gegenstand wird wenn möglich gekauft.
                try:
                    price = browser.find_element_by_class_name("a-color-price hlb-price a-inline-block a-text-bold")
                    price = price.text
                    x = str(datetime.datetime.now())
                    print('\033[2;37m'+ x + '\033[2;32m' + ' (Debug) initial price = ' + price)
                    price = price.replace(',', '.')
                    price = price.replace('€', '')
                    price = float(price)
                    x = str(datetime.datetime.now())
                    print('\033[2;37m'+ x + '\033[2;32m' + ' price = ' + str(price) + '€')

                    if price <= maxPrice:
                        buy = browser.find_element_by_id("submitOrderButtonId")
                        buy.click()
                        x = str(datetime.datetime.now())
                        print('\033[2;37m'+ x + '\033[2;32m' + " Congratulations!!! You got whatever you wanted!")
                        transactionPossible = True
                    else:
                        x = str(datetime.datetime.now())
                        print('\033[2;37m'+ x + '\033[2;31m' + " Price was too high. <" + str(price) + "> Exit Program.")

                except:
                    if amountError is False:
                        beep(4)
                        try:
                            mailField = browser.find_element_by_id('ap_email')
                            while mailField is not None:
                                mailField = browser.find_element_by_id('ap_email')
                                beep(4)
                                time.sleep(4)
                        except:
                            x = str(datetime.datetime.now())
                            print('\033[2;37m'+ x + '\033[2;33m' + ' Type anything to continue')
                            input()
                            browser.get(link)
                    amountError = False

            except:
                beep(4)

        except:
            x = str(datetime.datetime.now())
            print('\033[2;37m'+ x + '\033[2;31m' + " no AddToCart-Button for: " + str(browser.title))
