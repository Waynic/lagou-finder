import urllib.parse

import requests
from bs4 import BeautifulSoup


class LagouAPI(object):
    LAGOU_GATEWAY = 'http://www.lagou.com/jobs/positionAjax.json?'
    sess = requests.Session()

    @classmethod
    def search(cls, kd, **kwargs):
        """

        :param kd: 关键字
        :param kwargs: 其他参数
        :return:
        """
        # 对url参数进行编码
        url_encoded = urllib.parse.urlencode(kwargs)
        # 拼接url
        cls.jl_url = cls.LAGOU_GATEWAY + url_encoded
        page = 1
        page_max = None
        while True:
            payload = {
                'first': False,
                'pn': page,
                'kd': kd,
            }
            # 请求结果
            r = cls.sess.post(cls.jl_url, data=payload)
            # 对返回的结果进行JSON序列化
            json_result = r.json()
            if page_max is None:
                # 获得页数
                # page_max = json_result['content']['totalPageCount']
                # 拉钩返回的数据比之前多了一层'positionResult'，并且字段名也由totalPageCount变为totalCount
                page_max = json_result['content']['positionResult']['totalCount']
            # 用生成器返回得到的结果
            # for j in json_result['content']['result']:
            # 拉钩返回的数据比之前多了一层'positionResult'
            for j in json_result['content']['positionResult']['result']:
                yield j
            if page >= page_max:
                break
            page += 1

    @classmethod
    def get_location_by_pos_id(cls, pos_id):
        r = cls.sess.get('http://www.lagou.com/jobs/%d.html' % pos_id)
        soup = BeautifulSoup(r.content, 'html.parser')
        corp_info = soup.select('#container > div.content_r > dl > dd')[0]
        return corp_info.div.contents[0]
