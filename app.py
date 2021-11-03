import re
from flask import Flask, render_template, redirect, request
import pickle
from flask.helpers import url_for
import pandas as pd
import numpy as np

#  df = pd.read_csv('pivot_table.csv')
#  movie_feature_df = df.drop('title', axis=1)
#  movie_name = df.title
#  model = pickle.load(open('model.pkl', 'rb'))
#  movie = int(input('Enter movie id: '))

# def recommend(movie):
#     model.kneighbors(movie_feature_df.iloc[movie,:].values.reshape(1, -1), n_neighbors=6)
#     distances, indices = model.kneighbors(movie_feature_df.iloc[movie,:].values.reshape(1, -1), n_neighbors=6)
#     for i in range(0, len(distances.flatten())):
#         if i==0:
#             print(f"Recommendation for {movie_name[movie]} are:\n")
#         else:
#             print(f"{i}. {movie_name[indices.flatten()[i]]}")
# recommend(movie)

def get_suggestions():
    data = pd.read_csv('pivot_table.csv')
    return list(data['title'].str.capitalize())

app=Flask(__name__)

@app.route('/')
def homepage():
    return render_template('index.html')

@app.route('/submit', methods=['POST', 'GET'])
def submit():
    movie=0
    if request.method=='POST':
        movie=request.form['movie']
        #print(movie)
        df = pd.read_csv('pivot_table.csv')
        movie_id = df[df['title']==movie].index[0]
        #print(movie_id)
    return redirect(url_for('recommend', movie=movie_id))

@app.route('/recommmend/<int:movie>')
def recommend(movie):
    df = pd.read_csv('pivot_table.csv')
    movie_feature_df = df.drop('title', axis=1)
    movie_name = df.title
    model = pickle.load(open('model.pkl', 'rb'))
    model.kneighbors(movie_feature_df.iloc[movie,:].values.reshape(1, -1), n_neighbors=6)
    distances, indices = model.kneighbors(movie_feature_df.iloc[movie,:].values.reshape(1, -1), n_neighbors=6)
    list = []
    name = movie_name[movie]
    for i in range(0, len(distances.flatten())):
        if i==0:
            #print(f"Recommendation for {movie_name[movie]} are:\n")
            continue
        else:
            list.append(movie_name[indices.flatten()[i]])
            #print(f"{i}. {movie_name[indices.flatten()[i]]}")
    #print(f"movie id: {movie}")
    #print(list)
    #print(type(list))
    #for i in list:
    #    print(i)

    return render_template('recommend.html', list=list, name=name)

if __name__=='__main__':
    app.run(debug=True)