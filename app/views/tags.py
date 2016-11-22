from . import views
from flask import redirect, request, jsonify
from app.model.post import Tag


@views.route('/tags/input')
def tagsInput():
    """文章编辑页，标签自动完成获取列表。
    Returns:
        TYPE: Description
    """
    all_tags = Tag.query.all();
    return jsonify([tag.name for tag in all_tags])


@views.route('/tags/<string:name>')
def tagsView(name):
    tag=Tag.query.filter_by(name=name).first()
    # tag.pages
    # return tag_name
    pass