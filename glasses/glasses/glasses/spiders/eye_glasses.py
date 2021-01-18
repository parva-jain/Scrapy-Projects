import scrapy


class EyeGlassesSpider(scrapy.Spider):
    name = 'eye_glasses'
    allowed_domains = ['www.glassesshop.com']
    start_urls = ['https://www.glassesshop.com/bestsellers']

    def start_requests(self):
        yield scrapy.Request(url = 'https://www.glassesshop.com/bestsellers', callback=self.parse, headers={
            'User-Agent' : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"
        })

    def parse(self, response):
        for product in response.xpath("//div[@class='col-12 pb-5 mb-lg-3 col-lg-4 product-list-row text-center product-list-item']"):
            yield{
                'product_url': product.xpath(".//div[@class='product-img-outer']/a/@href").get(),
                'image_url': product.xpath(".//img[@class='lazy d-block w-100 product-img-default']/@data-src").get(),
                'name': product.xpath(".//div[@class='p-title']/a/@title").get(),
                'price': product.xpath(".//div[@class='p-price']/div/span[1]/text()").get(),
                'User-Agent' : response.request.headers['User-Agent']
            }

        next_page = response.xpath('//a[@rel="next"]/@href').get()

        if next_page:
            yield scrapy.Request(url=next_page, callback=self.parse, headers={
            'User-Agent' : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"
            })                
            
