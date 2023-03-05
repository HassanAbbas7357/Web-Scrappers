from base.selenium_driver import SeleniumDriver as SD
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd


class City_Table:
    def __init__(self, City_Name, Company_Table_Objects_List):
        self.City_Name = City_Name
        self.Company_Table_Objects_List = Company_Table_Objects_List


class Company_Table:
    def __init__(self, City_Name, Company_Name, Verified_Listing_Or_Not,
                 Address, Phone_Number, Mobile_Phone, Website,
                 Contact_Person, Establish_Year, Company_Employees,
                 Registration_Code, Company_Manager, Working_Hours,
                 Description, Product_And_Services,
                 Listed_In_Categories):
        self.City_Name = City_Name
        self.Company_Name = Company_Name
        self.Verified_Listing_Or_Not = Verified_Listing_Or_Not
        self.Address = Address
        self.Phone_Number = Phone_Number
        self.Mobile_Phone = Mobile_Phone
        self.Website = Website
        self.Contact_Person = Contact_Person
        self.Establish_Year = Establish_Year
        self.Company_Manager = Company_Manager
        self.Company_Employees = Company_Employees
        self.Registration_Code = Registration_Code
        self.Working_Hours = Working_Hours
        self.Description = Description
        self.Product_And_Services = Product_And_Services
        self.Listed_In_Categories = Listed_In_Categories


class Business_List(SD):
    def __init__(self):
        self.driver = webdriver.Chrome('E://D drive//Automation Tasks//Real Task//driver//chromedriver.exe')
        super().__init__(driver=self.driver)
        self.driver.maximize_window()
        # self.driver.minimize_window()
        self.base_url = 'https://www.businesslist.pk' \
                        '/browse-business-cities'
        self.driver.get(self.base_url)
        self.wait = WebDriverWait(self.driver, 25)
        self.ActionChains = ActionChains(self.driver)

    def get_Cities(self):
        cities = self.wait.until(
            EC.presence_of_all_elements_located((By.XPATH, '//ul[@class="cat_list"]//a'))
        )
        city_list = [i.text for i in cities]
        return city_list

    def get_Company_Data(self, City_Name):
        cm = 0
        Company_objects_dic_list = []
        while True:
            companies = self.wait.until(
                EC.presence_of_all_elements_located((By.XPATH, '//div[@class="company with_img g_0"]/h4/a |'
                                                               ' //div[@class="company g_0"]/h4/a'))
            )
            companies_list = [i.text for i in companies]
            for company_name in companies_list:
                # print(company_name)
                # click on company
                self.wait.until(
                    EC.presence_of_element_located((By.LINK_TEXT, company_name))
                ).click()
                # ------------ scrap company data --------------
                # if any add occurs try to press escape button
                try:
                    time.sleep(0.3)
                    var = self.driver.find_element_by_xpath("//div[@class='tp']/following-sibling::h1").text
                except:
                    self.ActionChains.send_keys(Keys.ESCAPE).perform()
                cm += 1
                print(cm)
                try:
                    Company_Name = self.wait.until(
                        EC.visibility_of_element_located((By.XPATH, "//div[@class='tp']/following-sibling::h1"))
                    ).text.strip()
                except:
                    Company_Name = "None"

                main = self.driver.find_element_by_xpath('//main')

                try:
                    Verified_Listing_Or_Not = main.find_element_by_xpath("//div[@class='vvv r_3px']")
                    Verified_Listing_Or_Not = "Verified Listing"
                except:
                    Verified_Listing_Or_Not = "Not Verified Listing"

                try:
                    Address = main.find_element_by_xpath("//div[@class='text location']").text.replace(
                        'VIEW MAP', ''
                    ).strip()
                except:
                    Address = "None"

                try:
                    Phone_Number = main.find_element_by_xpath("//div[@class='text phone']").text.strip()
                except:
                    Phone_Number = "None"

                try:
                    Mobile_Phone = main.find_element_by_xpath(
                        '//div[@class="info"]//div[contains(text(),"Mobile phone")]'
                        '/following-sibling::div[@class="text"]').text.strip()

                except:
                    Mobile_Phone = "None"

                try:
                    Website = main.find_element_by_xpath('//div[@class="text weblinks"]').text.strip()
                except:
                    Website = "None"

                try:
                    Contact_Person = main.find_element_by_xpath('//div[@class="info"]//div[contains(text()'
                                                                ',"Contact Person")]/'
                                                                'following-sibling::div[@class="text"]').text. \
                        strip()
                except:
                    Contact_Person = "None"

                try:
                    Establish_Year = main.find_element_by_xpath('//div[span="Establishment year"]'
                                                                '').text.replace('ESTABLISHMENT YEAR',
                                                                                 '').strip()
                except:
                    Establish_Year = "None"

                try:
                    Company_Manager = main.find_element_by_xpath('//div[span="Company manager"]'
                                                                 '').text.replace('COMPANY MANAGER',
                                                                                  '').strip()
                except:
                    Company_Manager = "None"

                try:
                    Company_Employees = main.find_element_by_xpath('//div[span="Employees"]'
                                                                   '').text.replace('EMPLOYEES', '').strip()

                except:
                    Company_Employees = "None"

                try:
                    Registration_Code = main.find_element_by_xpath('//div[span="Registration code"]'
                                                                   '').text.replace('REGISTRATION CODE',
                                                                                    '').strip()
                except:
                    Registration_Code = "None"

                try:
                    Working_Hours = main.find_element_by_xpath('//div[@class="info oh r_3px"'
                                                               ']'
                                                               '').text.replace('WORKING HOURS',
                                                                                '').replace('SEE ALL',
                                                                                            '').strip()
                    Working_Hours = Working_Hours.replace('Monday:', '')
                except:
                    Working_Hours = "None"

                try:
                    Description = main.find_element_by_xpath('//div[@class="text desc"]').text.splitlines()
                    Description = " ".join(Description)
                except:
                    Description = "None"

                try:
                    Listed_In_Categories = main.find_elements_by_xpath('//div[@class="categories"]//a')
                    Listed_In_Categories = [i.text for i in Listed_In_Categories]
                    Listed_In_Categories = ", ".join(Listed_In_Categories)
                except:
                    Listed_In_Categories = "None"

                # ------------------------------------  products  -------------------------------------
                Product_And_Services_Descriptions_List = None
                try:
                    more_products_btn = self.driver.find_element_by_xpath('//a[@class="company_more"]')
                except:
                    more_products_btn = None

                if more_products_btn is not None:
                    try:
                        more_products_btn.click()
                        Products = self.wait.until(
                            EC.presence_of_all_elements_located((By.XPATH, '//div[@class="product"]'))
                        )
                        Product_And_Services_Descriptions_List = [i.text.replace('\n', ' : ') for i in Products]
                        self.driver.back()

                    except:
                        self.driver.back()
                        Product_And_Services_Descriptions_List = "None"
                elif more_products_btn is None:
                    try:
                        Products = self.wait.until(
                            EC.presence_of_all_elements_located((By.XPATH, '//div[@class="product"]'))
                        )
                        Product_And_Services_Descriptions_List = [i.text.replace('\n', ' : ') for i in Products]

                    except:
                        Product_And_Services_Descriptions_List = "None"

                # -------------------------------------------------------------------------------------------

                print(f"\n\nCompany_Name : {Company_Name} \nAddress : {Address} \nPhone_Number : {Phone_Number}"
                      f"\nMobile_Phone : {Mobile_Phone} \nWebsite : {Website} \nContact_Person : {Contact_Person}"
                      f"\nEstablish_Year : {Establish_Year} "
                      f"\nCompany_Manager : {Company_Manager}"
                      f"\nCompany_Employees: {Company_Employees} \nRegistration_Code : {Registration_Code}"
                      f"\nWorking_Hours : {Working_Hours}\nDescription : {Description} \n"
                      f"\nProduct_And_Services_Description_List : {Product_And_Services_Descriptions_List}"
                      f" \nListed_In_Categories : {Listed_In_Categories}"
                      )
                # ------------------------------------------------
                # ------------ Object Creation ----------------

                Company_Table_dic = {
                    'City_Name': City_Name,
                    'Company_Name': Company_Name,
                    'Verified_Listing_Or_Not': Verified_Listing_Or_Not,
                    'Address': Address,
                    'Phone_Number': Phone_Number,
                    'Mobile_Phone': Mobile_Phone,
                    'Website': Website,
                    'Contact_Person': Contact_Person,
                    'Establish_Year': Establish_Year,
                    'Company_Employees': Company_Employees,
                    'Registration_Code': Registration_Code,
                    'Company_Manager': Company_Manager,
                    'Working_Hours': Working_Hours,
                    'Description': Description,
                    'Product_And_Services': Product_And_Services_Descriptions_List,
                    'Listed_In_Categories': Listed_In_Categories
                }
                Company_objects_dic_list.append(Company_Table_dic)
                self.driver.back()

            try:
                # next btn
                self.wait.until(
                    EC.presence_of_element_located((By.XPATH, "//a[@rel='next']"))
                ).click()
            except:
                break
        df = pd.DataFrame.from_dict(Company_objects_dic_list)
        df.to_csv(f'{City_Name}.csv', index=False)
        print(df.head(10))

    def get_City_Data(self, city):
        # go to city page to scrap data of city
        self.wait.until(
            EC.presence_of_element_located((By.LINK_TEXT, city))
        ).click()
        time.sleep(2)
        self.ActionChains.send_keys(Keys.ESCAPE).perform()
        time.sleep(1)
        # now get all the companies data
        self.get_Company_Data(City_Name=city)

    def click_city(self):
        # city_list = self.get_Cities()
        city_list = ['Chakdara']
        for city in city_list:
            # City_Data = self.get_City_Data(city)
            self.get_City_Data(city)
            self.driver.get(self.base_url)

        self.driver.quit()


obj = Business_List()
obj.click_city()
