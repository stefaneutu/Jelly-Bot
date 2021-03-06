$(document).ready(function () {
    $("button.star-btn").click(onStarBtnClick);
    $("button.detach-profile").click(onDetachClick);
});

function onStarBtnClick() {
    $(this).toggleClass("active");

    changeStar($(this).data("cid"), $(this).hasClass("active"));
}

function onDetachClick() {
    if (confirm(detachConfirmMessage($(this).data("pname")))) {
        detachProfile($(this).data("poid"), $(this).data("coid"), function () {
            location.reload();
        });
    }
}