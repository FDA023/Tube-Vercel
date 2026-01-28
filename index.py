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

    # --- الخطة الجديدة: استخدام Cobalt API (محرك خارجي) ---
    # هذا المحرك يتجاوز حظر يوتيوب تلقائياً
    api_url = "https://api.cobalt.tools/api/json"
    
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
        # إرسال الطلب للمحرك الخارجي
        response = requests.post(api_url, json=payload, headers=headers)
        data = response.json()

        # التحقق من نجاح العملية
        if 'url' in data:
            return jsonify({
                "title": "تم جلب الفيديو بنجاح ✅", # المحرك أحياناً لا يعطي العنوان، نضع رسالة نجاح
                "thumbnail": "https://i.ytimg.com/vi/mqDf69j586s/maxresdefault.jpg", # صورة افتراضية أو يمكن جلبها
                "duration": "N/A",
                "video_url": data['url']
            })
        elif 'text' in data: # في حال وجود خطأ من المحرك
             return jsonify({"error": "Cobalt Error: " + data['text']}), 500
        else:
             return jsonify({"error": "فشل جلب الرابط، حاول مرة أخرى."}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

