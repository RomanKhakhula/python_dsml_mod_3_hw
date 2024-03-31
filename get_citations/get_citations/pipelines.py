# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import json
from itemadapter import ItemAdapter
from write_jsons_into_mongo import write_jsons_into_mongo

class GetCitationsPipeline:
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
        
        write_jsons_into_mongo()
