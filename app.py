from flask import Flask, render_template, request
import pickle
import numpy as np

# Load pickles
popular_df = pickle.load(open('popular.pkl', 'rb'))
pt = pickle.load(open('pt.pkl', 'rb'))
books = pickle.load(open('books.pkl', 'rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl', 'rb'))

app = Flask(__name__)


# --- Recommend function ---
def recommend(book_name):
    if book_name not in pt.index:
        return []

    index = np.where(pt.index == book_name)[0][0]
    similar_items = sorted(
        list(enumerate(similarity_scores[index])),
        key=lambda x: x[1],
        reverse=True
    )[1:6]

    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
        data.append(item)

    return data


# --- Routes ---
@app.route('/')
def index():
    books_list = list(
        zip(
            popular_df['Book-Title'].values,
            popular_df['Book-Author'].values,
            popular_df['Image-URL-M'].values,
            popular_df['num_ratings'].values,
            popular_df['avg_ratings'].round(1).values,
        )
    )
    return render_template('index.html', books=books_list, active_page="home")


@app.route('/recommend', methods=['GET', 'POST'])
def recommend_page():
    recommendations = []
    if request.method == 'POST':
        user_input = request.form.get('book_name')
        recommendations = recommend(user_input)
    return render_template('recommend.html', books=recommendations, active_page="recommend")


if __name__ == '__main__':
    app.run(debug=True)
