from flask import Blueprint, jsonify, request, make_response
from community_app.models.categories import Category
from pydantic import ValidationError
from community_app.schemas.categories import CategoryCreate, CategoryResponse
from community_app import db

categories_bp = Blueprint('categories', __name__, url_prefix='/categories')


@categories_bp.route('/', methods=['POST'])
def create_category():
    data = request.get_json()

    try:
        category_data = CategoryCreate(**data)
    except ValidationError as err:
        return make_response(jsonify(err.errors()), 400)

    category = Category(name=category_data.name)

    db.session.add(category)
    db.session.commit()

    return make_response(jsonify(CategoryResponse(id=category.id, name=category.name).dict()), 201)


@categories_bp.route('/', methods=['GET'])
def get_all_categories():
    categories = Category.query.all()
    return jsonify([CategoryResponse(id=c.id, name=c.name).dict() for c in categories])


@categories_bp.route('/<int:id>', methods=['PUT'])
def update_category(id):
    category = Category.query.get_or_404(id)

    data = request.get_json()

    try:
        category_data = CategoryCreate(**data)
    except ValidationError as err:
        return make_response(jsonify(err.errors()), 400)

    category.name = category_data.name
    db.session.commit()

    return jsonify(CategoryResponse(id=category.id, name=category.name).dict())


@categories_bp.route('/<int:id>', methods=['DELETE'])
def delete_category(id):
    category = Category.query.get_or_404(id)
    db.session.delete(category)
    db.session.commit()
    return make_response('', 204)
