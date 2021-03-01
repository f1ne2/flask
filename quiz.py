from app import app, db
from app.models import Categories, Questions, Answers


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Categories': Categories, 'Questions': Questions,
            'Answers': Answers}