# import requests
# import datetime
#
# response = requests.post('https://edge.pse.com.ph/common/DisclosureCht.ax', json={
#     "cmpy_id": "29",
#     "security_id": "146",
#     "startDate": "05-15-2020",
#     "endDate": "12-31-2021"
# }, headers={
#     'Content-type': 'application/json',
#     'Accept': 'text/plain'
# })
# print(response.json()['chartData'])


from rq import Queue
from redis import Redis
from my_module import count_words_at_url
import time

# Tell RQ what Redis connection to use
redis_conn = Redis('localhost', 6379)
q = Queue(connection=redis_conn)  # no args implies the default queue

# print(q)

# # Delay execution of count_words_at_url('http://nvie.com')
job = q.enqueue(count_words_at_url, 'http://nvie.com')
print(job.result)  # => None  # Changed to job.return_value() in RQ >= 1.12.0
#
# # Now, wait a while, until the worker is finished
time.sleep(2)
print(job.result)  # => 889  # Changed to job.return_value() in RQ >= 1.12.0
