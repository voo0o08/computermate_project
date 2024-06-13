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

    // // 동영상 이벤트 처리
    // video.addEventListener('play', function() {
    //     // console.log('동영상 재생 시작');
    // });

    // video.addEventListener('pause', function() {
    //     // console.log('동영상 일시 중지');
    // });

    // video.addEventListener('ended', function() {
    //     console.log('동영상 종료');
    //     video.currentTime=0;
    //     video.play();
    // });
});
