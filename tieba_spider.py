import csv
import time
import requests
from lxml import etree

# 使用requests请求页面
def get_data():
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Cookie": "wise_device=0; Hm_lvt_98b9d8c2fd6608d564bf2ac2ae642948=1663230046; BAIDU_WISE_UID=wapp_1663230046203_651; USER_JUMP=-1; st_key_id=17; BCLID=7422895861104160722; BCLID_BFESS=7422895861104160722; BDSFRCVID=jhuOJeCT5G0GC0OjK9rsM3AIaMCs_PJTTPjcTR5qJ04BtyCVcgUJEG0PtDQqHgC-Hf9jogKKXgOTHwtF_2uxOjjg8UtVJeC6EG0Ptf8g0M5; BDSFRCVID_BFESS=jhuOJeCT5G0GC0OjK9rsM3AIaMCs_PJTTPjcTR5qJ04BtyCVcgUJEG0PtDQqHgC-Hf9jogKKXgOTHwtF_2uxOjjg8UtVJeC6EG0Ptf8g0M5; H_BDCLCKID_SF=tJCHoC8XtIvbfP0k-4QEbbQH-UnLq-T3bmOZ0lOmJl02sp8xXP6veJDyXHbCB4ou057dbpcmQUJ8HUb-jJQkD50Y5hrmLtJMQmQ4KKJxbpbGqqnTLIc1b6FqhUJiBhvMBan7L-bIXKohJh7FM4tW3J0ZyxomtfQxtNRJ0DnjtpChbRO4-TFMj6j0jf5; H_BDCLCKID_SF_BFESS=tJCHoC8XtIvbfP0k-4QEbbQH-UnLq-T3bmOZ0lOmJl02sp8xXP6veJDyXHbCB4ou057dbpcmQUJ8HUb-jJQkD50Y5hrmLtJMQmQ4KKJxbpbGqqnTLIc1b6FqhUJiBhvMBan7L-bIXKohJh7FM4tW3J0ZyxomtfQxtNRJ0DnjtpChbRO4-TFMj6j0jf5; BIDUPSID=17624EE312F2878E03F5ABB36DF5730E; PSTM=1663230047; BAIDUID=67051D48B82676E34BCEDF65D83C63C6:FG=1; H_PS_PSSID=36543_36885_34813_36570_36786_37317_26350_37277_37363_37234; BAIDUID_BFESS=67051D48B82676E34BCEDF65D83C63C6:FG=1; BDUSS=mVUWVhHbjdSd0d4MWdaVllURn5IQk5zRll-WC1HaVkzVjhvVUpkUll3WEtjRXBqRVFBQUFBJCQAAAAAAAAAAAEAAAChIkE1381kdW8AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAMrjImPK4yJjY; BDUSS_BFESS=mVUWVhHbjdSd0d4MWdaVllURn5IQk5zRll-WC1HaVkzVjhvVUpkUll3WEtjRXBqRVFBQUFBJCQAAAAAAAAAAAEAAAChIkE1381kdW8AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAMrjImPK4yJjY; STOKEN=b2e595b68ce72bf812f2cc7a3bee2932d5d312371388530b6125e98d1fdf31da; tb_as_data=1584b43812fda9c4b1f35a034196e6de5c0b692b95f928bf9bcf68b349dff4490eb726795be0439ca8ebcbf20b2fc82f928267db6fcc8027ff3d9fd99dd2d02c8eb4d4976f8eadcae744ba5eeef8acd1a9147214f7ce59542218c7d5f85c7445b23300e2703b190e0615676e25cf6e17; Hm_lpvt_98b9d8c2fd6608d564bf2ac2ae642948=1663230934; ab_sr=1.0.1_MGM5MmY1NmIyODZmZTI4NzhhODE1ZjM3MjlmZmRmYTBkMGEyYzlkNzVlMTczZTE2YzY5ZmE2OGI0OTVmMTA4ZGJkNDVkMWE0OTcwYjE0NmFhZjJlYzhiYTFjYTY3NjJkNzUxYWFjNTY4MDA2MTM4NGNiYTRkNWM0ZTAzNjliYzUzZWIyMDIzNDg4MzNmMzZlYjNlZDAzYmZjN2NhOWFiYjU1MGRlOWIxMDJlOTYwZmViMWNhYmNmZDI2NDU4NTE4; st_data=3192b3afd2938c7dd918158697b870dba4072247317141e2e73df2ed11845a9f562c766fdd8933312b36449dc9fac34c34f89bb5b5862e3e3a6e72926d0a54d2e272813001ee863a0dd3206e9482205921fcf660ac5b5e2868174c7ebb9a5a1f; st_sign=9ab54371; RT=\"z=1&dm=baidu.com&si=b49c0149-e83b-4ea7-b715-7e77b70f4f63&ss=l82s84cf&sl=e&tt=93b&bcn=https://fclog.baidu.com/log/weirwood?type=perf&ld=jfrk&nu=32qcf5p7&cl=jn3v&ul=jn3x\"",
        "Host": "tieba.baidu.com",
        "Pragma": "no-cache",
        "sec-ch-ua": "\"Microsoft Edge\";v=\"105\", \" Not;A Brand\";v=\"99\", \"Chromium\";v=\"105\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.33"
    }

    for page in range(1, pages + 1):  # 循环每一页
        print(f'正在爬取第{page}页...')
        params = {
            "pn": f"{page}"  # ?pn=XXX
        }
        r = requests.get(url, headers=headers, params=params)  # 请求页面
        r.encoding = r.apparent_encoding
        html = etree.HTML(r.text)
        divs = html.xpath('.//div[@id="j_p_postlist"]/div')
        for div in divs:
            name = div.xpath('.//ul[@class="p_author"]/li[@class="d_name"]/a/text()')
            date = div.xpath('.//div[@class="post-tail-wrap"]/span[5]/text()')
            floor = div.xpath('.//div[@class="post-tail-wrap"]/span[6]/text()')
            text = div.xpath('.//div[@class="p_content  "]/cc/div[2]//text()')
            all_text = ''
            # print(name, date, floor)
            if name and date and floor:
                for x in text: # 有服务器、id关键词的能判断的
                    all_text += x.replace(' ', '')
                    if x.count('服务器'):
                        fwq = x.replace('服务器', '').replace('服务器', '').replace(' ', '').replace('服务器名', '').replace(':', '').replace('：', '')
                    if x.count('ID') or x.count('id'):
                        name_id = x.replace('角色ID', '').replace('ID', '').replace(':', '').replace(' ', '')\
                            .replace('角色id', '').replace('id', '').replace('：', '')
                try:
                    with open('data_tieba.csv', 'a', encoding='utf-8-sig', newline='') as f:
                        writer = csv.writer(f)
                        writer.writerow([name[0], date[0], floor[0], all_text, fwq, name_id])
                    fwq = ''
                    name_id = ''
                except:
                    with open('data_tieba.csv', 'a', encoding='utf-8-sig', newline='') as f:
                        writer = csv.writer(f)
                        writer.writerow([name[0], date[0], floor[0], all_text])
        time.sleep(2)


if __name__ == '__main__':
    # csv header
    with open('data_tieba.csv', 'a', encoding='utf-8-sig', newline='') as c:
        writer = csv.writer(c)
        writer.writerow(["用户名", "楼层", "回复时间", "回复内容", "服务器", "角色id"])  # create csv header
    url = "https://tieba.baidu.com/p/7740003759"  # 链接
    pages = 12  # 总页数
    get_data()
