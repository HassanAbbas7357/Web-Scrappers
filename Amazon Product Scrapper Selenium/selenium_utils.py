
from selenium import webdriver
from selenium.webdriver.common.by import By
import time


class Util_sel():
    driver = None

    def openChrome(self):
        try:
            driver = webdriver.Chrome("E:\D drive\Automation Tasks\Halima\AmazonScrap\chromedriver.exe")
            driver.get("https://www.amazon.in/s/ref=sr_il_to_watches?rh=n%3A1350387031%2Cn%3A%211350388031%2Cn%3A2563504031%2Cp_n_availability%3A1318485031&bbn=2563504031&ie=UTF8&qid=1535045015&lo=none")
            time.sleep(5)
            self.driver = driver
        except:
            print("Invalid login")
            exit()

    def GetBy(self, LocaType):

        if LocaType is not None:
            if LocaType == By.ID:
                return By.ID
            if LocaType == By.CLASS_NAME:
                return By.CLASS_NAME
            if LocaType == By.XPATH:
                return By.XPATH
            if LocaType == By.LINK_TEXT:
                return By.LINK_TEXT
            if LocaType == By.CSS_SELECTOR:
                return By.CSS_SELECTOR
            if LocaType == By.NAME:
                return By.NAME
        else:
            print("Locator Type ::" + LocaType + " is not correct")
        return False
    def getElement(self, locator, locaType=By.XPATH):
        # element = ""
        element = False
        getBy = self.GetBy(locaType)
        try:
            # element = self.driver.find_element(getBy, locator)
            # if element is not None and element != False:
            #     return element
            # else:
            #     return False

            elements_list = self.driver.find_elements(getBy, locator)
            if len(elements_list)> 0:
                element = elements_list[0]

            if element is not None and element != False:
                return element
            else:
                str("Element Not Found with Locator :: " + locator + "and Locator Type = " + getBy)
                return False

        except Exception as ex:
            print(str(ex))

    def getElements(self, locator, locaType=By.XPATH):
        # element = ""
        getBy = self.GetBy(locaType)
        try:
            element = self.driver.find_elements(getBy, locator)
            return element
            # print("Elements Found with Locator :: " + locator + "and Locator Type = "
            #       + getBy)

        except:
            print("Elements Not Found")
        return None

    def getElementText(self, locator, locaType=By.XPATH, returnBlankStr = True):

        gettext = self.getElement(locator, locaType)
        if gettext != False:
            textfecth = gettext.text
            # print("textfecth ::"+textfecth)
            return "" + textfecth
        if returnBlankStr == True:
            return ""
        else:
            return None

    def clickElement(self, locator, locaType=By.XPATH):

        try:
            element = self.getElement(locator, locaType)
            if element != False:
                element.click()
        except Exception as ex:

            print(str(ex))

    def getElementAttributeText(self, locator, attributeName, locaType=By.XPATH, returnBlankStr = True):

        try :
            element = self.getElement(locator, locaType)
            if element != False and element is not None:
                AttrTxt = element.get_attribute(str(attributeName))
                return AttrTxt
        except :
            print("")

        if returnBlankStr == True:
            return ""
        else:
            return None