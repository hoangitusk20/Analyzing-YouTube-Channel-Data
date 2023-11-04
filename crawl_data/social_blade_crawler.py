import pandas as pd
from bs4 import BeautifulSoup
from selenium.webdriver import Chrome, ChromeOptions
import re
import json
import os
import ThreadPoolExecutorPlus
import numpy as np
import time
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import requests

BASE_URL = 'https://socialblade.com'
NUMBER_OF_THREADS = 1


def driver_setup():
    options = ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--blink-settings=imagesEnabled=false")
    options.add_argument("--log-level=3")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--ignore-ssl-errors")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    try:
        caps = DesiredCapabilities().CHROME
        caps["pageLoadStrategy"] = "eager"
        driver = Chrome(desired_capabilities=caps, options=options)
    except:
        driver = Chrome(options=options)

    return driver


def get_country_list():
    f = open('./country_list.json')
    data = json.load(f)
    f.close()

    return data


def get_channel_list_by_country(country):
    driver = driver_setup()

    url = f'{BASE_URL}/youtube/top/country/{country}'

    channel_list = []

    driver.get(url)
    html = driver.page_source.encode('utf-8')
    soup = BeautifulSoup(html, 'html.parser')

    regexp = re.compile(r'/youtube/channel/*')
    for a in soup.select('a[href]'):
        if regexp.search(a['href']):
            _, _, id = a['href'].partition('/youtube/channel/')
            channel_list.append(id)

    return channel_list


def get_channel_list(path):
    country_list = get_country_list()

    if not os.path.exists(path):
        channel_list = []

        for country in country_list:
            channel_list.extend(get_channel_list_by_country(country))

        with open(path, 'w', encoding='utf-8') as f:
            json.dump(channel_list, f, ensure_ascii=False, indent=4)

        return channel_list

    f = open(path)
    channel_list = json.load(f)
    f.close()

    return channel_list


def get_channel_data(channel_id, driver=None):
    url = f'{BASE_URL}/youtube/channel/{channel_id}'

    response = requests.get(url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
    })
    response.encoding = 'utf-8'
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')

    data = {}

    numeric_columns = ['uploads', 'subscribers', 'video_views', 'social_blade_rank', 'subscriber_rank', 'video_views_rank', 'country_rank', 'channel_type_rank', 'subscribers_last_30_days',
                       'video_views_last_30_days', 'estimated_monthly_earnings_min', 'estimated_monthly_earnings_max', 'estimated_yearly_earnings_min', 'estimated_yearly_earnings_max']

    data['channel_id'] = channel_id

    try:
        data['channel_name'] = soup.select_one(
            '#YouTubeUserTopInfoBlockTop > div:nth-child(1) > h1').string
    except:
        data['channel_name'] = None

    try:
        data['uploads'] = soup.select_one(
            '#YouTubeUserTopInfoBlock > div:nth-child(2) > span:nth-child(3)').string
    except:
        data['uploads'] = None

    try:
        data['subscribers'] = soup.select_one(
            '#YouTubeUserTopInfoBlock > div:nth-child(3) > span:nth-child(3)').string
    except:
        data['subscribers'] = None

    try:
        data['video_views'] = soup.select_one(
            '#YouTubeUserTopInfoBlock > div:nth-child(4) > span:nth-child(3)').string
    except:
        data['video_views'] = None

    try:
        data['country'] = soup.select_one('#youtube-user-page-country').string
    except:
        data['country'] = None

    try:
        data['channel_type'] = soup.select_one(
            '#youtube-user-page-channeltype').string
    except:
        data['channel_type'] = None

    try:
        data['user_created'] = soup.select_one(
            '#YouTubeUserTopInfoBlock > div:nth-child(7) > span:nth-child(3)').string
    except:
        data['user_created'] = None

    try:
        data['total_grade'] = soup.select_one(
            '#socialblade-user-content > div:nth-child(1) > div:nth-child(1) > div:nth-child(1)').string
    except:
        data['total_grade'] = None

    try:
        data['social_blade_rank'] = soup.select_one(
            '#socialblade-user-content > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > p > span').string
    except:
        data['social_blade_rank'] = None

    try:
        data['subscriber_rank'] = soup.select_one(
            '#socialblade-user-content > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > p > span').string
    except:
        data['subscriber_rank'] = None

    try:
        data['video_views_rank'] = soup.select_one(
            '#socialblade-user-content > div:nth-child(1) > div:nth-child(2) > div:nth-child(3) > div:nth-child(1) > p > span').string
    except:
        data['video_views_rank'] = None

    try:
        data['country_rank'] = soup.select_one(
            '#socialblade-user-content > div:nth-child(1) > div:nth-child(2) > div:nth-child(4) > div:nth-child(1) > p > span').string
    except:
        data['country_rank'] = None

    try:
        data['channel_type_rank'] = soup.select_one(
            '#socialblade-user-content > div:nth-child(1) > div:nth-child(2) > div:nth-child(5) > div:nth-child(1) > p > span').string
    except:
        data['channel_type_rank'] = None

    try:
        data['subscribers_last_30_days'] = soup.select_one(
            '#socialblade-user-content > div:nth-child(3) > div:nth-child(1) > p:nth-child(1)').contents[0]
    except:
        data['subscribers_last_30_days'] = None

    try:
        data['video_views_last_30_days'] = soup.select_one(
            '#socialblade-user-content > div:nth-child(3) > div:nth-child(3) > p:nth-child(1)').contents[0]
    except:
        data['video_views_last_30_days'] = None

    try:
        data['estimated_monthly_earnings'] = soup.select_one(
            '#socialblade-user-content > div:nth-child(3) > div:nth-child(2) > p:nth-child(1)').string
    except:
        data['estimated_monthly_earnings'] = None

    try:
        data['estimated_yearly_earnings'] = soup.select_one(
            '#socialblade-user-content > div:nth-child(5) > div:nth-child(1) > div:nth-child(2) > p:nth-child(1)').string
    except:
        data['estimated_yearly_earnings'] = None

    data['estimated_monthly_earnings_min'] = None
    data['estimated_monthly_earnings_max'] = None
    data['estimated_yearly_earnings_min'] = None
    data['estimated_yearly_earnings_max'] = None

    try:
        for key, value in data.items():
            if value:
                data[key] = value.strip()

                if key == 'estimated_monthly_earnings':
                    x = re.split(r" \xa0-\xa0 ", value)
                    data['estimated_monthly_earnings_min'] = x[0]
                    data['estimated_monthly_earnings_max'] = x[1]

                if key == 'estimated_yearly_earnings':
                    x = re.split(r" \xa0-\xa0 ", value)
                    data['estimated_yearly_earnings_min'] = x[0]
                    data['estimated_yearly_earnings_max'] = x[1]

                if key in numeric_columns:
                    count = len(value.partition(".")[2]) - 1

                    value = re.sub("K", "000", value)
                    value = re.sub("M", "000000", value)
                    value = re.sub("B", "000000000", value)
                    if '.' in value:
                        value = value[:-count]

                    value = re.sub("[^0-9]", "", value)
                    if value == '':
                        value = None
                    else:
                        value = int(value)

                    data[key] = value
    except Exception as e:
        print(f"Error {str(e)} - {channel_id}")

    return data


def crawler(channel_list, driver):
    res = []

    for i, channel in enumerate(channel_list):
        print(f"{i} - Crawling {channel} ...")
        res.append(get_channel_data(channel, driver))

        pd.DataFrame(res).to_csv(f"./final-data/data.csv", index=0)

        time.sleep(0.5)

        if (i + 1) % 1000 == 0:
            time.sleep(900)

    return res


def split_file(file, dest, n):
    f = open(file)
    channel_list = json.load(f)
    f.close()

    chunks = np.array_split(channel_list, n)
    for i in range(len(chunks)):
        with open(f'{dest}/channel_list_{i}.json', 'w', encoding='utf-8') as f:
            json.dump(chunks[i].tolist(), f, ensure_ascii=False, indent=4)


def merge_output_files(src, dest, n):
    df = pd.DataFrame()
    for i in range(1, n):
        i_df = pd.read_csv(f'{src}/data_{i}.csv')
        df = pd.concat([df, i_df])
    df.to_csv(dest, index=0)


if __name__ == '__main__':
    # output_path = f'./final-data'

    # path = f'./channel_list/channel_list.json'

    # channel_list = get_channel_list(path)

    # drivers = [driver_setup() for _ in range(NUMBER_OF_THREADS)]
    # chunks = np.array_split(channel_list, NUMBER_OF_THREADS)

    # with ThreadPoolExecutorPlus.ThreadPoolExecutor(max_workers=NUMBER_OF_THREADS,) as executor:
    #     bucket = executor.map(crawler, chunks, drivers)
    #     results = [item for block in bucket for item in block]

    # [driver.quit() for driver in drivers]

    merge_output_files('data', 'data/data.csv', 3)
