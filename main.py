
from flask import Flask, render_template ,session, redirect, url_for
from database import db
from config import Config
import models
from routes import routes

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

app.register_blueprint(routes)

with app.app_context():
    db.create_all()

@app.route("/")
def home():
    if 'user_id' not in session:
        return redirect(url_for('routes.login'))
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
