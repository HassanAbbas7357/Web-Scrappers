import scrapy


class BusinesslistItem(scrapy.Item):
    Company_Name = scrapy.Field()
    Verified_Listing_Or_Not = scrapy.Field()
    Address = scrapy.Field()
    Phone_Number = scrapy.Field()
    Mobile_Phone = scrapy.Field()
    Website = scrapy.Field()
    Contact_Person = scrapy.Field()
    Establish_Year = scrapy.Field()
    Company_Manager = scrapy.Field()
    Company_Employees = scrapy.Field()
    Registration_Code = scrapy.Field()
    Working_Hours = scrapy.Field()
    Description = scrapy.Field()
    Product_And_Services = scrapy.Field()
    Listed_In_Categories = scrapy.Field()
