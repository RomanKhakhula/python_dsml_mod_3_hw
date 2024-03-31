import scrapy
from get_citations.items import CitationItem, CitationAuthorItem

class GetCitationsSpider(scrapy.Spider):
    name = "get_citations"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com"]

    def parse(self, response, **kwargs):
        for c in response.xpath("/html//div[@class='quote']"):
            citation_tags = c.xpath("div[@class='tags']/a/text()").extract()
            citation_author = c.xpath("span/small[@class='author']/text()").get().strip()
            citation = c.xpath("span[@class='text']/text()").get().strip()
            

            yield CitationItem(citation_tags=citation_tags, citation_author=citation_author, citation=citation)
            yield response.follow(url=self.start_urls[0] + c.xpath("span/a/@href").get(), callback=self.parse_citation_author)

        next_link = response.xpath("/html//li[@class='next']/a/@href").get()
        if next_link:
            yield scrapy.Request(url=self.start_urls[0] + next_link)
                
    @classmethod
    def parse_citation_author(cls, response, **kwargs):
        citation_author = response.xpath("/html//div[@class='author-details']")
        author_fullname = citation_author.xpath("h3[@class='author-title']/text()").get().strip()
        author_born_date = citation_author.xpath("p/span[@class='author-born-date']/text()").get().strip()
        author_born_location = citation_author.xpath("p/span[@class='author-born-location']/text()").get().strip()
        author_description = citation_author.xpath("div[@class='author-description']/text()").get().strip()

        yield CitationAuthorItem(author_fullname=author_fullname, author_born_date=author_born_date, author_born_location=author_born_location, author_description=author_description)