import scrapy

from .geo_locator import links

class RestaurantScraper(scrapy.Spider):
    name = "nearby_restaurant"
    start_urls = links
    def parse(self, response):  
        for article in response.css("tr.athing"):
            yield {
                "title": article.css("a.storylink::text").get(),
                "url": article.css("a.storylink::attr(href)").get(),
                "votes": int(article.css("span.score::text").re_first(r"\d+"))
            }
        
        next_page = response.css("a.morelink::attr(href)").get()
        if next_page is not None:
            yield response.follow(next_page,self.parse)