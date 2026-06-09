from flask import Flask, request, send_file
import subprocess
import os
import uuid

app = Flask(__name__)

@app.route('/generate', methods=['POST'])
def generate():
    image = request.files['image']
    audio = request.files['audio']
    
    job_id = str(uuid.uuid4())
    image_path = f'/tmp/{job_id}_img.jpg'
    audio_path = f'/tmp/{job_id}_audio.wav'
    output_path = f'/tmp/{job_id}_output.mp4'
    
    image.save(image_path)
    audio.save(audio_path)
    
    subprocess.run([
        'python', 'inference.py',
        '--checkpoint_path', 'checkpoints/wav2lip_gan.pth',
        '--face', image_path,
        '--audio', audio_path,
        '--outfile', output_path
    ])
    
    return send_file(output_path, mimetype='video/mp4')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
