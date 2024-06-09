var count = 0;
var data = new Array();
var point = 0;

function update() {
    $.ajax({
        url: "/game_process",
        type: "POST",
        contentType: 'application/json',
        data: JSON.stringify({}),
        success: function (result) {
            count = result[0].length;
            let main_part = $('#main');
            main_part.html('');
            for (let i = 0; i < count; i++) {
                main_part.html(
                    main_part.html() + `<p id=${i}>${result[0][i]}</p><input type=text id=${i} placeholder="Ваш ответ">`
                )
            }
            main_part.html(
                main_part.html() + `<br> <button id=check>Проверить</button>`
                )
            data = result;

        },
        error: function () { return 'error' },
    })
}

update();

function update_after_check() {
    $.ajax({
        url: "/game_process",
        type: "POST",
        contentType: 'application/json',
        data: JSON.stringify({}),
        success: function (result) {
            count = result[0].length;
            let main_part = $('#main');
            main_part.html(`<p>${point}</p>`);
            data = result;

        },
        error: function () { return 'error' },
    })
}


$('#check').prop('disabled', true)

$(document).on('input', 'input[type="text"]', function() {
    $('#check').prop('disabled', false);
});

$('#check').on("click", function () {
    let inputs = document.querySelectorAll("input");
    let i = 0;
    for (let input of inputs) {
        console.log(input.value)
        console.log(data[1][i])
        if (input.value == data[1][i]) {
            point++;
            update_after_check();
        }
        i++;
    }
})