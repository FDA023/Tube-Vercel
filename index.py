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

    # --- القائمة الذهبية للسيرفرات (تعمل بنظام التتابع) ---
    # إذا مات واحد، يحيي الآخر!
    cobalt_instances = [
        "https://co.wuk.sh/api/json",             # السيرفر الأصلي (الأقوى)
        "https://cobalt.gwoa.at/api/json",        # سيرفر نمساوي سريع
        "https://cobalt.synced.team/api/json",    # سيرفر احتياطي 1
        "https://api.cobalt.cwinfo.net/api/json", # سيرفر احتياطي 2
        "https://cobalt.junker.ddns.net/api/json",# سيرفر احتياطي 3
        "https://api.cobalt.tools/api/json"       # السيرفر الرسمي (أحياناً مغلق)
    ]

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

    # حلقة المحاولة المستميتة
    for api_url in cobalt_instances:
        try:
            print(f"Trying server: {api_url} ...") 
            response = requests.post(api_url, json=payload, headers=headers, timeout=8)
            
            # إذا كان الرد ليس JSON، نعتبره فشلاً ونجرب التالي
            try:
                data = response.json()
            except:
                continue

            # حالة النجاح ✅
            if 'url' in data:
                return jsonify({
                    "title": "تم جلب الفيديو بنجاح 🎥",
                    "thumbnail": "https://i.ytimg.com/vi/mqDf69j586s/maxresdefault.jpg",
                    "video_url": data['url']
                })
            
            # حالات الفشل المعروفة من السيرفر
            if 'text' in data:
                 print(f"Server Error: {data['text']}")
                 continue # جرب السيرفر التالي
            
        except Exception as e:
            print(f"Connection Failed to {api_url}: {str(e)}")
            continue # السيرفر طافي، اللي بعده!

    # إذا وصلنا هنا، يعني كل السيرفرات الـ 6 فشلت (نادر جداً)
    return jsonify({"error": "جميع السيرفرات مشغولة، حاول بعد دقيقة! 😔"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

