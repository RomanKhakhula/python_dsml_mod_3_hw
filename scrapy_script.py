import json
import scrapy
from itemadapter import ItemAdapter
from scrapy import Item, Field
from scrapy.crawler import CrawlerProcess
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from write_jsons_into_mongo import write_jsons_into_mongo

class CitationItem(Item):
    citation_tags = Field()
    citation_author = Field()
    citation = Field()

class CitationAuthorItem(Item):
    author_fullname = Field()
    author_born_date = Field()
    author_born_location = Field()
    author_description = Field()

class DataPipeline:
    citations = []
    citation_authors = []

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if 'citation' in adapter.keys():
            self.citations.append(dict(adapter))
        elif 'author_fullname' in adapter.keys():
            self.citation_authors.append(dict(adapter))
        else:
            raise Exception('Something went wrong.')

    def close_spider(self, spider):
        with open('citations.json', 'w', encoding='utf-8') as f:
            json.dump(self.citations, f, ensure_ascii=False, indent=4)
        with open('citation_authors.json', 'w', encoding='utf-8') as f:
            json.dump(self.citation_authors, f, ensure_ascii=False, indent=4)

class GetCitationSpider(scrapy.Spider):
    name = 'get_citation'
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com/"]
    custom_settings = {"ITEM_PIPELINES": {DataPipeline: 300}}

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

if __name__ == '__main__':
    process = CrawlerProcess()
    process.crawl(GetCitationSpider)
    process.start()
    write_jsons_into_mongo() 