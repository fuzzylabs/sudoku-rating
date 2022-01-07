import streamlit as st
from requests import post
from json import dumps

model_url = "http://localhost:5000/predict"

st.title("Sudoku Difficulty Evaluator")
user_input = st.text_input("Sudoku string")

for row in range(9):
    columns = st.columns(9)
    for i, column in enumerate(columns):
        column.selectbox("", (".", 1, 2, 3, 4, 5, 6, 7, 8, 9), key=row*9 + i)

if st.button("Evaluate"):
    request_data = [
        user_input
    ]

    response = post(model_url, data=dumps(request_data))
    st.write(f'Difficulty: {round(response.json()[0], 2)}')
