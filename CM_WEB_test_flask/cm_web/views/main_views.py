from flask import Blueprint, render_template
from ..models import Raw10
from datetime import datetime

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    # raw10 테이블의 모든 데이터 조회
    # data = Raw10.query.all()
    data = Raw10.query.limit(10).all()
    return render_template('index.html', data=data)

@bp.route('/data')
def get_data():
    # start_date = datetime.fromisoformat('2023-05-18T00:00:00.000000') # ISO 8601
    # end_date = datetime.fromisoformat('2023-05-20T00:00:00.000000') # 19일까지의 데이터를 포함하기 위해 20일을 끝으로 설정
    start_date = datetime(2023, 5, 18)
    end_date = datetime(2023, 5, 20)  # 19일까지의 데이터를 포함하기 위해 20일을 끝으로 설정
    entries = Raw10.query.filter(Raw10.time >= start_date, Raw10.time < end_date).all()
    return render_template('data.html', entries=entries)