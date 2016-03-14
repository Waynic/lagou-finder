#!/usr/bin/python3
import queue
import threading
import uuid

from BaiduMapAPI import BaiduMapAPI
from LagouAPI import LagouAPI
from JobDB import db, Job

jq = queue.Queue()
lock = threading.Lock()
done = False


def geo_worker():
    while True:
        try:
            jd = jq.get(timeout=1)
        except queue.Empty:
            with lock:
                if done:
                    break
            continue
        address = LagouAPI.get_location_by_pos_id(jd['positionId'])
        gis = BaiduMapAPI.search('上海', address)
        job = Job(str(uuid.uuid1()))
        job.company_name = jd['companyName']
        job.location = address
        job.ctime = jd['createTimeSort']
        job.salary = jd['salary']
        job.company_size = jd['companySize']
        job.field = jd['industryField']
        job.stage = jd['financeStage']
        job.title = jd['positionName']
        job.jid = jd['positionId']

        if gis:
            loc = gis[0]['location']
            job.lat, job.lng = loc['lat'], loc['lng']
            if 'address' in gis[0]:
                job.gis_loc = gis[0]['address']

        db.session.add(job)
        db.session.commit()

geo_thread = threading.Thread(target=geo_worker)
geo_thread.start()


def main():
    global done
    try:
        for jd in LagouAPI.search('PHP', city='上海', gx='全职', yx='21k-50k'):
            jq.put(jd)
        with lock:
            done = True
        geo_thread.join()
    except Exception as e:
        print(e.with_traceback())


if __name__ == '__main__':
    main()

