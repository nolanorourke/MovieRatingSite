# Name: Nolan O'Rourke no21b 
# The program in this file is the individual work of Nolan O'Rourke
# File: app.py
# Homework: 2
# February 14, 2024
#THIS IS NOT ANY PROGRESS, JUST EXAMPLE FROM CLASS
from flask import Flask, render_template, request
import sqlite3 as sql
import datetime
app = Flask(__name__)

#attachment for home
@app.route('/')
def home():
    return render_template('index.html')

#inserting review
@app.route('/addReview')
def insertR():
    return render_template('addReview.html')

#show the genres
@app.route('/showGenres')
def showG():
    return render_template('getReviews.html')

#Show top 5 table
@app.route('/TopFive')
def retrieve_BIY():#best in year
    return render_template('getYear.html')

@app.route('/insertReview',  methods = ['POST', 'GET'])
def add_review():#add review
    print("made it here 0")
    if request.method == 'POST':
        try:
            msg = ""
            print("Made it here1")
            un = request.form['Username']
            ttl = request.form['Title']

            mvid = str(ttl)
            mvid = ttl[:5]
            yr = request.form['Year']
            mvid += str(yr)

            rvtm = str(datetime.datetime.now())
            rtng = request.form['Rating']
            rv = request.form['Review']
            dir = request.form['Director']
            gen = request.form['Genre']

            print("made it here2")
            with sql.connect("movieData.db") as con:
                cur = con.cursor()
                print("made it here 3")
                cur.execute("INSERT INTO Reviews (Username, MovieID, ReviewTime, Rating, Review) VALUES (?,?,?,?,?)", (un, mvid, rvtm, rtng, rv))
                #con.commit()
                print("made it here 4")

                cur.execute("INSERT OR IGNORE INTO Movies (MovieID, Title, Director, Genre, Year) VALUES (?,?,?,?,?)", (mvid, ttl, dir, gen, yr))
                con.commit()
                print("made it here 5")

                msg = "Review successfully added"

        except:
            con.rollback()
            msg = "Error adding review"
        finally:
            return render_template('index.html', msg = msg)
            con.close()
    

@app.route('/listTopFive', methods = ['POST', 'GET'])
def list_Top_Five():#list by genre
    year = str(request.form['Year'])
    con = sql.connect("movieData.db")
    con.row_factory = sql.Row

    cur = con.cursor()
    cur.execute("SELECT Movies.Title, Movies.Genre, AVG(Reviews.Rating) AS AvgRating FROM Movies INNER JOIN Reviews ON Movies.MovieID = Reviews.MovieID WHERE Movies.Year = '"+year+"' GROUP BY Movies.MovieID ORDER BY AvgRating DESC, Movies.Title ASC LIMIT 5")

    rows = cur.fetchall();
    return render_template('bestInYear.html', rows = rows)
    con.close()

@app.route('/listInGenre', methods = ['POST', 'GET'])
def list_by_genre():#list by genre
    gen = str(request.form['Genre'])
    con = sql.connect("movieData.db")
    con.row_factory = sql.Row

    cur = con.cursor()
    cur.execute("SELECT Movies.Title, Movies.Director, Reviews.Review, Reviews.Rating FROM Movies INNER JOIN Reviews ON Movies.MovieID = Reviews.MovieID WHERE Movies.Genre = '"+gen+"'")
    
    rows = cur.fetchall();
    return render_template('listByGenre.html', rows = rows)

#this can stay
if __name__ == '__main__':
    app.run(debug = True)