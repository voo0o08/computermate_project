from flask import Blueprint, render_template
from ..models import Raw10

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    # raw10 테이블의 모든 데이터 조회
    # data = Raw10.query.all()
    data = Raw10.query.limit(10).all()
    return render_template('index.html', data=data)
