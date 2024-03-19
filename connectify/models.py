from datetime import datetime
from connectify import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    priority = db.Column(db.Integer, nullable=False, default=0)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self) -> str:
        return f"User('{self.first_name}', '{self.last_name}', '{self.image_file}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    introduction = db.Column(db.String, nullable=False)
    problem_statement = db.Column(db.String, nullable=False)
    solution = db.Column(db.String, nullable=False)
    unique_selling_proposition = db.Column(db.String, nullable=False)
    market_analysis = db.Column(db.String, nullable=False)
    target_audience = db.Column(db.String, nullable=False)
    competitive_analysis = db.Column(db.String, nullable=False)
    financial_projection = db.Column(db.String, nullable=False)
    risk_assessment = db.Column(db.String, nullable=False)
    team = db.Column(db.String, nullable=False)
    conclusion = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


    def __repr__(self) -> str:
        return f"Post('{self.title}', '{self.problem_statement}', '{self.financial_projection}')"
    
posts = [
    {
        'author': 'Abdulrasheed Muhammed',
        'title': 'First Pitch',
        'content': 'First Pitch Content',
        'date_posted': 'April 20, 2021'
    }, 
    {
        'author': 'Abdulsabur Muhammed',
        'title': 'Second Pitch',
        'content': 'Second Pitch Content',
        'date_posted': 'April 20, 2022'
    }
]