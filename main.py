from flask import Flask, redirect, request
from flask_sqlalchemy import SQLAlchemy
from configparser import ConfigParser


# form database url connector string
db_url_str = "mysql+pymysql://{}:{}@localhost:3306/gps?charset=utf8"
cp = ConfigParser()
cp.read("gps.ini")
user = cp.get("database", "user")
pw = cp.get("database", "password")
db_url_str = db_url_str.format(user, pw)


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = db_url_str
db = SQLAlchemy(app)


class Coordinates(db.Model):
    __tablename__ = "gps_coords"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    latitude = db.Column(db.Integer, nullable=False)
    longitude = db.Column(db.Integer, nullable=False)


db.create_all()


@app.route("/")
def index():
    return redirect("/static/index.html")


@app.route("/addlocation", methods=["POST"])
def add_location():
    json_ob = request.get_json()
    lat = json_ob.get("latitude")
    lng = json_ob.get("longitude")
    coord = Coordinates(latitude=lat, longitude=lng)
    db.session.add(coord)
    db.session.commit()

    return "location_added"


if __name__ == '__main__':
    run_config = dict(debug=True, port=8080)
    app.run(**run_config)