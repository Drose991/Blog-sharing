from flask import Flask, Response

app = Flask(__name__)

@app.route("/")
def home():
    return Response("Merhaba Dünya", mimetype="text/plain")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
