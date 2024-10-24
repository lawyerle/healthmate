var slideIndex = 1;
// 다음/이전 컨트롤
function plusSlides(n) {
    showSlides(slideIndex += n);
}

function showSlides(n) {
    var i;
    var slides = document.getElementsByClassName("healthcare-medicine-database-2");
    var eclipses = document.getElementsByClassName("ellipse-1787");
    var navi = document.getElementsByClassName("onboarding-2");
    
    if (n > slides.length) {
        navi[0].style.display = "none";
        window.location.href = "home"
    };
    if (n < 1) { slideIndex = slides.length };
    for (i = 0; i < slides.length; i++) {
        slides[i].style.display = "none";
        eclipses[i].style.backgroundColor = "#ccc"
    }
    slides[slideIndex - 1].style.display = "block";
    eclipses[slideIndex - 1].style.backgroundColor = "#000";
    navi[0].style.display = "flex";
}

function addButtonListener() {
    const group2018776028 = document.querySelectorAll(".group-2018776028");
    const group2018776029 = document.querySelectorAll(".group-2018776029");

    group2018776028.forEach(img => {
        img.addEventListener("click", () => plusSlides(-1));
    });

    group2018776029.forEach(img => {
        img.addEventListener("click", () => plusSlides(1));
    });  
}

function addStartButtonListener() {
    const frame1171275337 = document.querySelectorAll(".frame-1171275337");

    frame1171275337.forEach(btn => {
        btn.addEventListener("click", () => { window.location.href = "chatui"; });
    })
    
}

