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
  setInterval(updateChart, 200);
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
