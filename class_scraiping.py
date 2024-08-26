import pandas as pd
from datetime import datetime

class RSSScraper:
    def __init__(self):
        self.data = []

    def add_data(self, idx, title, link, description):
        self.data.append({
            'No': idx,
            'Title': title,
            'Link': link,
            'Description': description
        })

    def save_to_csv(self, filename: str) -> None:
        # データをDataFrameに変換
        df = pd.DataFrame(self.data)

        # CSVファイルに保存
        df.to_csv(filename, index=False, encoding='utf-8-sig')

class DateManager:
    def _get_current_date(self) -> str:
        return datetime.now().strftime("%Y%m%d")

    def generate_filename(self, base_name: str) -> str:
        current_date = self._get_current_date()
        return f"{base_name}_{current_date}.csv"

def main():
    # RSSフィードのURL
    rss_url = "http://xml.keizaireport.com/rss/node_15.xml"

    # CSVファイル名に日付を追加
    filename = DateManager.generate_filename("rss_feed_data")

    # RSSScraperのインスタンスを作成
    scraper = RSSScraper()

    # ここでRSSフィードをスクレイピングしてデータを追加する処理を行う
    # 例: scraper.add_data(idx, title, link, description)

    # データをCSVファイルに保存
    scraper.save_to_csv(filename)

if __name__ == "__main__":
    main()