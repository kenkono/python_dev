class Constants:
    def __init__(self):
        self._rss_url = "http://xml.keizaireport.com/rss/node_15.xml"

    @property
    def RSS_URL(self):
        return self._rss_url

# インスタンスを作成して定数をエクスポート
constants = Constants()