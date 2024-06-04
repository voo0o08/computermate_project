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
wrong_cnt = 0

bp = Blueprint("main", __name__, url_prefix="/")

CM_DF = pd.read_csv("./cm_web/static/data/result_ver1.csv")
DATA_LENGTH = len(CM_DF)

# total page를 위한 데이터 시작
TOTAL_DF = pd.read_csv("./cm_web/static/data/for_total.csv")
pre_data = TOTAL_DF["previouse_data"]
real_data = TOTAL_DF["data"]

WANT_DAY = 40 # 최근 n일 간(데이터는 주작)
day_length = int(np.floor(len(TOTAL_DF)/WANT_DAY))

max_len = day_length

A_counts = []
B_counts = []
C_counts = []
for i in range(WANT_DAY):
    # 조각조각 탐색 
    temp_list = pre_data[:max_len]
    # real_data[:max_len+day_length]
    
    A_cnt = len([num for num in temp_list if 2.9 <= num <= 3.1])            # A
    B_cnt = len([num for num in temp_list if 2.8 <= num <= 3.2]) - A_cnt    # B
    C_cnt = len(temp_list) - (A_cnt + B_cnt)                                # C
    
    A_counts.append(A_cnt)
    B_counts.append(B_cnt)
    C_counts.append(C_cnt)
    
    max_len += day_length
# total page를 위한 데이터 끝



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

scale_pv = CM_DF["scale_pv"]

sr_list = ((E_scr_pv, E_scr_sv),
           (c_temp_pv, c_temp_sv),
           (k_rpm_pv, k_rpm_sv),
           (n_temp_pv, n_temp_sv),
           (s_temp_pv, s_temp_sv))
yaxis_list = ((0, 10),
              (55, 75),
              (120, 220),
              (55, 75),
              (55, 75))
x_values = np.linspace(-WINDOW_SIZE, 0, WINDOW_SIZE, endpoint=False)
x_labels = [f"{int(x)}초" if x != 0 else "현재" for x in x_values]

# 5초 단위로 x축 레이블 설정
tickvals = list(range(0, WINDOW_SIZE, 5)) + [WINDOW_SIZE-1]  # 0부터 WINDOW_SIZE까지 5 간격으로, 마지막에 0초전 추가
ticktext = [x_labels[i] for i in tickvals]
ticktext[0] = " "
'''
E_scr_pv,E_scr_sv, -> 0, 10
c_temp_pv,c_temp_sv -> 65 75
k_rpm_pv,k_rpm_sv -> 100 200
n_temp_pv,n_temp_sv -> 65 75
s_temp_pv,s_temp_s ->  65 75
'''

k_name_list = ["스크류 속도", "챔버 온도", "칼날 속도", "노즐 온도", "스크류 온도"]

# 각 column의 성분을 그려주는 그래프 
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
                          margin=dict(t=30, b=30, l=100, r=0),
                          xaxis_range=[0, WINDOW_SIZE],  
                          yaxis_range=yaxis_list[graph_idx],
                          height=300,
                          xaxis_title="경과시간 (초)",
                          yaxis_title=k_name_list[graph_idx] # y축 이름 설정
                          )
    
    # x축 레이블 설정
    new_fig.update_xaxes(
        tickvals = tickvals,
        ticktext= ticktext
    )
    
    cnt += 1
    new_graphJSON = json.dumps(new_fig, cls=plotly.utils.PlotlyJSONEncoder)
    return new_graphJSON
    
# dash 도넛 차트 그리는 함수 
def draw_donut(title, colors):
    global cnt
    global DATA_LENGTH
    global wrong_cnt
    
    if title == "불량률":
        if scale_pv[cnt] <= 2.9 or scale_pv[cnt] >= 3.09:
            wrong_cnt += 1
    # col_pv = sr_list[graph_idx][0]
    # col_sv = sr_list[graph_idx][1]
    
    # 불량품 그래프 
    new_fig = go.Figure(data=[go.Pie(
    values=[wrong_cnt, DATA_LENGTH - wrong_cnt] if title=="불량률" else [cnt, DATA_LENGTH - cnt],
    labels=['Used', 'Remaining'],
    marker=dict(colors=colors),
    textinfo='none',
    hole=.4,
    rotation=0,
    direction='clockwise',
    type='pie'
    )])
    

    # 배경을 투명하게 설정, 주변부 없애기, 축범위 지정, 레이아웃 세로 길이 조금 줄임
    new_fig.update_layout(
        title=dict(
            text=title,
            x=0.5,  # 중앙 정렬
            xanchor='center',  # 중앙 정렬
            font=dict(size=15)  # 제목 폰트 크기
        ),
        height=245,
        width=245,
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',  # 배경을 투명하게 설정
        plot_bgcolor='rgba(0,0,0,0)',  # 배경을 투명하게 설정
        margin=dict(t=40, b=0, l=0, r=0),
        annotations=[
            dict(
                font=dict(size=15),
                showarrow=False,
                text=str(wrong_cnt) if title=="불량률" else str(cnt),
                x=0.5,
                y=0.5
            )
        ]
    )
    
    new_donutJSON = json.dumps(new_fig, cls=plotly.utils.PlotlyJSONEncoder)
    return new_donutJSON
    

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
    
   
    new_graphJSON = draw_graph()
    
    return render_template("dash.html", title="Home", graph1JSON=new_graphJSON)

# total + 누적 그래프 생성 
@bp.route("/total")
def total():
    # 10월 무게 데이터에 대한 series
    global pre_data 
    global real_data 
    
    pre_acc = [] # 파란색
    real_acc = [] # 빨간색 
    pre_sum = 0
    pre_real = 0
    for idx in range(len(pre_data)):
        pre_sum += ((pre_data[idx] - 3)*1)
        pre_real += ((real_data[idx] - 3)*1)
        pre_acc.append(pre_sum)
        real_acc.append(pre_real)

    # Create a scatter plot
    accumulate_fig = go.Figure()

    # pre_acc
    accumulate_fig.add_trace(go.Scatter(
        x=list(range(1, len(pre_acc) + 1)),
        y=pre_acc,
        mode='lines', # +markers
        fill='tozeroy',  # Fill to the x-axis
        fillcolor='rgba(0, 0, 255, 0.3)',  # Blue color with transparency
        name='예측값'
    ))
    
    # real_acc
    accumulate_fig.add_trace(go.Scatter(
        x=list(range(1, len(real_acc) + 1)),
        y=real_acc,
        mode='lines', # +markers
        fill='tozeroy',  # Fill to the x-axis
        fillcolor='rgba(255, 0, 0, 0.3)',  
        name='실제값'
    ))

    # Update layout for transparent background and tight layout
    accumulate_fig.update_layout(
        xaxis_title='기간',
        yaxis_title='누적값',
        paper_bgcolor='rgba(0,0,0,0)',  # Transparent background
        plot_bgcolor='rgba(0,0,0,0)',   # Transparent background
        width=1500, height=300,  # Reduced size
        margin=dict(l=0, r=0, t=20, b=20) # Tight layout
    )
    accumulate_graphJSON = json.dumps(accumulate_fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    ################################################### 품질 그래프 
    global A_counts, B_counts, C_counts
    x_label = list(range(day_length))
    # Create the stacked bar plot
    quality_fig = go.Figure()

    quality_fig.add_trace(go.Bar(
        x=x_label,
        y=A_counts,
        name='A 2.9~3.1',
        marker_color='#21A675',
        marker_line_width=0  # Remove border
    ))

    quality_fig.add_trace(go.Bar(
        x=x_label,
        y=B_counts,
        name='B 2.8~3.2',
        marker_color='#F28705',
        marker_line_width=0  # Remove border
    ))

    quality_fig.add_trace(go.Bar(
        x=x_label,
        y=C_counts,
        name='C Other',
        marker_color='#F23827',
        marker_line_width=0  # Remove border
    ))

    # Update layout for stacked bars
    quality_fig.update_layout(
        barmode='stack', 
        # title='야야야', 
        paper_bgcolor='rgba(0,0,0,0)', 
        plot_bgcolor='rgba(0,0,0,0)', 
        font=dict(color='black'),
        width=1000, height=300,  # 그래프 사이즈
        xaxis=dict(title='날짜', showgrid=False, zeroline=False),
        yaxis=dict(title='생산량', showgrid=False, zeroline=False),
        legend=dict(bgcolor='rgba(0,0,0,0)')
    )
    
    quality_graphJSON = json.dumps(quality_fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    return render_template("total.html", accumulate_graphJSON=accumulate_graphJSON, quality_graphJSON=quality_graphJSON)


@bp.route("/learning")
def learning():
    return render_template("learning.html")


# 차트는 여기서 업데이트됨
@bp.route('/update_chart')
def update_chart():
    # global graph_idx 
    # global sr_list # 쌍으로 담겨 있음 sr_list[graph_idx]로 쌍에 접근 가능 
    # global WINDOW_SIZE
    # global CM_DF
    # global cnt
    
    # print("Updating chart1...")  # 로그 추가 -> python terminal에서 확인
   
   
    new_graphJSON = draw_graph()
    # cnt += 1 # WINDOW 이동
    return jsonify({"new_graphJSON": new_graphJSON, "msg" : "화이팅!"})


# 규량님 거 JS to Python : 도넛 차트==================================================================================
@bp.route('/update_donut')
def update_donut():
    print("도넛 업데이트 중...")
    new_donut2JSON = draw_donut("생산량", ['#1FA680', '#ffffff'])
    new_donut3JSON = draw_donut("불량률", ['#FFA500', '#ffffff'])
    return jsonify({"new_donut2JSON": new_donut2JSON, "new_donut3JSON":new_donut3JSON," msg" : "도넛 차트 data.msg"})


# 규량 : 계기판 표현=================================================================================
@bp.route('/update_gauges')
def update_gauges():
    global cnt
    global WINDOW_SIZE
    data = {
        "챔버 온도": float(c_temp_pv[cnt+WINDOW_SIZE]),
        "칼날 속도": float(k_rpm_pv[cnt+WINDOW_SIZE]),
        "노즐 온도": float(n_temp_pv[cnt+WINDOW_SIZE]),
        "스크류 온도": float(s_temp_pv[cnt+WINDOW_SIZE]),
        "중량 예측": float(scale_pv[cnt+WINDOW_SIZE]),
        "스크류 속도": float(E_scr_pv[cnt+WINDOW_SIZE])
    }
    #cnt = (cnt + 1) % len(c_temp_pv)  # 데이터를 순환하도록 cnt를 리셋합니다.
    # print('게이지 오류!',c_temp_pv[cnt+WINDOW_SIZE])
    return jsonify(data)


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
    return render_template("employee_dash.html")