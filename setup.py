# Name: Nolan O'Rourke no21b 
# The program in this file is the individual work of Nolan O'Rourke
# File: setup.py
# Homework: 2
# February 14, 2024
import sqlite3

conn = sqlite3.connect('movieData.db')
print('Opened database successfully')

conn.execute('CREATE TABLE Reviews (Username TEXT, MovieID TEXT, ReviewTime DATETIME, Rating FLOAT, Review TEXT)')
print('Created Reviews table')

conn.execute('CREATE TABLE Movies (MovieID TEXT PRIMARY KEY, Title TEXT, Director TEXT, Genre TEXT, Year INTEGER)')
print('Created Movies table')

conn.close()