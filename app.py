from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reviews.db'
db = SQLAlchemy(app)

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(100), nullable=False)
    reviewer_name = db.Column(db.String(100), nullable=False)
    review_text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    reviews = Review.query.all()
    return render_template('index.html', reviews=reviews)

@app.route('/add', methods=['GET', 'POST'])
def add_review():
    if request.method == 'POST':
        product_name = request.form['product_name']
        reviewer_name = request.form['reviewer_name']
        review_text = request.form['review_text']
        rating = int(request.form['rating'])
        
        new_review = Review(product_name=product_name, reviewer_name=reviewer_name, review_text=review_text, rating=rating)
        db.session.add(new_review)
        db.session.commit()
        
        return redirect(url_for('index'))
    
    return render_template('add_review.html')

if __name__ == '__main__':
    app.run(debug=True)