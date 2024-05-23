from flask import Blueprint, redirect, jsonify

# Response, request => HTML 응답 요청을 처리하기 위함 
# render_template => HTML 파일을 렌더링
from flask import Flask, render_template, Response, request
import pandas as pd 
import json
import plotly
import plotly.express as px
import numpy as np

bp = Blueprint("main", __name__, url_prefix="/")

CM_DF = pd.read_csv("./cm_web/static/data/for_web.csv")
WINDOW_SIZE = 30
cnt = 0

# @=>데코레이터 
@bp.route("/")
def index():
    return render_template("index.html")


# dashboard =========================================================================
@bp.route("/dash")
def dash():
    # graph one
    df = px.data.medals_wide()
    fig1 = px.bar(df, x="nation", y=["gold", "silver", "bronze"], title="WideForm Input")
    
    graph1JSON = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)
    
    # Graph Two
    df = px.data.iris()
    fig2 = px.scatter_3d(df, x="sepal_length", y="sepal_width", z="petal_width",
                         color="species", title="Iris")
    graph2JSON = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)
    
    return render_template("dash.html", title="Home", graph1JSON=graph1JSON, graph2JSON=graph2JSON)


# 차트는 여기서 업데이트됨
@bp.route('/update_chart')
def update_chart():
    global WINDOW_SIZE
    global CM_DF
    global cnt
    print("Updating chart...")  # 로그 추가 -> python terminal에서 확인
    # 데이터 업데이트 로직 (예시)
    
    col_data = CM_DF["n_temp_pv"]
    new_fig = px.line(x=range(WINDOW_SIZE), y=col_data[cnt:cnt+WINDOW_SIZE],
                      markers=True)
    new_fig.update_layout(yaxis_range=[60, 80])
    
    new_graphJSON = json.dumps(new_fig, cls=plotly.utils.PlotlyJSONEncoder)
    cnt += 1 # WINDOW 이동
    return jsonify({"new_graphJSON": new_graphJSON, "msg" : "화이팅!"})

# 1번 공장 =======================================================================================
@bp.route('/factory1')
def factory1():
    return render_template("factory.html")