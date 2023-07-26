from flask import Flask, render_template, request
from PIL import Image
import io

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


def image_conversion(img):
    img = img.convert('L')  # グレースケール変換
    img = img.rotate(45)    # 画像を45度回転
    return img

@app.route('/upload', methods=['POST'])
def upload():
    if 'image' not in request.files:
        return 'No image selected.'

    image = request.files['image']

    # 画像の加工処理
    img = Image.open(image)
    img = image_conversion(img)

    # 加工した画像を表示するためにバイナリデータに変換
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)

    return send_image(img_bytes)

def send_image(img_bytes):
    # バイナリデータをブラウザに送信
    return app.response_class(
        response=img_bytes.read(),
        content_type='image/png'
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
