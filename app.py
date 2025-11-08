
from flask import Flask, request
from sqlalchemy import create_engine
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from flask import render_template
from sqlalchemy.sql import column
import sqlite3

con = sqlite3.connect("/content/flask_proj/db/tutorial.db")
cur = con.cursor()
try:
  cur.execute("CREATE TABLE movie(title, year, score)")
except:
  pass

con.close()

# declarative base class
class Base(DeclarativeBase):
    pass


# an example mapping using the base
class Movie(Base):
    __tablename__ = "movie"

    rowid: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    year: Mapped[int]
    score: Mapped[float]

    def __str__(self):
      return f"{self.title}, {self.year}: score {self.score}"

engine = create_engine("sqlite:////content/flask_proj/db/tutorial.db") 

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def lista_itens():

  if request.method == 'POST':

    dict_request = dict(request.form)

    dict_item = {
      'title': dict_request['title'],
      'year': int(dict_request['year']),
      'score': float(dict_request['score'])
    }

    with Session(engine) as session:

      item = Movie(**dict_item)
      session.add(item)
      session.commit()
      
  with Session(engine) as session:
    result = session.execute(select(Movie).order_by(Movie.rowid))

    return render_template('index.html', result=result)

@app.route("/ordenar", methods=['GET', 'POST'])
def ordenar():

  if request.method == 'POST':

    dict_item = dict(request.form)

    with Session(engine) as session:
      result = session.execute(select(Movie).order_by(column(dict_item['item'])))

      return render_template('index.html', result=result)


if __name__ == '__main__':
    app.run()
