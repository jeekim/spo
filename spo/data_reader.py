import glob
from bs4 import BeautifulSoup as bs
from typing import Iterator


class DataReader:
    """

    """
    def __init__(self, data_dir):
        self.data_dir = data_dir

    def get_reader(self) -> Iterator:
        """
        PMC article generator for SPO extraction
        :return:
        """
        files = glob.glob(f'{self.data_dir}/*.nxml')
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

