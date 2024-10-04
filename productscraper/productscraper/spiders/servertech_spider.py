import scrapy

class ServerTechSupplySpider(scrapy.Spider):
    name = "servertech"
    start_urls = ['https://www.servertechsupply.com/shop/?items_per_page=80']  # URL for 80 items per page

    def parse(self, response):
        # Extract product links from the main product listing page
        product_links = response.css('h3.product-name a::attr(href)').getall()

        # Follow each product link
        for link in product_links:
            yield response.follow(link, self.parse_product)

        # Follow the "Next" page link if it exists
        next_page = response.css('a.next.page-numbers::attr(href)').get()
        if next_page:
           yield scrapy.Request(url=next_page, callback=self.parse)

    def parse_product(self, response):
        # Extracting product details from the product page
        yield {
            'name': response.css('h1.product_title::text').get(),
            'price': response.css('p.price span.woocommerce-Price-amount bdi::text').get(),
            'sku': response.css('div.sku-wrapper span.sku::text').get(),
            'availability': response.css('div.availability-text::text').get(),
            'brand': response.css('span.yith-wcbr-brands a::text').get(),
            'description': response.css('div.woocommerce-product-details__short-description p::text').get(),
            'image_url': response.css('div.woocommerce-product-gallery__image a::attr(href)').get(),
            'technical_specifications': self.parse_technical_specs(response),
            #'url': response.url
        }
        

    def parse_technical_specs(self, response):
        specs = response.css('div.product-content p::text').getall()
        # Combine the specifications into a single string with newline characters
        return "\n".join(spec.strip() for spec in specs if spec.strip())
