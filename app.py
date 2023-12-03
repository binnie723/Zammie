from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/instructions')
def instructions():
    return render_template('instructions.html')

@app.route('/find-the-difference')
def find_the_difference():
    return render_template('find-the-difference.html')

@app.route('/webcam')
def webcam():
    return render_template('webcam.html')
    
@app.route('/manual')
def manual():
    return render_template('manual.html')
    
@app.route('/thankyou')
def thankyou():
    return render_template('thankyou.html')

@app.route('/get-image')
def get_image():
    # 이미지 가져오기 함수
    pass

if __name__ == '__main__':
    app.run(debug=True)

