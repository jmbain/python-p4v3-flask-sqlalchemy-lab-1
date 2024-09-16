# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

# Add views here
@app.route('/earthquakes/<int:id>')
def eq_by_id(id):
    eq = Earthquake.query.filter(Earthquake.id == id).first()
    if not eq:
        return {"message": f"Earthquake {id} not found."}, 404
    return eq.to_dict(), 200

@app.route('/earthquakes/magnitude/<float:magnitude>')
def eqs_by_mag(magnitude):
    eqs = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()
    # result = []
    # for eq in eqs:
    #     result.append(eq.to_dict())

    return {
        'count': len(eqs),
        'quakes': [eq.to_dict() for eq in eqs]
    }

if __name__ == '__main__':
    app.run(port=5555, debug=True)
