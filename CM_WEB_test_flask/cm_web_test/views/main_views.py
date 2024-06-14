from flask import Blueprint, render_template
from ..models import Raw10
from ..models import Test
from .. import db
from datetime import datetime


bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    # raw10 테이블의 모든 데이터 조회
    # data = Raw10.query.all()
    data = Raw10.query.limit(10).all()
    
    print("test query => ", Test.query.all())
    for i in range(1, 11):
        new_entry = Test(c_time=datetime.now(), my_num=i)
        db.session.add(new_entry)
    db.session.commit()
    return render_template('index.html', data=data)

