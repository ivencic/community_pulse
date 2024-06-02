from community_app import create_app
from community_app.routers.questions import questions_bp
from community_app.routers.response import response_bp
from community_app.models.questions import Question, Statistic
from community_app.models.response import Response
from community_app.models.cateries import Category

app = create_app()

app.register_blueprint(questions_bp)
app.register_blueprint(response_bp)

if __name__ == '__main__':
    app.run()
