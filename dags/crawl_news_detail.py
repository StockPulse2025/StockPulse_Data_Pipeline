import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import time
from io import StringIO
import json
from datetime import datetime
import pytz
import os

headers_content = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
    'Referer': 'https://finance.naver.com',
}

def extract_news_image(soup):
    ogimg = soup.find('meta', property='og:image')
    if ogimg and ogimg.get('content'):
        return ogimg['content']
    return ""

def collect_daily_news(interval_start_date):
    data = """no	종목코드	종목명	분야	이미지URL
1	005930	삼성전자		https://static.toss.im/png-icons/securities/icn-sec-fill-005930.png
2	000660	SK하이닉스		https://static.toss.im/png-icons/securities/icn-sec-fill-000660.png
3	373220	LG에너지솔루션		https://static.toss.im/png-icons/securities/icn-sec-fill-373220.png
4	207940	삼성바이오로직스		https://static.toss.im/png-icons/securities/icn-sec-fill-207940.png
5	005380	현대차		https://static.toss.im/png-icons/securities/icn-sec-fill-005380.png
6	012450	한화에어로스페이스		https://static.toss.im/png-icons/securities/icn-sec-fill-012450.png
7	329180	HD현대중공업		https://static.toss.im/png-icons/securities/icn-sec-fill-329180.png
8	105560	KB금융		https://static.toss.im/png-icons/securities/icn-sec-fill-105560.png
9	000270	기아		https://static.toss.im/png-icons/securities/icn-sec-fill-000270.png
10	034020	두산에너빌리티		https://static.toss.im/png-icons/securities/icn-sec-fill-034020.png
11	068270	셀트리온		https://static.toss.im/png-icons/securities/icn-sec-fill-068270.png
12	035420	NAVER		https://static.toss.im/png-icons/securities/icn-sec-fill-035420.png
13	042660	한화오션		https://static.toss.im/png-icons/securities/icn-sec-fill-042660.png
14	055550	신한지주		https://static.toss.im/png-icons/securities/icn-sec-fill-055550.png
15	028260	삼성물산		https://static.toss.im/png-icons/securities/icn-sec-fill-028260.png
16	012330	현대모비스		https://static.toss.im/png-icons/securities/icn-sec-fill-012330.png
17	035720	카카오		https://static.toss.im/png-icons/securities/icn-sec-fill-035720.png
18	009540	HD한국조선해양		https://static.toss.im/png-icons/securities/icn-sec-fill-009540.png
19	032830	삼성생명		https://static.toss.im/png-icons/securities/icn-sec-fill-032830.png
20	005490	POSCO홀딩스		https://static.toss.im/png-icons/securities/icn-sec-fill-005490.png
21	086790	하나금융지주		https://static.toss.im/png-icons/securities/icn-sec-fill-086790.png
22	011200	HMM		https://static.toss.im/png-icons/securities/icn-sec-fill-011200.png
23	015760	한국전력		https://static.toss.im/png-icons/securities/icn-sec-fill-015760.png
24	051910	LG화학		https://static.toss.im/png-icons/securities/icn-sec-fill-051910.png
25	064350	현대로템		https://static.toss.im/png-icons/securities/icn-sec-fill-064350.png
26	000810	삼성화재		https://static.toss.im/png-icons/securities/icn-sec-fill-000810.png
27	138040	메리츠금융지주		https://static.toss.im/png-icons/securities/icn-sec-fill-138040.png
28	402340	SK스퀘어		https://static.toss.im/png-icons/securities/icn-sec-fill-402340.png
29	316140	우리금융지주		https://static.toss.im/png-icons/securities/icn-sec-fill-316140.png
30	267260	HD현대일렉트릭		https://static.toss.im/png-icons/securities/icn-sec-fill-267260.png
31	010140	삼성중공업		https://static.toss.im/png-icons/securities/icn-sec-fill-010140.png
32	033780	KT&G		https://static.toss.im/png-icons/securities/icn-sec-fill-033780.png
33	006400	삼성SDI		https://static.toss.im/png-icons/securities/icn-sec-fill-006400.png
34	096770	SK이노베이션		https://static.toss.im/png-icons/securities/icn-sec-fill-096770.png
35	010130	고려아연		https://static.toss.im/png-icons/securities/icn-sec-fill-010130.png
36	024110	기업은행		https://static.toss.im/png-icons/securities/icn-sec-fill-024110.png
37	259960	크래프톤		https://static.toss.im/png-icons/securities/icn-sec-fill-259960.png
38	034730	SK		https://static.toss.im/png-icons/securities/icn-sec-fill-034730.png
39	030200	KT		https://static.toss.im/png-icons/securities/icn-sec-fill-030200.png
40	079550	LIG넥스원		https://static.toss.im/png-icons/securities/icn-sec-fill-079550.png
41	066570	LG전자		https://static.toss.im/png-icons/securities/icn-sec-fill-066570.png
42	323410	카카오뱅크		https://static.toss.im/png-icons/securities/icn-sec-fill-323410.png
43	003550	LG		https://static.toss.im/png-icons/securities/icn-sec-fill-003550.png
44	017670	SK텔레콤		https://static.toss.im/png-icons/securities/icn-sec-fill-017670.png
45	018260	삼성에스디에스		https://static.toss.im/png-icons/securities/icn-sec-fill-018260.png
46	006800	미래에셋증권		https://static.toss.im/png-icons/securities/icn-sec-fill-006800.png
47	000150	두산		https://static.toss.im/png-icons/securities/icn-sec-fill-000150.png
48	272210	한화시스템		https://static.toss.im/png-icons/securities/icn-sec-fill-272210.png
49	086280	현대글로비스		https://static.toss.im/png-icons/securities/icn-sec-fill-086280.png
50	009150	삼성전기		https://static.toss.im/png-icons/securities/icn-sec-fill-009150.png
51	003230	삼양식품		https://static.toss.im/png-icons/securities/icn-sec-fill-003230.png
52	003670	포스코퓨처엠		https://static.toss.im/png-icons/securities/icn-sec-fill-003670.png
53	352820	하이브		https://static.toss.im/png-icons/securities/icn-sec-fill-352820.png
54	267250	HD현대		https://static.toss.im/png-icons/securities/icn-sec-fill-267250.png
55	000100	유한양행		https://static.toss.im/png-icons/securities/icn-sec-fill-000100.png
56	047810	한국항공우주		https://static.toss.im/png-icons/securities/icn-sec-fill-047810.png
57	010120	LS ELECTRIC		https://static.toss.im/png-icons/securities/icn-sec-fill-010120.png
58	005830	DB손해보험		https://static.toss.im/png-icons/securities/icn-sec-fill-005830.png
59	443060	HD현대마린솔루션		https://static.toss.im/png-icons/securities/icn-sec-fill-443060.png
60	003490	대한항공		https://static.toss.im/png-icons/securities/icn-sec-fill-003490.png
61	047050	포스코인터내셔널		https://static.toss.im/png-icons/securities/icn-sec-fill-047050.png
62	042700	한미반도체		https://static.toss.im/png-icons/securities/icn-sec-fill-042700.png
63	090430	아모레퍼시픽		https://static.toss.im/png-icons/securities/icn-sec-fill-090430.png
64	377300	카카오페이		https://static.toss.im/png-icons/securities/icn-sec-fill-377300.png
65	071050	한국금융지주		https://static.toss.im/png-icons/securities/icn-sec-fill-071050.png
66	010620	HD현대미포		https://static.toss.im/png-icons/securities/icn-sec-fill-010620.png
67	000880	한화		https://static.toss.im/png-icons/securities/icn-sec-fill-000880.png
68	021240	코웨이		https://static.toss.im/png-icons/securities/icn-sec-fill-021240.png
69	000720	현대건설		https://static.toss.im/png-icons/securities/icn-sec-fill-000720.png
70	326030	SK바이오팜		https://static.toss.im/png-icons/securities/icn-sec-fill-326030.png
71	180640	한진칼		https://static.toss.im/png-icons/securities/icn-sec-fill-180640.png
72	010950	S-Oil		https://static.toss.im/png-icons/securities/icn-sec-fill-010950.png
73	064400	LG씨엔에스		https://static.toss.im/png-icons/securities/icn-sec-fill-003550.png
74	278470	에이피알		https://static.toss.im/png-icons/securities/icn-sec-fill-278470.png
75	005940	NH투자증권		https://static.toss.im/png-icons/securities/icn-sec-fill-005940.png
76	032640	LG유플러스		https://static.toss.im/png-icons/securities/icn-sec-fill-032640.png
77	016360	삼성증권		https://static.toss.im/png-icons/securities/icn-sec-fill-016360.png
78	029780	삼성카드		https://static.toss.im/png-icons/securities/icn-sec-fill-029780.png
79	161390	한국타이어앤테크놀로지		https://static.toss.im/png-icons/securities/icn-sec-fill-161390.png
80	034220	LG디스플레이		https://static.toss.im/png-icons/securities/icn-sec-fill-034220.png
"""

    df = pd.read_csv(StringIO(data), sep='\t', skipinitialspace=True)
    df["종목코드"] = df["종목코드"].astype(str).str.zfill(6)
    df["종목명"] = df["종목명"].str.strip()

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        'Referer': 'https://finance.naver.com',
    }

    all_news = []

    for _, row in df.iterrows():
        item_code = str(row['종목코드'])
        stock_name = row['종목명']
        sector = row['분야']

        print(f"▶ {stock_name}({item_code}) 뉴스 수집 중...")

        stop_page_loop = False

        for page in range(1, 200):
            if stop_page_loop:
                    break
            url = (
                f'https://finance.naver.com/item/news_news.nhn'
                f'?code={item_code}&page={page}'
                '&sm=title_entity_id.basic&clusterId='
            )
            print(f"Fetching page {page} for {stock_name}...")
            res = requests.get(url, headers=headers)
            res.encoding = 'euc-kr'
            soup = BeautifulSoup(res.text, 'html.parser')
            tr_list = soup.find_all('tr', {'class': 'relation_tit'})
            for tr in tr_list:
                title_td = tr.find('td', class_='title')
                info_td = tr.find('td', class_='info')
                date_td = tr.find('td', class_='date')

                if title_td is None:
                    continue

                a_tag = title_td.find('a')
                if a_tag is None:
                    continue
                
                title = a_tag.get_text(strip=True)
                link = 'https://finance.naver.com' + a_tag['href']
                info = info_td.get_text(strip=True) if info_td else ''
                date = date_td.get_text(strip=True) if date_td else ''
                kst_dt = datetime.fromisoformat(interval_start_date).astimezone(pytz.timezone("Asia/Seoul")).strftime("%Y.%m.%d %H:%M")

                print(date, kst_dt, date < kst_dt)
                if date < kst_dt:
                    stop_page_loop = True
                    break

                all_news.append({
                    'title': title,
                    'link': link,
                    'info': info,
                    'date': date,
                    'stock_code': str(item_code),
                    'stock_name': stock_name,
                    'sector': sector,
                })

            time.sleep(0.5)  # 과도한 요청 방지용 대기

    df_news = pd.DataFrame(all_news)
    print(f"\n✅ 총 뉴스 수집 건수: {len(df_news)}건")
    print(df_news.head())

    s3_path = f's3://stockplus-datalake/news-list/{interval_start_date}.csv'
    df_news.to_csv(s3_path, index=False, storage_options={
            "key": os.getenv("AWS_ACCESS_KEY_ID"),
            "secret": os.getenv("AWS_SECRET_ACCESS_KEY"),
        })

def get_article_content(url):
    try:
        res = requests.get(url, headers=headers_content)
        res.encoding = 'utf-8'
        html = res.text

        if "top.location.href=" in html:
            match = re.search(r"top\.location\.href='(.*?)'", html)
            if match:
                redirect_url = match.group(1)
                res = requests.get(redirect_url, headers=headers_content)
                res.encoding = 'utf-8'
                html = res.text
            else:
                return None, None  # 본문 영역 못 찾으면 빈 값 반환

        soup = BeautifulSoup(html, 'html.parser')
        news_image = extract_news_image(soup)

        selectors = [
            'article#dic_area',
            'div#contents',
            'div#newsct_article',
            'div._news_article',
        ]

        for sel in selectors:
            content_tag = soup.select_one(sel)
            if content_tag and content_tag.get_text(strip=True):
                return content_tag.get_text(separator='\n', strip=True), news_image
        return None, news_image
    
    except Exception as e:
        print(f"본문 추출 중 에러 발생: {e}")
        return None, news_image


def collect_daily_news_detail(interval_start_date):
    source_s3_path = f's3://stockplus-datalake/news-list/{interval_start_date}.csv'
    target_s3_path = f's3://stockplus-datalake/news/{interval_start_date}.csv'

    df = pd.read_csv(source_s3_path, storage_options={
        "key": os.getenv("AWS_ACCESS_KEY_ID"),
        "secret": os.getenv("AWS_SECRET_ACCESS_KEY"),
    })

    for idx, news in df.iterrows(): 
        url = news['link']

        if isinstance(url, str) and url.startswith('[') and ']' in url:
            url = url[url.find('](')+2:-1]

        print(f"본문 크롤링 중: {url}")
        content, news_image = get_article_content(url)
        df.at[idx, 'content'] = content
        df.at[idx, 'newsImage'] = news_image 
        time.sleep(0.3)

    df.to_csv(target_s3_path, index=False, storage_options={
            "key": os.getenv("AWS_ACCESS_KEY_ID"),
            "secret": os.getenv("AWS_SECRET_ACCESS_KEY"),
        })
    df.to_csv(f"./{interval_start_date}.csv", index=False)

def df_to_news_payload(df):
    news_data = []
    for _, row in df.iterrows():
        item = {
            "newsTitle": row["title"],
            "newsUrl": row["link"],
            "newsImage": row["newsImage"],
            "press": row["info"],
            "content": row["content"],
            "reason": row.get("description", "해당 이유는 자세히 제공되지 않습니다."),
            "publishedDate": datetime.strptime(row["date"], '%Y.%m.%d %H:%M').isoformat(),
            "relatedStocks": [{
                "stockName": row["stock_name"],
                "symbol": str(row["stock_code"]),
                "influenceScore": row.get("prediction", 0)
            }]
        }
        news_data.append(item)
    print("ttt", json.dumps({"newsDataList": news_data}, ensure_ascii=False, indent=2))
    return {"newsDataList": news_data}

def upload_daily_news_result(interval_start_date):
    s3_path = f's3://stockplus-datalake/news-result/{interval_start_date}.csv'

    df = pd.read_csv(f'./output/{interval_start_date}.csv')

    print("df 앞 부분", df.head())
    payload = df_to_news_payload(df)
    payload_df = pd.DataFrame(payload)
    payload_df.to_csv(s3_path, index=False, storage_options={
        "key": os.getenv("AWS_ACCESS_KEY_ID"),
        "secret": os.getenv("AWS_SECRET_ACCESS_KEY"),
    })

    url = "https://stockpulse.p-e.kr//api/v1/news/pipeline/batch"
    headers = {"Content-Type": "application/json"}
    print("payload", json.dumps(payload, ensure_ascii=False))
    print(pd.DataFrame(payload))
    response = requests.post(url, json=payload, headers=headers)

    print(response.status_code)
    print(response.json())

    # payload.to_csv(s3_path, index=False, storage_options={
    #         "key": os.getenv("AWS_ACCESS_KEY_ID"),
    #         "secret": os.getenv("AWS_SECRET_ACCESS_KEY"),
    # })
