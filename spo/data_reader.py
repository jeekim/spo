import glob
from bs4 import BeautifulSoup as bs


class DataReader:
    """

    """
    def __init__(self):
        self.data_dir = '/Users/jee.hyub.kim/Projects/spo/data/*.nxml'

    def get_reader(self):
        files = glob.glob(self.data_dir)
        for file in files:
            with open(file, 'r') as f:
                content = f.readlines()
                # Combine the lines in the list into a string
                content = "".join(content)
                bs_content = bs(content, "lxml")
                pmcid = bs_content.find("article-id", {"pub-id-type": "pmc"}).get_text()
                title = bs_content.find("article-title").get_text()
                if not bs_content.find('abstract'):
                    continue
                abstract = bs_content.find("abstract").get_text()
                yield pmcid, title, abstract

