from flask import Flask
from scraper import getResult, cgpaCal
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"*": {"origins": "*"}})

@app.route("/<ag>", )
def respondResult(ag):
    return cgpaCal(getResult(ag))



if __name__ == "__main__":
    app.run(debug=True)