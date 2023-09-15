import os
import base64
from pytube import YouTube
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/download', methods=['POST'])
def download_music():
    try:
        data = request.get_json()
        video_url = data.get('video_url')
        output_format = data.get('output_format')
        
        if not video_url or not output_format:
            return jsonify({'error': 'Missing video_url or output_format'}), 400

        yt = YouTube(video_url)

        if output_format == "mp4":
            video_stream = yt.streams.get_highest_resolution()
            downloaded_file_path = video_stream.download(output_path="./downloads")
        elif output_format == "mp3":
            audio_stream = yt.streams.filter(only_audio=True).first()
            downloaded_file_path = audio_stream.download(output_path="./downloads")
        else:
            return jsonify({'error': 'Invalid output_format'}), 400

        if downloaded_file_path:
            with open(downloaded_file_path, 'rb') as file:
                contentBytes = file.read()
            os.remove(downloaded_file_path)
            title = yt.title
            # Encode the bytes as Base64
            contentBytesBase64 = base64.b64encode(contentBytes).decode('utf-8')
            return jsonify({'musicName': title, 'musicBytes': contentBytesBase64})
        else:
            return jsonify({'error': 'Download failed'}), 500

    except Exception as e:
        print("Exception:", str(e))  # Print the exception for debugging
        return jsonify({'error': 'Internal server error'}), 500

if __name__ == "__main__":
    app.run(debug=True)
