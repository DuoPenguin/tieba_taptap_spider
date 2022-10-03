import time
import requests
import pandas as pd
import unicodedata

def get_data():
    headers = {
        "authority": "www.taptap.com",
        "accept": "application/json, text/plain, */*",
        "accept-language": "zh-CN,zh;q=0.9",
        "cookie": "acw_tc=2760828616632202804105681e1131b120589bf0035ca8ec4df1980ff6a256; locale=zh_CN; tap_theme=light; _gid=GA1.2.22276199.1663220281; _ga_6G9NWP07QM=GS1.1.1663220281.1.0.1663220281.0.0.0; _ga=GA1.1.1763977524.1663220281; XSRF-TOKEN=eyJpdiI6ImxnVEFOUXJZK0NyaGFRYzJlRDdtZHc9PSIsInZhbHVlIjoiY1wvZnBISUxqZUpUV01RZGNsNEpvczJcLzJnXC9YSktQRWYyTXNrM0d6dGpaaEphc2NJbG1iekRQc3FBSU9HSHJhTTB5NEliZFVPdDFDZDVWbkF6WDBjdUE9PSIsIm1hYyI6IjRmYWQzMGY1MjNlNjlmNzcwMzJiZmU1YmE0MjczYzdjMzBjZGQwODdmNmY0MDhhNDkwMWFiMDlkNTFhNzQzZDYifQ%3D%3D; tap_sess=eyJpdiI6ImUyU3ExS2tUUDZ1RHo4K0xyYkluY3c9PSIsInZhbHVlIjoiMG9XYlQ2WlNrQVwvK0F1d2tnQm0zNWZMU1dCYkVWNG5IcXhCZ3E4NXF3ZDdsNWpMNkttQjZDc3RLeE1pc1N2MjZMS2hoWHhhQVhLWkhlbE5VNytpY1VRPT0iLCJtYWMiOiJhNjYyZTVkZTllMDY5YjFlYzljNjEzMjZkNzA0ODg2Y2E2NjkwNjNiZGIzM2M5MzQ3MGU4NWEyNzMxNzBkZjgyIn0%3D",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
        "x-requested-with": "XMLHttpRequest",
        "x-xsrf-token": "eyJpdiI6ImxnVEFOUXJZK0NyaGFRYzJlRDdtZHc9PSIsInZhbHVlIjoiY1wvZnBISUxqZUpUV01RZGNsNEpvczJcLzJnXC9YSktQRWYyTXNrM0d6dGpaaEphc2NJbG1iekRQc3FBSU9HSHJhTTB5NEliZFVPdDFDZDVWbkF6WDBjdUE9PSIsIm1hYyI6IjRmYWQzMGY1MjNlNjlmNzcwMzJiZmU1YmE0MjczYzdjMzBjZGQwODdmNmY0MDhhNDkwMWFiMDlkNTFhNzQzZDYifQ==",
    }
    #csv header
    df1 = pd.DataFrame(columns=['用户名', '楼层', '回复内容', '回复时间','服务器','角色id']) #pandas表格结构
    for p in range(21):
        print('正在爬取第' + str(p+1) + '页')
        params = (
            ("from", str(p * 10)),
            ("limit", "10"),
            ("order", "desc"),
            ("sort", "rank"),
            ("topic_id", "20238820"),
            ("X-UA",
             "V=1&PN=WebApp&LANG=zh_CN&VN_CODE=90&VN=0.1.0&LOC=CN&PLT=PC&DS=Android&UID=7e2395b1-0439-4911-b831-161089037aeb&DT=PC&OS=macOS&OSV=12.1.0"),
        )

        r = requests.get("https://www.taptap.com/webapiv2/post/v3/by-topic", headers=headers, params=params)

        for i in range(10):
            try:#taptap好像和贴吧不一样是动态数据所以尝试json
                name = r.json()['data']['list'][i]['author']['name']
                position = r.json()['data']['list'][i]['position']
                raw_text = r.json()['data']['list'][i]['contents']['raw_text']
                create_time = r.json()['data']['list'][i]['create_time']
                text = unicodedata.normalize('NFKC',raw_text)

                #关键词筛选替换，储存的数据和贴吧的不一样，尝试用splitlines一行一行判断
                for line in text.splitlines():
                    if line.count('服务器'):
                        fwq = line.replace('服务器', '').replace('服务器', '').replace(' ', '').replace('服务器名', '').replace(':', '').replace('：', '')
                    if line.count('ID'):
                        name_id = line.replace('角色ID', '').replace('ID', '').replace(':', '').replace(' ', '')\
                            .replace('角色id', '').replace('id', '').replace('：', '')


                try:
                    data = {'用户名': [name], '楼层': [position], '回复内容': [raw_text], '回复时间': [create_time],'服务器':fwq,'角色id':name_id}
                    fwq = ''
                    name_id = ''
                except:
                    data = {'用户名': [name], '楼层': [position], '回复内容': [raw_text], '回复时间': [create_time]}

                d1 = pd.DataFrame(data)
                df1 = pd.concat([df1, d1], axis=0).reset_index(drop=True)#连接df1，d1
            except:
                continue
    time.sleep(3)
    #date format
    df1['回复时间'] = df1['回复时间'].apply(
        lambda x: time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(x))))#将日期时间转换为字符串
    #print(df1)
    df1.to_csv('data_tap.csv', encoding='utf-8_sig', index=False)


if __name__ == '__main__':

    get_data()
