from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask.views import MethodView
from dotenv import load_dotenv

load_dotenv()

# Inicializar Flask y configuraciones
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar SQLAlchemy y Marshmallow
db = SQLAlchemy(app)
ma = Marshmallow(app)

# Definir el modelo User
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

# Definir el esquema para User
class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User


@app.route('/')
def index():
    return "¡Bienvenido a mi aplicación Flask! VAMO RIVER CARAJO MIERDA"


# Definir una clase MethodView para User
class UserView(MethodView):

    user_schema = UserSchema()

    def get(self, user_id):
        user = User.query.get_or_404(user_id)
        return self.user_schema.jsonify(user)

    def post(self):
        data = request.get_json()
        new_user = User(username=data['username'], email=data['email'])
        db.session.add(new_user)
        db.session.commit()
        return self.user_schema.jsonify(new_user), 201

# Agregar la ruta para UserView
app.add_url_rule('/users/<int:user_id>/', view_func=UserView.as_view('user'))


# Inicializar la base de datos y ejecutar la aplicación
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
