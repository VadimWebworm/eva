$(function () {
    var heightHeaderFooter = $(".header").height();
    function setHeiHeight() {
        $(".screen-height").height($(window).height() - heightHeaderFooter);
    };
    setHeiHeight();
    $(window).resize( setHeiHeight );
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
    $('.sliderInner').slick({
        fade: true,
        arrows: false,
        focusOnSelect: false,
        autoplay: true,
        autoplaySpeed: 2000,
        speed: 2500,
    });
});






