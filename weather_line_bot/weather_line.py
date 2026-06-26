import os
import requests
import datetime
from linebot import LineBotApi
from linebot.models import TextSendMessage

# 今日の月と日を取得
now_time = datetime.date.today()

# LINEのChannelAccessTokenとUSER IDを取得する
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
USER_ID = os.getenv("USER_ID")

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)

# 気象庁から天気情報を取得
url = "https://www.jma.go.jp/bosai/forecast/data/forecast/110000.json" # 熊谷地方気象台

try:
    response = requests.get(url)
    response.raise_for_status()
    weather_data =response.json()

    # 地域名と天気情報を抜き出す
    area_name = weather_data[0]["timeSeries"][0]["areas"][1]["area"]["name"] # 南部
    today_weather = weather_data[0]["timeSeries"][0]["areas"][1]["weathers"][0] # 南部

    # 天気に記号をつける
    if "雷" in today_weather:
        today_weather += "⛈"
    elif "雪" in today_weather:
        today_weather += "⛄"
    elif "雨" in today_weather:
        today_weather += "⛈"
    elif "くもり" in today_weather and "晴れ" in today_weather:
        today_weather += "🌤のち曇り"
    elif "くもり" in today_weather:
        today_weather += "☁"
    elif "晴れ" in today_weather:
        today_weather += "☀"

    # LINEに送信するメッセージの作成
    line_message = f"【今日の天気】\n{now_time.month}月{now_time.day}日の埼玉県 {area_name}の天気は「{today_weather}です！」" 
    
    # LINEにメッセージを送信
    line_bot_api.push_message(USER_ID, TextSendMessage(text=line_message))
    print("LINEへの天気通知が成功しました")

# エラー処理
except Exception as e:
    print(f"エラーが発生しました：{e}")