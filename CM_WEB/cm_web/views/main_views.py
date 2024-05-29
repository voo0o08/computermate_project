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

WINDOW_SIZE = 50
cnt = 0

bp = Blueprint("main", __name__, url_prefix="/")

CM_DF = pd.read_csv("./cm_web/static/data/for_web.csv")

graph_idx = 2 # 기본값 => rpm
name_list = ("E_scr", "c_temp", "k_rpm", "n_temp", "s_temp")

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

sr_list = ((E_scr_pv, E_scr_sv),
           (c_temp_pv, c_temp_sv),
           (k_rpm_pv, k_rpm_sv),
           (n_temp_pv, n_temp_sv),
           (s_temp_pv, s_temp_sv))
yaxis_list = ((0, 10),
              (55, 75),
              (100, 200),
              (55, 75),
              (55, 75))
x_values = np.linspace(-WINDOW_SIZE, 0, WINDOW_SIZE, endpoint=False)
x_labels = [f"{int(x)}초" if x != 0 else "현재" for x in x_values]

# 5초 단위로 x축 레이블 설정
tickvals = list(range(0, WINDOW_SIZE, 5)) + [WINDOW_SIZE-1]  # 0부터 WINDOW_SIZE까지 5 간격으로, 마지막에 0초전 추가
ticktext = [x_labels[i] for i in tickvals]

'''
E_scr_pv,E_scr_sv, -> 0, 10
c_temp_pv,c_temp_sv -> 65 75
k_rpm_pv,k_rpm_sv -> 100 200
n_temp_pv,n_temp_sv -> 65 75
s_temp_pv,s_temp_s ->  65 75
'''
def draw_graph():
    global WINDOW_SIZE
    global CM_DF
    global cnt
    global x_labels

    col_pv = sr_list[graph_idx][0]
    col_sv = sr_list[graph_idx][1]
    new_fig = px.line(x=range(WINDOW_SIZE), y=col_pv[cnt:cnt+WINDOW_SIZE], markers=True)
    new_fig.update_traces(name="pv", showlegend=True, marker=dict(opacity=0.5)) # 기본 상태 그래프는 showlegend 안하면 밑에 sv 범례만 뜸 
    # 알파값 높을수록 진함

    # setting value 그래프 추가 
    new_fig.add_trace(go.Scatter(x=list(range(WINDOW_SIZE)), y=col_sv[cnt:cnt+WINDOW_SIZE], name="sv"))

    # 배경을 투명하게 설정, 주변부 없애기, 축범위 지정, 레이아웃 세로 길이 조금 줄임
    new_fig.update_layout(paper_bgcolor='rgba(0,0,0,0)',
                          margin=dict(t=0, b=0, l=0, r=0),
                          xaxis_range=[0, WINDOW_SIZE],  
                          yaxis_range=yaxis_list[graph_idx],
                          height=250,
                          xaxis_title="Time (s)",
                          yaxis_title=name_list[graph_idx] # y축 이름 설정
                          )
    
    # x축 레이블 설정
    new_fig.update_xaxes(
        tickvals = tickvals,
        ticktext= ticktext
    )
    
    cnt += 1
    new_graphJSON = json.dumps(new_fig, cls=plotly.utils.PlotlyJSONEncoder)
    return new_graphJSON
    


# @=>데코레이터 
@bp.route("/")
def index():
    return render_template("job_choice.html")


# dashboard =========================================================================
@bp.route("/dash")
def dash():
    # global WINDOW_SIZE
    # global CM_DF
    # global cnt
    print("그래프 초기화")  # 로그 추가 -> python terminal에서 확인
    
    # col_pv = sr_list[graph_idx][0]
    # col_sv = sr_list[graph_idx][1]
    # new_fig = px.line(x=range(WINDOW_SIZE), y=col_pv[cnt:cnt+WINDOW_SIZE], markers=False)
    # new_fig.update_traces(name="pv", showlegend=True) # 기본 상태 그래프는 showlegend 안하면 밑에 sv 범례만 뜸 


    # # setting value 그래프 추가 
    # new_fig.add_trace(go.Scatter(x=list(range(WINDOW_SIZE)), y=col_sv[cnt:cnt+WINDOW_SIZE], name="sv"))

    # # 배경을 투명하게 설정, 주변부 없애기, 축범위 지정, 레이아웃 세로 길이 조금 줄임
    # new_fig.update_layout(paper_bgcolor='rgba(0,0,0,0)',
    #                       margin=dict(t=0, b=0, l=0, r=0),
    #                       yaxis_range=yaxis_list[graph_idx],
    #                       height=250)
    
    # new_graphJSON = json.dumps(new_fig, cls=plotly.utils.PlotlyJSONEncoder)
    new_graphJSON = draw_graph()
    
    return render_template("dash.html", title="Home", graph1JSON=new_graphJSON)


# 차트는 여기서 업데이트됨
@bp.route('/update_chart')
def update_chart():
    # global graph_idx 
    # global sr_list # 쌍으로 담겨 있음 sr_list[graph_idx]로 쌍에 접근 가능 
    # global WINDOW_SIZE
    # global CM_DF
    # global cnt
    print("Updating chart1...")  # 로그 추가 -> python terminal에서 확인
   
    # pv 측정값 그래프 그리기 
    # col_pv = sr_list[graph_idx][0]
    # col_sv = sr_list[graph_idx][1]
    # new_fig = px.line(x=range(WINDOW_SIZE), y=col_pv[cnt:cnt+WINDOW_SIZE], markers=False)
    # new_fig.update_traces(name="pv", showlegend=True) # 기본 상태 그래프는 showlegend 안하면 밑에 sv 범례만 뜸 
   

    # # setting value 그래프 추가 
    # new_fig.add_trace(go.Scatter(x=list(range(WINDOW_SIZE)), y=col_sv[cnt:cnt+WINDOW_SIZE], name="sv"))

    # # 배경을 투명하게 설정, 주변부 없애기, 축범위 지정, 레이아웃 세로 길이 조금 줄임
    # new_fig.update_layout(paper_bgcolor='rgba(0,0,0,0)',
    #                       margin=dict(t=0, b=0, l=0, r=0),
    #                       yaxis_range=yaxis_list[graph_idx],
    #                       height=250,
    #                       xaxis_title="Time (s)",
    #                       yaxis_title=name_list[graph_idx] # y축 이름 설정
    #                       )
    
    # new_graphJSON = json.dumps(new_fig, cls=plotly.utils.PlotlyJSONEncoder)
    new_graphJSON = draw_graph()
    # cnt += 1 # WINDOW 이동
    return jsonify({"new_graphJSON": new_graphJSON, "msg" : "화이팅!"})




# 1번 공장 =======================================================================================
@bp.route('/factory1')
def factory1():
    return render_template("factory1.html")

@bp.route('/factory2')
def factory2():
    return render_template("factory2.html")

@bp.route('/factory2_machine2_2')
def factory2_machine2_2():
    return render_template("factory2_machine2_2.html")

@bp.route('/factory3')
def factory3():
    return render_template("factory3.html")

################################################### 값 확인 
@bp.route('/click_button', methods=['POST'])
def click_button():
    global graph_idx
    global name_list
    data = request.get_json()
    print(data)
    name_list = ["E_scr", "c_temp", "k_rpm", "n_temp", "s_temp"]
    for i in range(len(name_list)):
        if data["button"] == name_list[i]:
            graph_idx = i
    '''
    E_scr_pv,E_scr_sv,
    c_temp_pv,c_temp_sv,
    k_rpm_pv,k_rpm_sv,       
    n_temp_pv,n_temp_sv,
    s_temp_pv,s_temp_sv
    '''
    # print(graph_idx) # 0, 1, 2, 3, 4
    return jsonify({"message": "버튼이 클릭되었습니다!"})

################################################### employee 전용 ###################################################
@bp.route('/employee_dash')
def employee_dash():
    return render_template("temp.html")