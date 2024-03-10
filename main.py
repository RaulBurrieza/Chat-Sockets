from random import randint
from datetime import datetime
from flask import Flask, request, jsonify,render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres.ocgkkizcykkwsdzxjrzc:basededatosflask@aws-0-eu-central-1.pooler.supabase.com:5432/postgres'
db = SQLAlchemy(app)
datetime = datetime.now()
class mensajes(db.Model):
    __tablename__ = 'mensajes'
    id = db.Column(db.Integer, primary_key=True,name='id')
    sender = db.Column(db.String(50), nullable=False,name='from')
    receiver = db.Column(db.String(50), nullable=False,name='to')
    content = db.Column(db.String(50), nullable=False,name='message')

@app.route('/')
def indexPage():
    return render_template('index.html')


@app.route('/enviar_mensaje', methods=['POST'])
def enviar_mensaje():
    data = request.get_json()
    random_id = int(datetime.timestamp())
    nuevo_mensaje = mensajes(
        id = random_id,
        sender=data['sender'],
        receiver=data['receiver'],
        content=data['message']
    )

    db.session.add(nuevo_mensaje)
    db.session.commit()

    return jsonify({"mensaje": "Mensaje enviado correctamente"})

@app.route('/descargar_mensajes/<usuario>', methods=['GET'])
def descargar_mensajes(usuario):
    mensajes_nuevos = mensajes.query.filter_by(receiver=usuario).all()
    db.session.commit()

    if mensajes_nuevos:
        mensajes_descargados = [
            {"from": mensaje.sender, "message": mensaje.content}
            for mensaje in mensajes_nuevos
        ]
        return jsonify({"mensajes": mensajes_descargados})
    else:
        return jsonify({"mensajes": []})

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
