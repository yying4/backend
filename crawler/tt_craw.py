import db_mongo
from concurrent.futures import ThreadPoolExecutor, wait, FIRST_COMPLETED, ALL_COMPLETED, as_completed
import time


def first_out(a):
    a = '请等待5分钟'
    return a

def test_sec(cid):
    web_bv = db_mongo.html_str(cid) + cid
    time.sleep(3)
    print('------------')
    print('爬完了~')
    return web_bv





def main_func(cid):
    with ThreadPoolExecutor(max_workers=3) as t:
        all_task = []
        obj1 = t.submit(first_out,1)
        obj2 = t.submit(test_sec, cid)
        all_task = [obj1,obj2]
        #wait(all_task, return_when=FIRST_COMPLETED)

        for future in as_completed(all_task):
            data = future.result()
            #print(data)
    return data

#cid = "1c00e9fa-339e-11eb-9563-f8b314a037d3"
#d=main_func(cid)
#print(d)



