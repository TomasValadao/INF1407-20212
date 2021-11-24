$(document).ready(function () {
    $(".cancel_btn").click(function () {
        $.ajax({
            url: $(this).attr("href"),
            type: 'GET'
        })
    })
})