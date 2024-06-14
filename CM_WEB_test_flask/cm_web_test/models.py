# ## 모듈 로딩 --------------------------------------------------
from cm_web_test import db
from datetime import datetime


# ## Translation 테이블 클래스 ---------------------------------------
# ## 컬럼 : id, original_text, translation_text, create_date
# class Translation(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     original_text = db.Column(db.Text(), nullable=False)
#     translation_text = db.Column(db.Text(), nullable=False)
#     create_date = db.Column(db.DateTime(), nullable=False, default=datetime.now())

class Raw10(db.Model):
    __tablename__ = 'raw10'
    time = db.Column(db.DateTime(), primary_key=True)
    # 다른 컬럼들도 정의하세요. 예:
    E_scr_pv = db.Column(db.Integer)
    E_scr_sv = db.Column(db.Integer)
    c_temp_pv = db.Column(db.Double)
    c_temp_sv = db.Column(db.Integer)
    k_rpm_pv = db.Column(db.Integer)
    k_rpm_sv = db.Column(db.Integer)
    n_temp_pv = db.Column(db.Double)
    n_temp_sv = db.Column(db.Integer)
    scale_pv = db.Column(db.Double)
    s_temp_pv = db.Column(db.Double)
    s_temp_sv = db.Column(db.Integer)
    
class Test(db.Model):
    __tablename__ = 'test_table'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    c_time = db.Column(db.DateTime, nullable=False)
    my_num = db.Column(db.Integer, nullable=False)
    