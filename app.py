from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp

app = Flask(__name__)
# CORS zaroori hai taaki aapki Netlify website is API se baat kar sake
CORS(app)

@app.route('/api/info', methods=['GET'])
def get_video_info():
    video_url = request.args.get('url')
    if not video_url:
        return jsonify({"error": "URL parameter is missing"}), 400

    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=False)

            # Zaroori details nikal lo
            video_details = {
                "title": info_dict.get('title'),
                "thumbnails": info_dict.get('thumbnails'),
            }

            # Sirf zaroori formats bhejo
            formats = []
            for f in info_dict.get('formats', []):
                # Humein woh format chahiye jisme video aur audio dono ho
                if f.get('vcodec') != 'none' and f.get('acodec') != 'none':
                    formats.append({
                        'format_id': f.get('format_id'),
                        'ext': f.get('ext'),
                        'resolution': f.get('resolution'),
                        'url': f.get('url'),
                        'qualityLabel': f.get('format_note') or f.get('resolution'),
                        'hasVideo': True,
                        'hasAudio': True
                    })
            
            # Final response
            response_data = {
                "videoDetails": video_details,
                "formats": formats
            }
            
            return jsonify(response_data)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)