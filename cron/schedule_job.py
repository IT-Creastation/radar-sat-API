import schedule
import time
import requests
from dotenv import load_dotenv
import os
load_dotenv()


def job():
    try:
        response = requests.post(
            os.getenv("LOCAL")+"/run",
            data={'key': 'value'})
        print(response.status_code, response.text)
    except Exception as ex:
        print(ex)


schedule.every(5).seconds.do(job)

# schedule.every().day.at("10:30").do(job)


while True:
    schedule.run_pending()
    time.sleep(1)
