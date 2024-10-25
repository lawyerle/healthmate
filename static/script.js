var slideIndex = 1;
showSlides(slideIndex);

// 다음/이전 컨트롤
function plusSlides(n) {
    showSlides(slideIndex += n);
}

function showSlides(n) {
    var i;
    var slides = document.getElementsByClassName("mySlides");
    if (n > slides.length) {slideIndex = 1}
    if (n < 1) {slideIndex = slides.length}
    for (i = 0; i < slides.length; i++) {
        slides[i].style.display = "none";
    }
    slides[slideIndex-1].style.display = "block";
}

// home에서 chat으로 이동
function navigateToChatUI(question) {
    window.location.href = '/chatui?question=' + encodeURIComponent(question);
}