var $j = jQuery.noConflict(); // $j로 jQuery 객체 저장 -> 이거 없으면  충돌남
console.log("jQuery type:", typeof $j);  // jQuery가 올바르게 로드되었는지 확인

// $(document).ready 블록 내부에 있는 코드는 문서가 완전히 로드된 후 실행
$j(document).ready(function() {
  var graph1DataElement = $j('#graph1-data');
  // 그래프 초기화 
  if (graph1DataElement.length) {
    try {
      var graph1 = JSON.parse(graph1DataElement.text());
      Plotly.newPlot("chart1", graph1, {});  // 차트 생성
      console.log("chart ready");
    } catch (e) {
      console.error("Error parsing JSON data:", e);
    }
  } else {
    console.error("#graph1-data element not found");
  }

  // // buttons = 버튼 전체 선택 
  // let buttons = document.querySelectorAll('.updatemenu-item-rect');
  // console.log(`======= buttons =======`)
  // console.log(`${buttons}`)
  // // 각 버튼에 대해 클릭 이벤트 리스너 추가
  // buttons.forEach(button => {
  //   button.onclick = function() {
  //     console.log('안녕하세요!');
  //   };
  // });
  

// 그래프 업데이트 
function updateChart(now_button) {
  // update_chart 뭔지 잘 보기 여러가지 version이 있어욤
  $j.getJSON('/update_chart', function(data) {
    console.log("Data received:", data);  // 콘솔 로그 추가
    console.log(data.msg);
    
    try {
      var new_graph = JSON.parse(data.new_graphJSON);  // JSON 문자열을 객체로 변환
      Plotly.react("chart1", new_graph.data, new_graph.layout);  // 차트 업데이트
    } catch (e) {
      console.error("Error parsing JSON data:", e);
    }
  }).fail(function(jqXHR, textStatus, errorThrown) {
    console.error("AJAX request failed:", textStatus, errorThrown);  // 에러 로그 추가
  });
  }
  setInterval(updateChart, term);
});
// ready 끝

// let now_button = "E_scr" // 그래프 초기 값 설정 
// // buttons = 버튼 전체 선택 
// let buttons = document.querySelectorAll('.button_');

// console.log(`======= buttons =======`)
// console.log(`${buttons}`)
// // 각 버튼에 대해 클릭 이벤트 리스너 추가
// buttons.forEach(button => {
//   button.onclick = function() {
//     console.log(`Button text => ${this.textContent}`);
//   };
//   now_button = this.textContent

document.addEventListener("DOMContentLoaded", function() {
  // 버튼들을 가져옵니다.
  let buttons = document.querySelectorAll('.button_');

  // 각 버튼에 대해 클릭 이벤트 리스너를 추가합니다.
  buttons.forEach(button => {
    button.addEventListener("click", function() {
      let buttonValue = this.value; // 클릭된 버튼의 값 가져오기

      // 서버로 AJAX 요청을 보냅니다.
      let xhr = new XMLHttpRequest();
      xhr.open("POST", "/click_button"); // 요청을 보낼 URL을 지정합니다.
      xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
      xhr.onload = function() {
        if (xhr.status == 200) {
          console.log("Button value sent to server:", buttonValue);
        } else {
          console.error("Request failed:", xhr.status, xhr.statusText);
        }
      };
      xhr.onerror = function() {
        console.error("Network error");
      };
      xhr.send(JSON.stringify({ button: buttonValue })); // 버튼의 값을 JSON 형태로 서버에 전송합니다.
    });
  });
});

document.addEventListener("DOMContentLoaded", function() {
  let buttons = document.querySelectorAll('.button_');
  
  buttons.forEach(button => {
      button.addEventListener('click', function() {
          buttons.forEach(btn => btn.classList.remove('active'));
          this.classList.add('active');
      });
  });
});

// 도넛 차트
// 초기 도넛 차트를 생성합니다.
function createDonutChart(id, value, title) {
  var colors;
  if(id === 'donut-chart-3') {
    colors = ['#FFA500', '#f2f2f2']; // 불량품 수의 막대 색상을 주황색으로 변경
  } else {
    colors = ['#1FA680', '#f2f2f2'];
  }

  var data = [{
      values: [value, 300 - value],
      labels: ['Used', 'Remaining'],
      marker: {
          colors: colors // 여기서 변경
      },
      textinfo: 'none',
      hole: .4,
      rotation: 0,
      direction: 'clockwise',
      type: 'pie'
  }];

  var layout = {
      title: title,
      height: 220,
      width: 220,
      showlegend: false,
      paper_bgcolor: 'rgba(0,0,0,0)', // 배경을 투명하게 설정
      plot_bgcolor: 'rgba(0,0,0,0)', // 배경을 투명하게 설정
      margin: { t: 30, b: 0, l: 0, r: 0 },

      annotations: [
          {
              font: {
                  size: 20
              },
              showarrow: false,
              text: value.toString(),
              x: 0.5,
              y: 0.5
          }
      ]
  };

  Plotly.newPlot(id, data, layout);
}

// 도넛 차트를 실시간으로 업데이트하는 함수
function updateDonutChart(id, value) {
  var colors;
  if(id === 'donut-chart-3') {
    colors = ['#FFA500', '#f2f2f2']; // 불량품 수의 막대 색상을 주황색으로 변경
  } else {
    colors = ['#1FA680', '#f2f2f2'];
  }

  Plotly.restyle(id, 'values', [[value, 300 - value]]);
  Plotly.restyle(id, 'marker.colors', [colors]); // 막대 색상 업데이트
  Plotly.relayout(id, {
      annotations: [{
          font: {
              size: 20
          },
          showarrow: false,
          text: value.toString(),
          x: 0.5,
          y: 0.5
      }]
  });
}

// 초기 차트 생성
createDonutChart('donut-chart-1', 500, '총 생산량'); // 총 생산량을 500으로 변경
createDonutChart('donut-chart-2', 400, '일일 생산량'); // 일일 생산량을 400으로 변경
createDonutChart('donut-chart-3', 100, '불량품 수'); // 불량품 수를 100으로 변경

// 초기값 설정
let value1 = 1;
let value2 = 1;
let value3 = 1;

// 매 0.1초마다 도넛 차트 값을 업데이트
setInterval(function() {
  // 값 증가 (예: 1씩 증가)
  value1 = (value1 % 301) + 1;
  value2 = (value2 % 301) + 1;
  value3 = (value3 % 301) + 1;

  // 도넛 차트 업데이트 함수 호출
  updateDonutChart('donut-chart-1', value1);
  updateDonutChart('donut-chart-2', value2);
  updateDonutChart('donut-chart-3', value3);
}, 100); // 0.1초마다 업데이트

document.addEventListener("DOMContentLoaded", function() {
  let buttons = document.querySelectorAll('.button_');

  buttons.forEach(button => {
      button.addEventListener('click', function() {
          buttons.forEach(btn => btn.classList.remove('active'));
          this.classList.add('active');
      });
  });
});




// 게이지 JS (새로 추가됨)
document.addEventListener("DOMContentLoaded", function() {
  function createGaugeChart(id, title, range) {
    var data = [{
      type: "indicator",
      mode: "gauge+number",
      value: 0,
      title: { text: title, font: { size: 15 } },
      gauge: {
        axis: { range: range*1.1 },
        bar: { color: "lightgray" },
        steps: [
          { range: [range[0], (range[1] - range[0]) * 0.5 + range[0]], color: "yellow" },
          { range: [(range[1] - range[0]) * 0.5 + range[0], range[1]], color: "green" },
          { range: [range[1], (range[1] -range[0])* 0.5 + range[1]], color: "yellow" }

        ]
      }
    }];

    var layout = {
      width: 200,
      height: 200,
      margin: { t: 0, b: 0 },
      paper_bgcolor: 'rgba(0,0,0,0)', // 배경을 투명하게 설정
      plot_bgcolor: 'rgba(0,0,0,0)', // 배경을 투명하게 설정
    };

    Plotly.newPlot(id, data, layout);
  }

  function updateGaugeChart(id, value) {
    var dataUpdate = {
      value: [value]
    };

    Plotly.update(id, dataUpdate);
  }

  function createAllGauges() {
    createGaugeChart('gauge-chart-1', '챔버 온도(℃)', [55, 75]);
    createGaugeChart('gauge-chart-2', '칼날 RPM', [100, 200]);
    createGaugeChart('gauge-chart-3', '노즐 온도(℃)', [55, 75]);
    createGaugeChart('gauge-chart-4', '스크류 온도(℃)', [55, 75]);
    createGaugeChart('gauge-chart-5', '중량 무게(g)', [2, 4]);
    createGaugeChart('gauge-chart-6', '스크류 속도', [6,9]);
  }

  function updateAllGauges() {
    $j.getJSON('/update_gauges', function(data) {
      updateGaugeChart('gauge-chart-1', data.c_temp_pv);
      updateGaugeChart('gauge-chart-2', data.k_rpm_pv);
      updateGaugeChart('gauge-chart-3', data.n_temp_pv);
      updateGaugeChart('gauge-chart-4', data.s_temp_pv);
      updateGaugeChart('gauge-chart-5', data.scale_pv);
      updateGaugeChart('gauge-chart-6', data.E_scr_pv);

    }).fail(function(jqXHR, textStatus, errorThrown) {
      console.error("AJAX request failed:", textStatus, errorThrown);
    });
  }

  createAllGauges();
  setInterval(updateAllGauges, term);
});

let term=500;