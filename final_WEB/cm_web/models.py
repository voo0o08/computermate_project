# ## 모듈 로딩 --------------------------------------------------
from cm_web import db
from datetime import datetime


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
    