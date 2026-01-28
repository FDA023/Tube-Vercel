from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import requests
import random

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

    # --- قائمة سيرفرات بديلة (تعمل حالياً) ---
    # إذا توقف واحد، نستخدم الآخر
    servers = [
        "https://cobalt.kwiatekmiki.pl/api/json",
        "https://api.cobalt.bpj.li/api/json"
    ]
    
    # نختار سيرفر عشوائي لتوزيع الحمل
    api_url = random.choice(servers)

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

    try:
        # محاولة الاتصال بالسيرفر
        response = requests.post(api_url, json=payload, headers=headers)
        data = response.json()

        # التحقق من نجاح العملية
        if 'url' in data:
            return jsonify({
                "title": "تم جلب الفيديو بنجاح 🎥", 
                "thumbnail": "https://i.ytimg.com/vi/mqDf69j586s/maxresdefault.jpg", # صورة افتراضية
                "duration": "N/A",
                "video_url": data['url']
            })
        elif 'text' in data: # في حال وجود خطأ من المحرك
             return jsonify({"error": "Server Error: " + data['text']}), 500
        else:
             return jsonify({"error": "فشل جلب الرابط من السيرفر الخارجي"}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

