from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import urllib.parse 

# Configure Database URI: 
params = urllib.parse.quote_plus("DRIVER=ODBC+Driver+17+for+SQL+Server;SERVER=mybkb.database.windows.net;DATABASE=BKB_CR;UID=bkbadmin;PWD=@Mybkb2024")

# initialization
app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecret'
app.config['SQLALCHEMY_DATABASE_URI'] = "mssql+pyodbc:///?odbc_connect=%s" % params
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

# extensions
db = SQLAlchemy(app)

class Car(db.Model):
    __tablename__ = 'car'
    __table_args__ = {'schema': 'dbo'}
    
    car_id = db.Column(db.String(20), primary_key=True)
    brand = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)

@app.route('/')
def index():
    cars = Car.query.all()
    return render_template('index.html', cars=cars)

@app.route('/add_car', methods=['POST'])
def add_car():
    car_id = request.form['car_id']
    brand = request.form['brand']
    model = request.form['model']
    year = int(request.form['year'])
    price = float(request.form['price'])
    car = Car(car_id=car_id, brand=brand, model=model, year=year, price=price)
    db.session.add(car)
    db.session.commit()
    return redirect(url_for('index'))
    
@app.route('/update_car', methods=['POST'])
def update_car():
    car_id = request.form['car_id']
    car = Car.query.filter_by(car_id=car_id).first()
    if car:
        car.brand = request.form['brand']
        car.model = request.form['model']
        car.year = int(request.form['year'])
        car.price = float(request.form['price'])
        db.session.commit()
        return redirect(url_for('index'))
    return "Car not found."


@app.route('/delete_car', methods=['POST'])
def delete_car():
    car_id = request.form['car_id']
    car = Car.query.get(car_id)
    if car:
        db.session.delete(car)
        db.session.commit()
        return redirect(url_for('index'))
    return "Car not found."

if __name__ == '__main__':
    #db.create_all()
    app.run(debug=True, port=8080)