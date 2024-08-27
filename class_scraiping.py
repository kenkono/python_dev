import requests
import pandas as pd
from datetime import datetime
import xml.etree.ElementTree as ET
from Constants import constants  # 定数をインポート

class RSSScraper:
    def __init__(self):
        self.data = []

    def fetch_rss(self, url: str):
        response = requests.get(url)
        response.raise_for_status()
        return response.content

    def parse_rss(self, rss_content: bytes):
        root = ET.fromstring(rss_content)
        for idx, item in enumerate(root.findall(".//item"), start=1):
            title = item.find("title").text
            link = item.find("link").text
            description = item.find("description").text
            self.add_data(idx, title, link, description)

    def add_data(self, idx, title, link, description):
        self.data.append({
            'No': idx,
            'Title': title,
            'Link': link,
            'Description': description
        })

    def save_to_csv(self, filename: str) -> None:
        df = pd.DataFrame(self.data)
        df.to_csv(filename, index=False, encoding='utf-8-sig')

class DateManager:
    def _get_current_date(self) -> str:
        return datetime.now().strftime("%Y%m%d")

    def generate_filename(self, base_name: str) -> str:
        current_date = self._get_current_date()
        return f"{base_name}_{current_date}.csv"

def main():
    rss_url = constants.RSS_URL  # 定数を使用

    rss_scraper = RSSScraper()
    date_manager = DateManager()

    rss_content = rss_scraper.fetch_rss(rss_url)
    rss_scraper.parse_rss(rss_content)

    filename = date_manager.generate_filename("rss_data")
    rss_scraper.save_to_csv(filename)

if __name__ == "__main__":
    main()