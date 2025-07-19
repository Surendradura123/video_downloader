from flask import Flask, render_template, request, send_from_directory
import yt_dlp
import os
from uuid import uuid4

app = Flask(__name__)
DOWNLOAD_FOLDER = "downloads"

# Ensure downloads folder exists
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        video_url = request.form['url']
        video_id = str(uuid4())  # unique filename prefix
        try:
            ydl_opts = {
                'outtmpl': f'{DOWNLOAD_FOLDER}/{video_id}-%(title)s.%(ext)s',
                'format': 'bestvideo+bestaudio/best',
                'merge_output_format': 'mp4',
                'quiet': True,
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(video_url)
                filename = ydl.prepare_filename(info)
                if not filename.endswith(".mp4"):
                    filename = filename.rsplit(".", 1)[0] + ".mp4"

            return render_template('index.html', success=True, filename=os.path.basename(filename))

        except Exception as e:
            return render_template('index.html', error=str(e))

    return render_template('index.html')

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(DOWNLOAD_FOLDER, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
