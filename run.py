from flask import Flask, request, jsonify, send_from_directory
from flask import render_template, Response, stream_with_context
from werkzeug.utils import secure_filename
import asyncio
import edge_tts
import os
import uuid
import time
CLEANUP_DELAY = 300  # 300秒（5分钟）后清理文件

app = Flask(__name__)
AUDIO_DIR = "static/audio"
os.makedirs(AUDIO_DIR, exist_ok=True)
app.model_folder = 'models' 


@app.route('/')
@app.route('/desktop.html')
def desktop():
    return render_template('desktop.html')


@app.route('/models/<path:filename>')
def model_file(filename):
    """ 提供 models 文件夹中的文件 """
    print( filename)
    return send_from_directory(app.model_folder, filename)


async def text_to_speech_stream(text, speaker="zh-CN-XiaoxiaoNeural"):
    """使用 edge_tts 生成 TTS 音频，并实时返回 URL"""
    filename = f"{uuid.uuid4()}.mp3"
    filepath = os.path.join(AUDIO_DIR, filename)
    tts = edge_tts.Communicate(text, speaker)
    await tts.save(filepath)
    return f"/{AUDIO_DIR}/{filename}"


async def delete_file_later(filepath):
    """延迟删除文件"""
    await asyncio.sleep(CLEANUP_DELAY)
    if os.path.exists(filepath):
        os.remove(filepath)
        print(f"Deleted: {filepath}")


@app.route("/generate_audio_backend", methods=["POST"])
def generate_audio_backend():
    """流式返回音频 URL"""
    data = request.json
    texts = data.get("texts", [])  # 预期输入 ['你好', '你好吗?', '我很好']
    speakers = {"speaker1": "zh-CN-YunjianNeural", "speaker2": "zh-CN-XiaoxiaoNeural"}  # 轮流使用不同语音

    def generate():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        role = "speaker1"
        length = 0
        with open("script1.txt", "r", encoding="utf-8") as file:
            lines = file.readlines()

        # 去除每行末尾的换行符，并保存为列表
        texts = [line.strip() for line in lines]
        for i, text in enumerate(texts):
            line = text
            if line.startswith("{speaker"):
                role = line[1:9]
                line = line[11:].strip()
            print(role, 'say', line[:8])
            length += len(line)
            audio_url = loop.run_until_complete(text_to_speech_stream(line, speakers[role]))
            yield f"data: {audio_url}\n\n" 

    return Response(stream_with_context(generate()), content_type="text/event-stream")


@app.route("/generate_audio", methods=["POST"])
def generate_audio():
    """流式返回音频 URL"""
    data = request.json
    texts = data.get("texts", [])  # 预期输入 ['你好', '你好吗?', '我很好']
    speakers = {"speaker1": "zh-CN-YunjianNeural", "speaker2": "zh-CN-XiaoxiaoNeural"}  # 轮流使用不同语音

    def generate():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        role = "speaker1"
        length = 0
        for i, text in enumerate(texts):
            line = text
            if line.startswith("{speaker"):
                role = line[1:9]
                line = line[11:].strip()
            print(role, 'say', line[:8])
            length += len(line)
            audio_url = loop.run_until_complete(text_to_speech_stream(line, speakers[role]))
            yield f"data: {audio_url}\n\n" 
    return Response(stream_with_context(generate()), content_type="text/event-stream")


@app.route("/static/audio/<filename>")
def get_audio(filename):
    return send_from_directory(AUDIO_DIR, filename)


@app.route("/goclick", methods=["POST"])
def go_click():
    from click_screen import click_at
    click_at()
    return '', 204


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=11444)
    # app.run(debug=True, host='0.0.0.0', port=11445)
