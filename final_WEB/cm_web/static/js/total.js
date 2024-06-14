document.addEventListener("DOMContentLoaded", function() {
    var graphJSON = JSON.parse(document.getElementById('accumulate-data').textContent);
    Plotly.newPlot('accumulate_graph', graphJSON.data, graphJSON.layout);
});

document.addEventListener("DOMContentLoaded", function() {
    var graphJSON = JSON.parse(document.getElementById('quality-data').textContent);
    Plotly.newPlot('quality_graph', graphJSON.data, graphJSON.layout);
});

document.addEventListener("DOMContentLoaded", function() {
    var video = document.getElementById('cctv');

    // 동영상 자동 재생 설정
    video.muted = true; // muted 속성 설정
    video.loop = true; // 반복 재생 설정
    video.play(); // 동영상 재생

});
