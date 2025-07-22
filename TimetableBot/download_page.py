import requests
import time


def download_page():
    headers = {
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36'}

    response = requests.get(
        "https://rasp.yandex.ru/suburban/universitetskaya-saint-petersburg-and-leningradskaya-oblast"
        "--sankt-peterburg-baltiyskiy/today", headers=headers)

    text = response.text

    f = open("page.html", "w")
    f.write(text)
    f.close()


def ticker():
    while True:
        dur = []
        now = time.localtime()
        if now.tm_hour < 4:
            dur.append(4 - (now.tm_hour + 1))
            dur.append(60 - (now.tm_min + 1))
            dur.append(60 - now.tm_sec)
        else:
            dur.append((24 - (now.tm_hour + 1)) + 4)
            dur.append(60 - (now.tm_min + 1))
            dur.append(60 - now.tm_sec)
        secs = dur[0] * 3600 + dur[1] * 60 + dur[2]
        time.sleep(secs)
        download_page()

ticker()