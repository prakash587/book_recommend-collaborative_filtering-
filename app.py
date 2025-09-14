from flask import Flask, render_template
import pickle

popular_df = pickle.load(open('popular.pkl', 'rb'))
app = Flask(__name__)

@app.route('/')
def index():
    books = list(
        zip(
            popular_df['Book-Title'].values,
            popular_df['Book-Author'].values,
            popular_df['Image-URL-M'].values,
            popular_df['num_ratings'].values,
            popular_df['avg_ratings'].values,
        )
    )
    return render_template('index.html', books=books)

if __name__ == '__main__':
    app.run(debug=True)
