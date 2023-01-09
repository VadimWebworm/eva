$(function () {
    var heightHeaderFooter = $(".header").height();
    $(".screen-height").height($(window).height() - heightHeaderFooter);

    // $(window).resize(function () {
    //     $(".screen-height").height($(window).height());
    // });
    if(!$(".btnPrev").length){
        $('.quizInnerBtn').addClass('quizInnerNonBtn');
        }
    $(".start-stop").click(function () {
        $('.quizInnerItem h4').removeClass('animation-true').eq($(this).index() - 1).addClass("animation-true");
        $("button").removeClass("active").eq($(this).index() - 1).addClass("active");
        if(!$(".btnPrev").length){
            $('.quizInnerBtn').addClass('quizInnerNonBtn');
            }
        if ($("#stop").hasClass("active")){
            $(".btnNext").removeClass("nonvision");
            if(!$(".btnPrev").length){
                $('.quizInnerBtn').removeClass('quizInnerNonBtn');
                }
        }else{
            $(".btnNext").addClass("nonvision");
        }
    });
    // $("#stop").click(function(){
        
    // })

    $('.sliderInner').slick({
        fade: true,
        arrows: false,
        focusOnSelect: false,
        autoplay: true,
        autoplaySpeed: 2000,
        speed: 2500,
    });
});

// let btn = document.querySelector('.btnNext');
// let stop = document.getElementById('stop');
// stop.addEventListener("click", (e) => {
//     stop.classList.add('time')
//     console.log(document.getElementById('stop').classList)
//     console.log('yes')
//     btn.classList.remove('nonvision')
    


// })
// console.log(stop.classList)





