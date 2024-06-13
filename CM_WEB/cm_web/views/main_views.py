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
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

# 그래프 폰트 크긱 지정 
TITLE_SIZE = 30
LEGEND_SIZE = 20
TICK_TITLE_SIZE = 20
TICK_SIZE = 15

WINDOW_SIZE = 50
cnt = 0
wrong_cnt = 0

bp = Blueprint("main", __name__, url_prefix="/")

CM_DF = pd.read_csv("./cm_web/static/data/result_ver2.csv")
DATA_LENGTH = len(CM_DF)

# total page를 위한 데이터 시작
# TOTAL_DF = pd.read_csv("./cm_web/static/data/for_total.csv")
TOTAL_DF = pd.read_csv("./cm_web/static/data/LSM0610.csv")
real_data = TOTAL_DF["previouse_data"] # 원본 데이터
predict_data = TOTAL_DF["data"] # 우리가 예측한 데이터 

# 현재 날짜와 시각을 가져옴
now = datetime.now()
WANT_DAY = 7 # 최근 n일 간(데이터는 주작)
END_DAY = now.strftime("%m/%d")
START_DAY = (now + timedelta(days=-WANT_DAY)).strftime("%m/%d")
# print(start_day,"\n" ,end_day)
day_length = int(np.floor(len(TOTAL_DF)/WANT_DAY))

max_len = day_length

A_counts = []
B_counts = []
C_counts = []
for i in range(WANT_DAY):
    # 조각조각 탐색 
    temp_list = predict_data[:max_len]
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
    new_fig.update_traces(name="측정값", showlegend=True, marker=dict(opacity=0.5))  # 기본 상태 그래프는 showlegend 안하면 밑에 sv 범례만 뜸 

    # setting value 그래프 추가 
    new_fig.add_trace(go.Scatter(x=list(range(WINDOW_SIZE)), y=col_sv[cnt:cnt+WINDOW_SIZE], name="세팅값"))

    # 배경을 투명하게 설정, 주변부 없애기, 축범위 지정, 레이아웃 세로 길이 조금 줄임
    new_fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(t=30, b=30, l=100, r=0),
        xaxis_range=[0, WINDOW_SIZE],  
        yaxis_range=yaxis_list[graph_idx],
        height=300,
        xaxis_title="경과시간 (초)",
        xaxis=dict(
            title="경과시간 (초)",
            title_font=dict(size=TICK_TITLE_SIZE),
            tickfont=dict(size=TICK_SIZE)
        ),
        yaxis=dict(
            title=k_name_list[graph_idx],
            title_font=dict(size=TICK_TITLE_SIZE),
            tickfont=dict(size=TICK_SIZE)
        ),
        legend=dict(
            font=dict(size=20)
        )
    )
    
    # x축 레이블 설정
    new_fig.update_xaxes(
        tickvals=tickvals,
        ticktext=ticktext
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
    
   
    new_graphJSON = draw_graph()
    
    return render_template("dash.html", title="Home", graph1JSON=new_graphJSON)

# total + 누적 그래프 생성 
@bp.route("/total")
def total():
    # 10월 무게 데이터에 대한 series
    global real_data # 
    global predict_data # 예측 데이터
    global now
    
    pre_acc = [] # 파란색 -> AI 도입 후
    real_acc = [] # 빨간색 -> AI 도입 전
    pre_sum = 0
    real_sum = 0
    
    for idx in range(len(real_data)):
        pre_sum += (abs(predict_data[idx] - 3)*1)
        real_sum += (abs(real_data[idx] - 3)*1)
        pre_acc.append(pre_sum)
        real_acc.append(real_sum)
    
    real_1 = real_acc[-1]
    pre_1 = pre_acc[-1]
    precent = round(abs(real_1-pre_1)/real_1 * 100,2)
    # print(acc_sub)

    # Create a scatter plot
    accumulate_fig = go.Figure()

    # pre_acc (AI 도입 후)
    accumulate_fig.add_trace(go.Scatter(
        x=list(range(1, len(pre_acc) + 1)),
        y=pre_acc,
        mode='lines', # +markers
        # fill='tozeroy',  # Fill to the x-axis
        fill='tozeroy',
        fillcolor='rgba(200, 207, 160, 0.7)',  # Blue color with transparency rgb(200, 207, 160)
        line=dict(color='rgba(200, 207, 160, 1)'),
        name='AI도입 후'
    ))
    
    # real_acc (AI 도입 전)
    accumulate_fig.add_trace(go.Scatter(
        x=list(range(1, len(real_acc) + 1)),
        y=real_acc,
        mode='lines', # +markers
        fill='tonexty',  # Fill to the previous trace
        fillcolor='rgba(239, 156, 102, 0.5)',  # rgb(252, 220, 148)
        line=dict(color='rgba(239, 156, 102, 1)'),
        name='AI도입 전'
    ))
    
    
    last_month = (now - relativedelta(months=1)).month
    # Update layout for transparent background and tight layout
    acc_sub = abs(real_1-pre_1)
    print("==================================================",round(acc_sub*2.39,2))
    # text=f'지난 달({last_month}월)은 AI 도입 전보다 {round(acc_sub*2.39,2)}원 절약'
    accumulate_fig.update_layout(
        legend=dict(font=dict(size=20)),
        title=dict(
            text=f'지난 달({last_month}월)은 AI 도입 전보다 {precent}% 절약',  # 그래프 제목 설정
            font=dict(size=TITLE_SIZE, color='black')  # 제목 글꼴 크기 및 색상 설정
        ),
        # xaxis_title=str(last_month)+"월",

        paper_bgcolor='rgba(0,0,0,0)',  # Transparent background
        plot_bgcolor='rgba(0,0,0,0)',   # Transparent background
        width=1500, height=350,  # Reduced size
        margin=dict(l=0, r=0, t=50, b=0), # Tight layout
        showlegend=True,
        yaxis=dict(
            title='|val-3| 누적값[g]',
            title_font=dict(size=TICK_TITLE_SIZE, color='black'),  # y축 타이틀 글씨 설정
            tickfont=dict(size=TICK_SIZE)),
        xaxis=dict(
            # title=str(last_month) + "월",
            # title_font=dict(size=20, color='black'),  # x축 타이틀 글씨 설정
            tickfont=dict(size=TICK_SIZE),
            tickvals=[1, len(predict_data)/2, len(predict_data)],  # x축 눈금 값 설정 (1일, 15일, 30일)
            ticktext=["1일", "15일", "31일"],  # 눈금 레이블 설정
            ),
    )
    
    accumulate_graphJSON = json.dumps(accumulate_fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    ################################################### 품질 그래프 
    global A_counts, B_counts, C_counts
    x_label = list(range(1, day_length+1))
    # Create the stacked bar plot
    quality_fig = go.Figure()

    quality_fig.add_trace(go.Bar(
        x=x_label,
        y=A_counts,
        name='A등급:2.9~3.1g',
        marker_color='#21A675',
        marker_line_width=0  # Remove border
    ))

    quality_fig.add_trace(go.Bar(
        x=x_label,
        y=B_counts,
        name='B등급:2.8~3.2g',
        marker_color='#F28705',
        marker_line_width=0  # Remove border
    ))

    quality_fig.add_trace(go.Bar(
        x=x_label,
        y=C_counts,
        name='C등급:~2.8 or 3.2~',
        marker_color='#F23827',
        marker_line_width=0  # Remove border
    ))
    
    x_day_list = []
    for i in range(WANT_DAY):
        day = now + timedelta(days=-WANT_DAY+i)
        x_day_list.append(day.strftime("%m-%d"))
    print(x_day_list) # ['05-31', '06-01', '06-02', '06-03', '06-04', '06-05', '06-06']
        
    # print([range(WANT_DAY)])
    # Update layout for stacked bars
    quality_fig.update_layout(
        barmode='stack', 
        title=dict(
            text=f'최근 일주일 생산품 현황({START_DAY}~{END_DAY})',  # 그래프 제목 설정
            font=dict(size=TITLE_SIZE, color='black')  # 제목 글꼴 크기 및 색상 설정
        ),
        paper_bgcolor='rgba(0,0,0,0)', 
        plot_bgcolor='rgba(0,0,0,0)', 
        font=dict(color='black'),
        width=850, 
        height=350,  # 그래프 사이즈
        # xaxis=dict(title='날짜', showgrid=False, zeroline=False),
        
        # title_font=dict(size=20, color='black', weight='bold'),  # y축 타이틀 글씨 설정
        #     tickfont=dict(size=15)),
        yaxis=dict(
            title='생산량[개]', showgrid=False, zeroline=False,
            title_font=dict(size=TICK_TITLE_SIZE, color='black'),
            tickfont=dict(size=TICK_SIZE)
            ),
        title_x = 0.5,
        # title_y = 1.5,
        legend=dict(
            x=0.0,  # 범례의 x 좌표 (그래프의 오른쪽에 위치하도록 설정)
            y=1.0,  # 범례의 y 좌표 (그래프의 상단에 위치하도록 설정)
            bgcolor='rgba(0,0,0,0)', 
            font=dict(size=LEGEND_SIZE)
            ),
        
        margin=dict(l=0, r=0, t=50, b=0),
        xaxis=dict(
            title="날짜",
            tickvals=list(range(1,WANT_DAY+1)),  # x축 눈금 값 설정 (1일, 15일, 30일)
            ticktext=x_day_list,  # 눈금 레이블 설정
            title_font=dict(size=TICK_TITLE_SIZE, color='black'),
            tickfont=dict(size=TICK_SIZE)
            )
    )
    
    quality_graphJSON = json.dumps(quality_fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    return render_template("total.html", accumulate_graphJSON=accumulate_graphJSON, quality_graphJSON=quality_graphJSON)


# @bp.route("/learning")
# def learning():
#     return render_template("learning.html")


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

quality_list = [10, 30, 100] # c, b, a 순서
# 규량님 거 JS to Python : 품질 차트==================================================================================
@bp.route('/update_donut')
def update_donut():
    global cnt
    global quality_list
    global scale_pv
    '''
    발산 막대 차트 
    #21A675 녹색
    #F28705 주황색
    #F23827 빨간색
    '''
  
    if 2.9 <= scale_pv[cnt] <= 3.1:
        quality_list[2] += 1
    elif 2.8 <= scale_pv[cnt] <= 3.2:
        quality_list[1] += 1
    else:
        quality_list[0] += 1
        
    categories = ['C등급', 'B등급', 'A등급']  # y축에 표시될 카테고리
    counts = [quality_list[0], quality_list[1], quality_list[2]]  # 각 카테고리에 해당하는 x축 값
    colors = ['#F23827', '#F28705', '#21A675']  # 막대 색상 설정 (C, B, A 순서)
    names = ['~2.8g|3.2g ~', '2.8 ~ 3.2g', '2.9 ~ 3.1g']  # 범례에 표시될 이름

    # diverging_chartJSON
    diverging_fig = go.Figure()  # diverging_Figure 객체를 생성

    # 막대 그래프 추가
    for count, category, color, name in zip(counts, categories, colors, names):
        diverging_fig.add_trace(go.Bar(
            x=[count],
            y=[category],
            orientation='h',  # 수평 막대 그래프로 설정
            marker=dict(color=color),  # 막대 색상 설정
            text=[count],  # 각 막대에 표시될 텍스트
            textposition='auto',  # 텍스트 위치 자동 설정
            name=name  # 범례에 표시될 이름
        ))

    # 레이아웃 업데이트
    diverging_fig.update_layout(
        title=dict(
            text='일일 생산 고무링 품질 수준',  # 그래프 제목 설정
            font=dict(size=TITLE_SIZE, color='black')  # 제목 글꼴 크기 및 색상 설정
        ),
        xaxis=dict(title='등급별 고무링 개수', showgrid=False, range=[0, 1000], tickfont=dict(size=TICK_SIZE), title_font=dict(size=TICK_TITLE_SIZE)),  # x축 제목 설정, 그리드 라인 제거, 범위 설정
        yaxis=dict(title='', showgrid=False,tickfont=dict(size=TICK_SIZE)),  # y축 제목 제거 및 그리드 라인 제거
        barmode='stack',  # 막대 그래프 모드 설정 (스택 모드)
        margin=dict(l=0, r=0, t=50, b=0),  # 그래프의 여백을 최소화
        paper_bgcolor='rgba(0,0,0,0)',  # 투명 배경 설정
        plot_bgcolor='rgba(0,0,0,0)',  # 투명 플롯 영역 설정
        font=dict(color='black'),  # 글꼴 색상 설정
        showlegend=True,  # 범례 표시 설정
        height=350,  # 그래프 높이 설정
        width=600,
        legend=dict(
            x=0.7,  # 범례의 x 좌표 (그래프의 오른쪽에 위치하도록 설정)
            y=0.1,  # 범례의 y 좌표 (그래프의 상단에 위치하도록 설정)
            bgcolor='rgba(255,255,255,0)',  # 범례 배경 색상 (반투명 흰색)
            font=dict(
                size=20,  # 범례 글꼴 크기
                color='black'  # 범례 글꼴 색상
            )
        )
    )
    diverging_chartJSON = json.dumps(diverging_fig, cls=plotly.utils.PlotlyJSONEncoder)
    return jsonify({"diverging_chartJSON": diverging_chartJSON, "msg": "발산 막대 차트 data.msg"})


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


@bp.route('/data_test', methods=['POST'])
def data_test():
    data = request.get_json()
    print(data["startDate"])
    print(data["endDate"])

    return jsonify({"message": "날짜는 고마 잘 넘어왔심더"})
