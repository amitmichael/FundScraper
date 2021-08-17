from flask import Flask, render_template
from flask_pymongo import PyMongo


app = Flask(__name__)
title = "Funds Updated Info"
heading = "Funds Updated Info"
app.config["MONGO_URI"] = "mongodb+srv://dbUser:12345@cluster0.5iar3.mongodb.net/db"
mongodb_client = PyMongo(app)
db = mongodb_client.db.Funds


@app.route('/')
def get_funds():
    funds = db.find()
    a1 = "active"
    return render_template('index.html', a1=a1, funds=funds, t=title, h=heading)


if __name__ == '__main__':
    app.run()
