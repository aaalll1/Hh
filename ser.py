import os
import time
import schedule
import requests
import logging
from flask import Flask
from flask_restful import Resource, Api
from threading import Thread

# إعداد تسجيل الأخطاء
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)
api = Api(app)

class Greeting(Resource):
    def get(self):
        return "𝗦𝗰𝗼𝗿𝗽𝗶𝗼 𝘄𝗼𝗿𝗸𝘀 𝘀𝘂𝗰𝗰𝗲𝘀𝘀𝗳𝘂𝗹𝗹𝘆 ✅"

api.add_resource(Greeting, '/')

def visit_site():
    url = f"http://localhost:{os.environ.get('PORT', 10000)}"
    try:
        response = requests.get(url)
        logger.info(f"Visited {url} - Status Code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to visit {url} - Error: {e}")

# جدولة المهمة لتعمل كل 3 دقائق
schedule.every(3).minutes.do(visit_site)

def run_flask_app():
    try:
        app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)), threaded=True)
    except Exception as e:
        logger.error(f"Failed to start Flask server - Error: {e}")

if __name__ == "__main__":
    # تشغيل خادم Flask في خيط منفصل
    flask_thread = Thread(target=run_flask_app)
    flask_thread.start()
    logger.info("Flask server started.")
    
    # الانتظار بضع ثواني للتأكد من أن خادم Flask قد بدأ
    time.sleep(5)
    
    # تشغيل المجدول
    while True:
        schedule.run_pending()
        time.sleep(1)
