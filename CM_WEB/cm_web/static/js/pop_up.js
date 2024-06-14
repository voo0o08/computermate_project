document.addEventListener("DOMContentLoaded", function() {
    // 요소들을 변수에 저장
    const learningLink = document.getElementById("learning-link");
    const popup = document.getElementById("popup");
    const confirmPopup = document.getElementById("confirm_popup");
    const resultPopup = document.getElementById("result_popup");
    const updateConfirmPopup = document.getElementById("update_confirm_popup");
    const popupOverlay = document.getElementById("popup_overlay");
    const relearningForm = document.getElementById("relearning-form");
    const confirmText = document.getElementById("confirm_text");
    const resultText = document.getElementById("result_text");
    const confirmButton = document.getElementById("confirm_button");
    const updateButton = document.getElementById("update_button");
    const confirmUpdateButton = document.getElementById("confirm_update_button");
    const cancelUpdateButton = document.getElementById("cancel_update_button");

    const startDateInput = document.getElementById("start-date");
    const endDateInput = document.getElementById("end-date");

    // 유효한 데이터 범위
    const validStartDate = new Date("2023-05-01");
    const validEndDate = new Date("2023-09-30");
    
    // 재학습 링크 클릭 시 팝업 표시
    learningLink.addEventListener("click", function(event) {
        event.preventDefault();
        popup.style.display = "block";
        popupOverlay.style.display = "block";
    });

    // 팝업 오버레이 클릭 시 모든 팝업 닫기
    popupOverlay.addEventListener("click", function() {
        closePopup();
        closeConfirmPopup();
        closeResultPopup();
        closeUpdateConfirmPopup();
    });
    
    // 재학습 폼 제출 시 날짜 유효성 검사
    relearningForm.addEventListener("submit", function(event) {
        event.preventDefault();
        const startDate = new Date(startDateInput.value);
        const endDate = new Date(endDateInput.value);

        // 선택한 날짜가 유효 범위 내에 있는지 확인
        if (startDate < validStartDate || endDate > validEndDate) {
            alert("선택한 날짜에 데이터가 없습니다.");
        } else {
            // 유효한 날짜면 확인 팝업 표시
            confirmText.innerHTML = `이 날짜에 재학습 하시겠습니까?<br><br>시작 일자: ${startDateInput.value}<br>종료 일자: ${endDateInput.value}`;
            popup.style.display = "none";
            confirmPopup.style.display = "block";
        }
    });

    // 재학습 확인 버튼 클릭 시 결과 팝업 표시
    confirmButton.addEventListener("click", function() {
        const startDate = startDateInput.value;
        const endDate = endDateInput.value;
        
        // 무작위 MAPE 값 생성
        const oldStartDate = "2023-05-01";
        const oldEndDate = "2023-09-30";
        const oldPrediction = (Math.random() * (0.099 - 0.001) + 0.001).toFixed(4);
        const newPrediction = (Math.random() * (0.099 - 0.001) + 0.001).toFixed(4);
        
        // 결과 텍스트 업데이트
        resultText.innerHTML = `기존: ${oldStartDate}~${oldEndDate}, 평가값: ${oldPrediction}(MAPE값)<br><br>변경: ${startDate}~${endDate}, 평가값: ${newPrediction}(MAPE값)`;
        confirmPopup.style.display = "none";
        resultPopup.style.display = "block";
    });

    // 갱신 버튼 클릭 시 갱신 확인 팝업 표시
    updateButton.addEventListener("click", function() {
        updateConfirmPopup.style.display = "block";
    });

    // 갱신 확인 팝업에서 예 버튼 클릭 시 처리
    confirmUpdateButton.addEventListener("click", function() {
        const startDate = startDateInput.value;
        const endDate = endDateInput.value;
        alert(`선택한 기간 (${startDate} ~ ${endDate})에 대해 갱신하였습니다.`);
        closeUpdateConfirmPopup();
        closeResultPopup();
    });

    // 갱신 확인 팝업에서 아니요 버튼 클릭 시 팝업 닫기
    cancelUpdateButton.addEventListener("click", function() {
        closeUpdateConfirmPopup();
    });
});

// 팝업 닫기 함수들
function closePopup() {
    document.getElementById("popup").style.display = "none";
    document.getElementById("popup_overlay").style.display = "none";
}

function closeConfirmPopup() {
    document.getElementById("confirm_popup").style.display = "none";
    document.getElementById("popup_overlay").style.display = "none";
}

function closeResultPopup() {
    document.getElementById("result_popup").style.display = "none";
    document.getElementById("popup_overlay").style.display = "none";
}

function closeUpdateConfirmPopup() {
    document.getElementById("update_confirm_popup").style.display = "none";
    document.getElementById("popup_overlay").style.display = "none";
}

