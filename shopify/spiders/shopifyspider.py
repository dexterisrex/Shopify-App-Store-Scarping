from scrapy.spiders import Spider
from scrapy import Request

class MySpider(Spider):

    name = 'shopify'
    allowed_domains = ['shopify.com']
    start_urls = ['https://apps.shopify.com/categories/selling-products-product-variants?surface_detail=selling-products&surface_type=category&surface_version=redesign']

    def parse(self, response):
        for product in response.css('figure~div>div.tw-flex'):
            name = product.css('div .tw-text-heading-6 a::text').extract_first().strip()
            rating = product.css('div .tw-items-center span::text').extract_first().strip()
            reviews = product.css('div .tw-items-center span + span + span::text').extract_first().strip().replace('(','').replace(')','').replace('total reviews','')
            plan_type = product.css('div .tw-items-center span + span + span + span + span::text').extract_first() if rating == 'No reviews' else product.css('div .tw-items-center span + span + span + span + span + span::text').extract_first()
            rating = '' if rating == 'No reviews' else rating
            descriptions = product.css('div .tw-text-fg-tertiary::text').extract_first().strip()
            try:  next_page_url = response.css('[rel="next"].tw-group')[0].attrib['href']
            except:  next_page_url = False

            yield {
                 'Company Name': name,
                 'Compnay Rating': rating,
                 'Company Reviews': reviews,
                 'Company Trial': plan_type,
                 'Company Description': descriptions,
             }

        if next_page_url:
            yield Request(next_page_url, callback=self.parse)