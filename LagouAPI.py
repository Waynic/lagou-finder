import urllib.parse

import requests
from bs4 import BeautifulSoup


class LagouAPI(object):
    LAGOU_GATEWAY = 'http://www.lagou.com/jobs/positionAjax.json?'
    sess = requests.Session()

    @classmethod
    def search(cls, kd, **kwargs):
        url_encoded = urllib.parse.urlencode(kwargs)
        cls.jl_url = cls.LAGOU_GATEWAY + url_encoded
        page = 1
        page_max = None
        while True:
            payload = {
                'first': False,
                'pn': page,
                'kd': kd,
            }
            r = cls.sess.post(cls.jl_url, data=payload)
            json_result = r.json()
            if page_max is None:
                page_max = json_result['content']['totalPageCount']
            for j in json_result['content']['result']:
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
