from flask import Flask


app = Flask(__name__)
app.secret_key = "ABC"

@app.route('/')
def index():
    return "<html><body> Placeholder for homepage. </body></html>"

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5000)
