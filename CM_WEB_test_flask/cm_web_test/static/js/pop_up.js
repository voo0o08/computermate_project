document.addEventListener("DOMContentLoaded", function() {
    const learningLink = document.getElementById("learning-link");
    const popup = document.getElementById("popup");
    const confirmPopup = document.getElementById("confirm_popup");
    const popupOverlay = document.getElementById("popup_overlay");
    const relearningForm = document.getElementById("relearning-form");
    const confirmText = document.getElementById("confirm_text");
    const confirmButton = document.getElementById("confirm_button");

    learningLink.addEventListener("click", function(event) {
        event.preventDefault();
        popup.style.display = "block";
        popupOverlay.style.display = "block";
    });

    popupOverlay.addEventListener("click", function() {
        closePopup();
        closeConfirmPopup();
    });

    relearningForm.addEventListener("submit", function(event) {
        event.preventDefault();
        const startDate = document.getElementById("start-date").value;
        const endDate = document.getElementById("end-date").value;
        if (startDate && endDate) {
            confirmText.innerHTML = `이 날짜에 재학습 하시겠습니까?<br><br>시작 일자: ${startDate}<br>종료 일자: ${endDate}`;
            popup.style.display = "none";
            confirmPopup.style.display = "block";
        } else {
            alert("날짜를 선택해주세요.");
        }
    });

    confirmButton.addEventListener("click", function() {
        // 여기서는 단순히 확인 메시지만 출력하고 팝업창을 닫습니다.
        const startDate = document.getElementById("start-date").value;
        const endDate = document.getElementById("end-date").value;
        alert(`재학습이 완료되었습니다.`);
        closeConfirmPopup();
        closePopup();
    });

});

function closePopup() {
    document.getElementById("popup").style.display = "none";
    document.getElementById("popup_overlay").style.display = "none";
}

function closeConfirmPopup() {
    document.getElementById("confirm_popup").style.display = "none";
    document.getElementById("popup_overlay").style.display = "none";
}
