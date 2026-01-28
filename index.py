from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return send_file('index.html')

@app.route('/get-info', methods=['GET'])
def get_video_info():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "No URL provided"}), 400

    # --- قائمة السيرفرات القوية (نظام الطوارئ) ---
    # سيقوم الكود بتجربتها بالترتيب
    cobalt_instances = [
        "https://api.cobalt.bpj.li/api/json",      # سيرفر 1 (سريع)
        "https://cobalt.pub/api/json",             # سيرفر 2 (عام)
        "https://cobalt.kwiatekmiki.pl/api/json",  # سيرفر 3 (احتياطي)
    ]

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    payload = {
        "url": url,
        "vQuality": "720",
        "filenamePattern": "basic"
    }

    # حلقة تكرار لتجربة السيرفرات واحداً تلو الآخر
    for api_url in cobalt_instances:
        try:
            print(f"Trying server: {api_url}") # للتوضيح في السجلات
            response = requests.post(api_url, json=payload, headers=headers, timeout=10)
            data = response.json()

            # إذا نجح السيرفر وأعطانا رابطاً، نوقف البحث ونرسل النتيجة
            if 'url' in data:
                return jsonify({
                    "title": "تم جلب الفيديو بنجاح 🎥",
                    "thumbnail": "https://i.ytimg.com/vi/mqDf69j586s/maxresdefault.jpg",
                    "video_url": data['url']
                })
            
            # إذا رد السيرفر بخطأ، نجرب التالي
            continue 

        except Exception as e:
            # إذا كان السيرفر طافياً، نجرب التالي فوراً
            continue

    # إذا جربنا كل السيرفرات وفشلت كلها
    return jsonify({"error": "جميع السيرفرات مشغولة حالياً، حاول بعد دقيقة! 😔"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

