import feedparser
import pandas as pd
from datetime import datetime

class RSSScraper:
    def __init__(self, rss_url: str):
        self.rss_url = rss_url
        self.data = []

    def fetch_data(self) -> None:
        # RSSフィードを解析
        feed = feedparser.parse(self.rss_url)

        # 各エントリから必要な情報を抽出
        for idx, entry in enumerate(feed.entries, start=1):
            title = entry.title
            link = entry.link
            description = entry.description
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

if __name__ == "__main__":
    # RSSフィードのURL
    rss_url = "http://xml.keizaireport.com/rss/node_15.xml"

    # 現在の日付を取得
    current_date = datetime.now().strftime("%Y%m%d")

    # CSVファイル名に日付を追加
    filename = f"rss_feed_data_{current_date}.csv"

    # RSSスクレイパーのインスタンスを作成
    scraper = RSSScraper(rss_url)

    # データを取得してCSVに保存
    scraper.fetch_data()
    scraper.save_to_csv(filename)

    print(f"CSVファイル '{filename}' が作成されました。")