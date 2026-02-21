from flask import Flask
from routes.auth_routes import auth_bp
from routes.editor_routes import editor_bp
from database import init_db

app = Flask(__name__)
app.config.from_object("config.Config")

init_db()

app.register_blueprint(auth_bp)
app.register_blueprint(editor_bp)

if __name__ == "__main__":
    app.run(debug=True)
