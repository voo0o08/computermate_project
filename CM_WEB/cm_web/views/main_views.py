from flask import Blueprint, redirect, jsonify

# Response, request => HTML 응답 요청을 처리하기 위함 
# render_template => HTML 파일을 렌더링
from flask import Flask, render_template, Response, request
import pandas as pd 
import json
import plotly
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

bp = Blueprint("main", __name__, url_prefix="/")

CM_DF = pd.read_csv("./cm_web/static/data/for_web.csv")

E_scr_pv = CM_DF["E_scr_pv"]
E_scr_sv = CM_DF["E_scr_sv"]

c_temp_pv = CM_DF["c_temp_pv"]
c_temp_sv = CM_DF["c_temp_sv"]

k_rpm_pv = CM_DF["k_rpm_pv"]
k_rpm_sv = CM_DF["k_rpm_sv"]

n_temp_pv = CM_DF["n_temp_pv"]
n_temp_sv = CM_DF["n_temp_sv"]

s_temp_pv = CM_DF["s_temp_pv"]
s_temp_sv = CM_DF["s_temp_sv"]

WINDOW_SIZE = 30
cnt = 0

# @=>데코레이터 
@bp.route("/")
def index():
    return render_template("index.html")


# dashboard =========================================================================
@bp.route("/dash", methods=['POST'])
def dash():
    
    # # graph one
    # df = px.data.medals_wide()
    # fig1 = px.bar(df, x="nation", y=["gold", "silver", "bronze"], title="WideForm Input")
    
    # graph1JSON = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)
    
    # # Graph Two
    # df = px.data.iris()
    # fig2 = px.scatter_3d(df, x="sepal_length", y="sepal_width", z="petal_width",
    #                      color="species", title="Iris")
    # graph2JSON = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)
    
    ###########################################################################################
    global WINDOW_SIZE
    global CM_DF
    global cnt
    print("그래프 초기화")  # 로그 추가 -> python terminal에서 확인
    
    #Figure 생성
    new_fig = go.Figure()

    #그래프 생성
    x = ['A', 'B', 'C', 'D']

    # 1번 그래프
    new_fig.add_trace(go.Bar(name='Data 1',x=x, y=[100, 200, 500, 673]))

    # 2번 그래프
    new_fig.add_trace(go.Bar(name='Data 2',x=x, y=[56, 123, 982, 213]))

    # 버튼 3개 생성
    new_fig.update_layout(
        updatemenus=[
            dict(
                type="buttons",
                buttons=list([
                    dict(label="Both",
                        method="update",
                        args=[{"visible": [True, True]},
                            {"title": "Both"}]),
                    dict(label="Data 1",
                        method="update",
                        args=[{"visible": [True, False]},
                            {"title": "Data 1",}]),
                    dict(label="Data 2",
                        method="update",
                        args=[{"visible": [False, True]},
                            {"title": "Data 2",}]),
                ]),
            ),
        ]
    )
    
    new_graphJSON = json.dumps(new_fig, cls=plotly.utils.PlotlyJSONEncoder)
    cnt += 1 # WINDOW 이동
    
    return render_template("dash.html", title="Home", graph1JSON=new_graphJSON)


# 차트는 여기서 업데이트됨
@bp.route('/update_chart')
def update_chart():
    global WINDOW_SIZE
    global CM_DF
    global cnt
    print("Updating chart1...")  # 로그 추가 -> python terminal에서 확인
    # 데이터 업데이트 로직 (예시)
    
    col_data = CM_DF["n_temp_pv"]
    new_fig = px.line(x=range(WINDOW_SIZE), y=col_data[cnt:cnt+WINDOW_SIZE],
                      markers=True)
    new_fig.update_layout(yaxis_range=[60, 80])
    
    new_graphJSON = json.dumps(new_fig, cls=plotly.utils.PlotlyJSONEncoder)
    cnt += 1 # WINDOW 이동
    return jsonify({"new_graphJSON": new_graphJSON, "msg" : "화이팅!"})


# 차트는 여기서 업데이트됨
@bp.route('/update_chart2')
def update_chart2():
    global WINDOW_SIZE
    global CM_DF
    global cnt
    print("Updating chart2...")  # 로그 추가 -> python terminal에서 확인
    # 데이터 업데이트 로직 (예시)
    
    # col_data = CM_DF["n_temp_pv"]
    # new_fig = px.line(x=range(WINDOW_SIZE), y=col_data[cnt:cnt+WINDOW_SIZE],
    #                   markers=True)
    # new_fig.update_layout(yaxis_range=[60, 80])
    #################################### button test code 
    
    #Figure 생성
    new_fig = go.Figure()

    #그래프 생성
    x = ['A', 'B', 'C', 'D']

    # 1번 그래프
    new_fig.add_trace(go.Bar(name='Data 1',x=x, y=[100, 200, 500, 673]))

    # 2번 그래프
    new_fig.add_trace(go.Bar(name='Data 2',x=x, y=[56, 123, 982, 213]))


    # 버튼 3개 생성
    new_fig.update_layout(
        updatemenus=[
            dict(
                type="buttons",
                buttons=list([
                    dict(label="Both",
                        method="update",
                        args=[{"visible": [True, True]},
                            {"title": "Both"}]),
                    dict(label="Data 1",
                        method="update",
                        args=[{"visible": [True, False]},
                            {"title": "Data 1",}]),
                    dict(label="Data 2",
                        method="update",
                        args=[{"visible": [False, True]},
                            {"title": "Data 2",}]),
                ]),
            ),
        ]
    )
    
    new_graphJSON = json.dumps(new_fig, cls=plotly.utils.PlotlyJSONEncoder)
    cnt += 1 # WINDOW 이동
    return jsonify({"new_graphJSON": new_graphJSON, "msg" : "이것은 update2!"})



# 1번 공장 =======================================================================================
@bp.route('/factory1')
def factory1():
    return render_template("factory.html")

# button 값 확인 
@bp.route('/click_button', methods=['POST'])
def click_button():
    data = request.get_json()
    print(data)
    # now_button = data.get('button')
    # print(f"now_button: {now_button}")  # 터미널에 출력
    
    print("버튼이 클릭되었습니다!")
    return jsonify({"message": "버튼이 클릭되었습니다!"})

    # return jsonify(success=True)