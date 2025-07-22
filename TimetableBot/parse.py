from bs4 import BeautifulSoup


def get_trains() -> str:
    f = open("page.html")
    text = f.read()
    f.close()

    timetable = []
    soup = BeautifulSoup(text, "html.parser")

    date = soup.find('span', class_='SearchTitle__subtitle')
    blocks = soup.find_all('tr', class_='SearchSegment SearchSegments__segment')


    timetable.append(f'{date.text}\n')
    timetable.append("==================================================\n")
    for train in blocks:
        params = []
        name = train.find('h3', class_='SegmentTitle__title')
        type_of_train = train.find('span', class_='SegmentTransport__item SegmentTransport__item_subtype')
        arrive_time = train.find_all('span', class_='TableTimeAndStations__time')
        dur = train.find('div', class_='TableDuration')
        price = train.find('span', class_='Price TariffsListItem__price')
        params.append(f'{name.text} ')
        if type_of_train is not None:
            params.append(f"{type_of_train.text} ")
        for s in arrive_time:
            params.append(f"{s.text} \n")
        params.append(f"{dur.text} \n")
        params.append(f"{price.text} \n")
        params.append("==================================================\n")
        for train in params:
            timetable.append(train)
    return "".join(params for params in timetable)
