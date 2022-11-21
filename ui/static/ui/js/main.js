$(function () {
    $(".screen-height").height($(window).height());

    $(window).resize(function () {
        $(".screen-height").height($(window).height());
    });

    $(".start-stop").click(function () {
        $('.jumbotron__inner-item p').removeClass('animation-true').eq($(this).index()).addClass("animation-true");
        $("button").removeClass("active").eq($(this).index()).addClass("active");
    });
    $(".pause-button").click(function () {
        $('.jumbotron__inner-item p').toggleClass('animation-true');
        $(".pause-button").toggleClass('active');
        
    });
    $("#stop").click(function () {
        $('#quest').load(document.URL + ' #quest');
    });
});

