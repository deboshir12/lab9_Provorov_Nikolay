import flask
import sqlalchemy.sql
from flask_sqlalchemy import SQLAlchemy


app = flask.Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://alexivanov:5432@localhost/test'
db = SQLAlchemy(app)


class Work(db.Model):
    company = db.Column(db.String(128), primary_key=True)
    term = db.Column(db.Integer, nullable=False)


@app.route('/', methods=['GET'])
def hello():
    return flask.render_template('index.html', works=Work.query.all())


@app.route('/add_message', methods=['POST'])
def add_message():
    company = flask.request.form['company']
    term = flask.request.form['term']

    # messages.append(Message(text, tag))
    if company not in Work.query.all():
        db.session.add(Work(company=company, term=term))
        db.session.commit()
    else:
        print("Ты долбоеб")
    return flask.redirect(flask.url_for('hello'))


@app.route('/clear', methods=['POST'])
def clear():
    db.session.execute(sqlalchemy.sql.text("DELETE FROM work"))
    db.session.commit()
    return flask.redirect(flask.url_for('hello'))



with app.app_context():
    db.create_all()
app.run()
