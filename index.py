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

    # --- القائمة الجديدة (سيرفرات 2025 النشطة) ---
    # تم اختيارها بعناية لتعمل مع Vercel
    cobalt_instances = [
        "https://cobalt.minaev.su/api/json",      # سيرفر روسي قوي وسريع
        "https://cobalt.ayo.tf/api/json",         # سيرفر مجتمعي مستقر
        "https://api.cobalt.tools/api/json",      # السيرفر الرسمي (الخيار الآمن)
        "https://co.wuk.sh/api/json",             # السيرفر الأصلي (الاحتياطي)
    ]
    
    # خلط القائمة عشوائياً في كل مرة لتوزيع الحمل
    random.shuffle(cobalt_instances)

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Origin": "https://tube-vercel.vercel.app",
        "Referer": "https://tube-vercel.vercel.app/"
    }

    payload = {
        "url": url,
        "vQuality": "720",
        "filenamePattern": "basic"
    }

    print(f"Checking URL: {url}")

    # المحاولة مع السيرفرات
    for api_url in cobalt_instances:
        try:
            print(f"Trying server: {api_url} ...")
            # قللنا الوقت لـ 4 ثواني فقط لكل سيرفر لكي لا يعلق الموقع
            response = requests.post(api_url, json=payload, headers=headers, timeout=4)
            
            try:
                data = response.json()
            except:
                print(f"Failed to parse JSON from {api_url}")
                continue

            # التحقق من النجاح
            if 'url' in data:
                print(f"Success with {api_url}!")
                return jsonify({
                    "title": "تم جلب الفيديو بنجاح 🎥",
                    "thumbnail": "https://i.ytimg.com/vi/mqDf69j586s/maxresdefault.jpg",
                    "video_url": data['url']
                })
            
            if 'text' in data:
                 print(f"Server Error from {api_url}: {data['text']}")
            
        except Exception as e:
            print(f"Connection Failed to {api_url}: {str(e)}")
            continue

    return jsonify({"error": "للأسف، جميع السيرفرات مشغولة حالياً. حاول بعد قليل! 😔"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

