var $j = jQuery.noConflict(); // $j로 jQuery 객체 저장 -> 이거 없으면  충돌남
console.log("jQuery type:", typeof $j);  // jQuery가 올바르게 로드되었는지 확인

$j(document).ready(function() {
  var graph1DataElement = $j('#graph1-data');
  // 그래프 초기화 
  if (graph1DataElement.length) {
    try {
      var graph1 = JSON.parse(graph1DataElement.text());
      Plotly.newPlot("chart1", graph1, {});  // 차트 생성
    } catch (e) {
      console.error("Error parsing JSON data:", e);
    }
  } else {
    console.error("#graph1-data element not found");
  }

  // 그래프 업데이트 
  function updateChart() {
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

  setInterval(updateChart, 500);
});