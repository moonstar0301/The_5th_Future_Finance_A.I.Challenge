import threading
from crawling import real_estate_research_crawl, tax_research_crawl, investment_research_crawl
from pdf_merge import pdf_merger

def thread_function(func):
    func()

if __name__ == "__main__":
    real_estate_research_crawl()
    tax_research_crawl()
    investment_research_crawl()
    pdf_merger()
