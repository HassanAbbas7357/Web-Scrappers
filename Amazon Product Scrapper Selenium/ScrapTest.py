from selenium.webdriver.common.by import By
import time
from selenium_utils import Util_sel
import csv
import os
from bs4 import BeautifulSoup



class Amaz_Scrap(Util_sel):

    _sel = ""
    def __init__(self):
        self.openChrome()

    def ExecuteScrapng(self):

        # Num of pages
        TotalPages_PAth = "//div[contains(@class,'a-padding-base')]//li[last()-1]"
        WatchPage = "//div[contains(@class,'a-padding-base')]//li[last()]//a"
        Prodcts = "//div[@class='s-main-slot s-result-list s-search-results sg-row']/div[@data-component-type='s-search-result']"

        Tot_Pags = self.getElementText(TotalPages_PAth, By.XPATH)
        print(Tot_Pags)
        for page in range(int(Tot_Pags)):
            page = page+1
            print("Start Page Scrap :"+str(page))
            if page > 1:
                self.clickElement(WatchPage)
                time.sleep(2)
            Tot_prodcts = len(self.getElements(Prodcts))
            for i in range(Tot_prodcts):
                i = i+1
                EachWatcDiv = Prodcts+"["+str(i)+"]"
                watchBrand_pth =EachWatcDiv+"//h5[@class='s-line-clamp-1']//span"
                watchBrand = self.getElementText(watchBrand_pth)
                self.clickElement(EachWatcDiv)
                time.sleep(2)
                arraylst = self.getProd_Data(watchBrand)
                if len(arraylst) > 0:
                    self.writeCsv(arraylst)




    def getProd_Data(self,watchBrand):

        windows = self.driver.window_handles
        self.driver.switch_to_window(windows[1])

        # getting new tab data
        arraylst = []
        self.clickElement("//a[.='See all reviews']")
        time.sleep(2)
        # calculate paging
        Tot_review_txt = self.getElementText("//div[@data-hook='cr-filter-info-review-rating-count']//span")
        reviews_Path  = "//div[@data-hook='review']"
        Tot_review = Tot_review_txt.split("|")[1].strip()
        Tot_review = Tot_review.split(" ")[0].replace(",", "")
        Rews_pr_pag = 10
        Per_pag = int(Tot_review) / Rews_pr_pag
        Tot_pags = int(round(Per_pag))
        Tot_pags = 1 if Tot_pags == 0 else Tot_pags
        print("Total Review Pages : "+str(Tot_pags))
        try:
            for i in range(Tot_pags):

                rev_n = i+1
                print("rev_n = " +str(rev_n))
                if rev_n > 1:
                    self.clickElement("//li[@class='a-last']//a[contains(.,'Next page')]")
                    time.sleep(2)

                # get each page reviews / 10
                self.GetReviews_of_Page(watchBrand, arraylst)
                # for r_n_pag in range(Rews_pr_pag):
                #     r_n_pag = r_n_pag+1
                #     Rev_Box = reviews+"["+str(r_n_pag)+"]//div[contains(@id, 'customer_review')]"
                #     USerNam = self.getElementText(reviews + "//span[@class='a-profile-name']")
                #     ratingstar  =  self.getElementText(Rev_Box + "//i[@data-hook='review-star-rating']/span")
                #     reviewDate  =  self.getElementText(Rev_Box + "//span[@data-hook='review-date']")
                #     reviewBodytext  =  self.getElementText(Rev_Box + "//span[@data-hook='review-body']")
                #     watchlist.append(watchBrand)
                #     watchlist.append(USerNam)
                #     watchlist.append(ratingstar)
                #     watchlist.append(reviewDate)
                #     watchlist.append(reviewBodytext)
                #     arraylst.append(watchlist)
                # self.writeCsv(arraylst)
                # watchlist = []
                # arraylst = []



            self.driver.close()
            self.driver.switch_to_window(windows[0])
            return arraylst
        except Exception as ex:
            print(str(ex))




    def GetReviews_of_Page(self, watchBrand, arraylst):
        reviews = "//div[@data-hook='review']"

        Rews_pr_pag = 10
        try:
            for r_n_pag in range(Rews_pr_pag):
                r_n_pag = r_n_pag + 1
                Rev_Box = reviews + "[" + str(r_n_pag) + "]//div[contains(@id, 'customer_review')]"
                USerNam = self.getElementText(Rev_Box + "//span[@class='a-profile-name']")
                # ratingstar = self.getElementText(Rev_Box + "//a[@class='a-link-normal']//span[@class='a-icon-alt']")
                ratingstar = self.getElementAttributeText(Rev_Box + "//a[@class='a-link-normal']", "title")
                Prod_color = self.getElementText(Rev_Box + "//a[@data-hook='format-strip']")
                reviewDate = self.getElementText(Rev_Box + "//span[@data-hook='review-date']")
                reviewBodytext = self.getElementText(Rev_Box + "//span[@data-hook='review-body']")
                Peopl_found = self.getElementText(Rev_Box + "//span[@data-hook='helpful-vote-statement']")

                # rating
                # htm_rat = self.getElementAttributeText(Rev_Box + "//a[@class='a-link-normal']//span[@class='a-icon-alt']", "innherHTML")
                # soup = BeautifulSoup(htm_rat, 'html.parser')
                #
                # ratingstar1 = soup.find("tbody").find_all("span", {"class":"a-icon-alt"}).text


                watchlist = []

                # watchlist.append("")
                watchlist.append("Watch")
                watchlist.append(watchBrand)
                watchlist.append(USerNam)
                watchlist.append(ratingstar)
                watchlist.append(reviewDate)
                watchlist.append(Prod_color)
                watchlist.append(reviewBodytext)
                watchlist.append(Peopl_found)
                if USerNam != "":
                    arraylst.append(watchlist)
            print(arraylst)
        except Exception as ex:
            print(str(ex))


    def writeCsv(self, arraylst):
        headers = ['Category', 'Product Name', 'Review Users', 'Stars', 'Review Post Date', 'Product color',
                   'Review Description', 'People Found Helpful']
        fileName = "AmazonReviewsData.csv"
        with open(fileName, 'a+', newline='', encoding="utf-8") as file:
            file_is_empty = os.stat(fileName).st_size == 0
            writer = csv.writer(file)
            if file_is_empty:
                writer.writerow(headers)
            writer.writerows(arraylst)



a = Amaz_Scrap().ExecuteScrapng()




