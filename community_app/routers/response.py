from flask import Blueprint, jsonify, request, make_response
from community_app.models.response import Response
from community_app.models.questions import Question, Statistic

from community_app import db


response_bp = Blueprint('response', __name__, url_prefix='/response')


@response_bp.route('/')
def get_all_response():
    statistic: list[Statistic, ...] = Statistic.query.all()

    result: list[dict] = [
        {
            "question_id": stat.question_id,
            "agree_count": stat.agree_count,
            "disagree_count": stat.disagree_count
        }
        for stat in statistic
    ]

    return make_response(jsonify(result), 200)


@response_bp.route('/add', methods=['POST'])
def add_new_response():
    data = request.get_json()

    if not data or 'question_id' not in data or 'is_agree' not in data:
        return make_response(jsonify(
            {
                "message": "INVALID DATA"
            }
        ), 400)

    question: Question = Question.query.get(data['question_id'])

    if not question:
        return make_response(jsonify(
            {
                "message": "QUESTION NOT FOUND"
            }
        ), 404)

    response: Response = Response(
        question_id=question.id,
        is_agree=data['is_agree']
    )

    db.session.add(response)

    statistic: Statistic = Statistic.query.filter_by(question_id=question.id).first()

    if not statistic:
        statistic: Statistic = Statistic(
            question_id=question.id,
            agree_count=0,
            disagree_count=0
        )

        db.session.add(statistic)

    if data['is_agree']:
        statistic.agree_count += 1
    else:
        statistic.disagree_count += 1

    db.session.commit()

    return make_response(jsonify(
        {
            "message": "NEW RESPONSE WAS ADDED"
        }
    ), 201)
