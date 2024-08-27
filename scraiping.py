import feedparser
import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime

# 1. RSSフィードの取得とパース
rss_url = "http://xml.keizaireport.com/rss/node_15.xml"
feed = feedparser.parse(rss_url)

# 2. レポートリンクの取得と内容のスクレイピング
reports = []

for entry in feed.entries:
    report_url = entry.link
    report_title = entry.title
    report_published = entry.published

    # レポートリンクから内容を取得
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    response = requests.get(report_url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    
    # レポートの内容を抽出
    report_content = [a['href'] for h1 in soup.find_all('h1') for a in h1.find_all('a', class_='bb', href=True)]
    
    # 取得したデータをリストに追加
    reports.append({
        'Title': report_title,
        'URL': report_url,
        'Published': report_published,
        'Content': report_content
    })
    print(report_content)

# 3. CSVへの書き出し
# ファイル名に日付を含める
filename = f"reports_{datetime.datetime.now().strftime('%Y-%m-%d')}.csv"

# DataFrameに変換してCSVに書き出し
df = pd.DataFrame(reports)
df.to_csv(filename, index=False, encoding='utf-8-sig')

print(f"CSV file '{filename}' has been created.")
