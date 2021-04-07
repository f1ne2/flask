from app import app, db
from app.models import Categories, Questions, Answers


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Categories': Categories, 'Questions': Questions,
            'Answers': Answers}


if __name__ == "__main__":
    app.run(host="127.0.0.1", port="5000")