# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Item, Field

class CitationItem(Item):
    citation_tags = Field()
    citation_author = Field()
    citation = Field()


class CitationAuthorItem(Item):
    author_fullname = Field()
    author_born_date = Field()
    author_born_location = Field()
    author_description = Field()
