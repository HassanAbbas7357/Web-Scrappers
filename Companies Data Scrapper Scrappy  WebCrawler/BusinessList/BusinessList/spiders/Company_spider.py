import scrapy
from ..items import BusinesslistItem


class CompanySpider(scrapy.Spider):
    name = 'CompanySpider'
    start_urls = [
        'https://www.businesslist.pk/location/karachi',
    ]
##
    def parse(self, response):
        company_page_links = response.xpath('//div[@class="company with_img g_0"]/h4/a | //div[@class="company '
                                            'g_0"]/h4/a')
        yield from response.follow_all(company_page_links, self.parse_company)

        pagination_links = response.xpath("//a[@rel='next']/@href")
        yield from response.follow_all(pagination_links, self.parse)

    def parse_company(self, response):
        def extract_with_xpath(query):
            return response.xpath(query).get(default='None').strip()

        def extract_verified_xpath(query):
            return response.xpath(query).get(default='Not-Verified').strip().replace('Listing', 'Verified-Listing')

        items = BusinesslistItem()
        Company_Name = extract_with_xpath("//b[@id='company_name']/text()")
        Verified_Listing_Or_Not = extract_verified_xpath("//div[@class='vvv r_3px']/text()")
        Address = extract_with_xpath("//div[@class='text location']/text()").replace('VIEW MAP', '')
        Phone_Number = extract_with_xpath("//div[@class='text phone']/text()").replace('=', '+')
        Mobile_Phone = extract_with_xpath('//div[@class="info"]//div[contains(text(),"Mobile phone")]'
                                          '/following-sibling::div[@class="text"]/text()').replace('=', '+')
        Website = extract_with_xpath('//div[@class="text weblinks"]/a/@href')
        Contact_Person = extract_with_xpath('//div[@class="info"]//div[contains(text()'
                                            ',"Contact Person")]/'
                                            'following-sibling::div[@class="text"]/text()')
        Establish_Year = extract_with_xpath('//div[span="Establishment year"]/text()').replace('Establishment Year', '')
        Company_Manager = extract_with_xpath('//div[span="Company manager"]/text()')
        Company_Employees = response.xpath('//div[span="Employees"]/text()').get()

        if Company_Employees is not None:
            Company_Employees = Company_Employees.replace('EMPLOYEES', '')

        Registration_Code = extract_with_xpath('//div[span="Registration code"]/text()').replace('REGISTRATION CODE',
                                                                                                 '')
        Working_Hours = extract_with_xpath("//div[@class='cmp_more']//table//tr[1]/td[2]/text()")
        Description = extract_with_xpath('string(//div[@class="text desc"])').splitlines()
        Description = " ".join(Description)

        Product_And_Services = response.xpath('string(//div[@class="product"])').getall()
        Product_And_Services_Descriptions_List = [i.replace('\n', ' : ') for i in Product_And_Services]

        Listed_In_Categories = response.xpath('//div[@class="categories"]//a/text()').getall()

        yield {
            'Company_Name': Company_Name,
            'Verified_Listing_Or_Not': Verified_Listing_Or_Not,
            'Address': Address,
            'Phone_Number': Phone_Number,
            'Mobile_Phone': Mobile_Phone,
            'Website': Website,
            'Contact_Person': Contact_Person,
            'Establish_Year': Establish_Year,
            'Company_Manager': Company_Manager,
            'Company_Employees': Company_Employees,
            'Registration_Code': Registration_Code,
            'Working_Hours': Working_Hours,
            'Description': Description,
            'Product_And_Services': Product_And_Services_Descriptions_List,
            'Listed_In_Categories': Listed_In_Categories

        }
