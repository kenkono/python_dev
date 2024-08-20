import feedparser
import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import time
import openai

# OpenAI APIキーを設定
# openai.api_key = 'API Key'

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
    # レポートの内容を抽出（ページ構造によって要調整）
    # <h1>タグ内にある<a>タグのリンクのclass=bbを取得する
    # report_content = " ".join([a['href'] for h1 in soup.find_all('h1') for a in h1.find_all('a', class_='bb', href=True)])   
    report_content = [a['href'] for h1 in soup.find_all('h1') for a in h1.find_all('a', class_='bb', href=True)]   
    # ヘッダーを設定
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
    # 各リンクにアクセスしてページ内容を取得
    for link in report_content:
        try:
            # リダイレクトを追跡
            response = requests.get(link, headers=headers, allow_redirects=True)
            response.raise_for_status()  # ステータスコードが200でない場合に例外を発生させる
            
            # 最初のリダイレクト先のURLを取得
            intermediate_url = response.url
            print(f"Intermediate URL: {intermediate_url}")
            
            # 1秒待機してからリクエストを送信
            time.sleep(1)
            
            # 中間ページの内容を取得して次のURLを解析
            intermediate_response = requests.get(intermediate_url, headers=headers, verify=False)
            intermediate_response.raise_for_status()
            intermediate_soup = BeautifulSoup(intermediate_response.content, "html.parser")
            
            # 次のURLを取得（ページ構造によって要調整）
            next_link = intermediate_soup.find('a')['href']
            print(f"Next URL: {next_link}")
            
            # 最終的なURLに対してリクエストを送信
            final_response = requests.get(next_link, headers=headers, verify=False)
            final_response.raise_for_status()
            
            page_content = final_response.content
            page_soup = BeautifulSoup(page_content, "html.parser")
            
            # ここでpage_soupを使ってページ内容を解析する
            print(f"Content of {next_link}:")
            # print(page_soup.prettify())  # ページ内容を表示（必要に応じて変更）

            # ページ内容をテキストとして取得
            page_text = page_soup.get_text()

            # ChatGPT APIを使用して要約
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "以下のテキストを要約してください。"},
                    {"role": "user", "content": page_text}
                ],
                max_tokens=150
            )
            
            summary = response.choices[0].message['content'].strip()
            print(summary)
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching the page {link}: {e}")
    # 取得したデータをリストに追加
    reports.append({
        'Title': report_title,
        'URL': report_url,
        'Published': report_published,
        'Content': report_content
    })
# 3. CSVへの書き出し

# ファイル名に日付を含める
filename = f"reports_{datetime.datetime.now().strftime('%Y-%m-%d')}.csv"

# DataFrameに変換してCSVに書き出し
df = pd.DataFrame(reports)
df.to_csv(filename, index=False, encoding='utf-8-sig')

print(f"CSV file '{filename}' has been created.")