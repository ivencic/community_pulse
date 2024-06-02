from flask import Blueprint, jsonify, request, make_response

from pydantic import ValidationError

from community_app.models.questions import Question
from community_app.schemas.questions import QuestionCreate, QuestionResponse
from community_app import db


questions_bp = Blueprint('questions', __name__, url_prefix='/questions')


@questions_bp.route('/', methods=['GET'])
def get_all_questions():
    questions: list[Question, ...] = Question.query.all()

    # questions_data: list[dict] = [
    #     {
    #         "id": question.id,
    #         "text": question.text,
    #         "created_at": question.created_at
    #     }
    #     for question in questions
    # ]

    results = [
        QuestionResponse.from_orm(question).dict() for question in questions
    ]

    response = make_response(jsonify(results), 200)

    response.headers["Custom-Header"] = 'OUR CUSTOM HEADER'

    return response


@questions_bp.route('/add', methods=['POST'])
def add_new_question():
    data = request.get_json()

    # if not data or 'text' not in data:
    #     return jsonify(
    #         {
    #             "message": "NO DATA PROVIDED"
    #         }
    #     ), 400

    try:
        question_data = QuestionCreate(**data)
    except ValidationError as err:
        return make_response(jsonify(err.errors()), 400)

    question: Question = Question(text=question_data.text)

    db.session.add(question)
    db.session.commit()

    # return make_response(
    #     jsonify(
    #         {
    #             "message": "NEW QUESTION ADDED",
    #             "question_id": question.id
    #         }
    #     ), 201
    # )
    return make_response(
        jsonify(QuestionResponse(
            id=question.id,
            text=question.text
        ).dict()), 201
    )


@questions_bp.route('/<int:question_id>')
def get_question_by_id(question_id):
    question: Question = Question.query.get(question_id)

    # if not question:
    #     abort(404)

    if not question:
        return make_response(jsonify(
            {
                "message": "NOT FOUND",
            }
        ), 404)

    question_data = {
        "id": question.id,
        "text": question.text,
        "created_at": question.created_at
    }

    return make_response(jsonify(question_data), 200)


@questions_bp.route('/update/<int:question_id>', methods=['PUT'])  # 127.0.0.1:5000/questions/update/5
def update_question_by_pk(question_id):
    question: Question = Question.query.get(question_id)

    if not question:
        return make_response(jsonify(
            {
                "message": "NOT FOUND"
            }
        ), 404)

    request_data = request.get_json()

    if 'text' in request_data:
        question.text = request_data["text"]

        db.session.commit()

        return make_response(jsonify(
            {
                "message": "QUESTION UPDATED SUCCESSFULLY",
                "new_text": question.text
            }
        ), 200)

    else:
        return make_response(jsonify(
            {
                "message": "NO DATA PROVIDED"
            }
        ), 400)


@questions_bp.route('/delete/<int:question_id>', methods=['DELETE'])
def delete_question_by_pk(question_id):
    question: Question = Question.query.get(question_id)

    if not question:
        return make_response(jsonify(
            {
                "message": "NOT FOUND"
            }
        ), 404)

    db.session.delete(question)
    db.session.commit()

    return make_response(jsonify(
        {
            "message": "QUESTION DELETED SUCCESSFULLY"
        }
    ), 200)
