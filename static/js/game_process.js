var data = new Array();
var request_data = {}

var total_solved = 0;
var total_rating = 0;


function get_exps(solved, rating) {
    $.ajax({
        url: "/get_exps",
        type: "POSt",
        contentType: 'application/json',
        data: JSON.stringify(request_data),
        success: function (result) {
            if (result[0] == 'О') {
                alert(result);
                return;
            }

            count = result[0].length;
            let main_part = $('#main');
            main_part.html('');
            $('#next').html('Проверить');
            for (let i = 0; i < count; i++) {
                main_part.html(
                    main_part.html() + `<p id=${i}>${result[0][i]}</p><input type=text id=${i} placeholder="Ваш ответ">`
                );
            }
            data = result;
            $('#next').off('click');
            $('#next').on('click', check);
            $('#about-game').html(`Всего решено: ${total_solved}, получено рейтинга за сессию: ${total_rating}`)

        },
        error: function (error) { alert(error) },
    })
}


function equation_check() {
    request_data.type = 'equation';
    request_data.complexity = parseInt($('#compl').val());
    get_exps();
}

function arithmetic_check() {
    request_data.type = 'arithmetic';
    request_data.complexity = parseInt($('#compl').val());
    request_data.nums_count = parseInt($('#count').val());
    request_data._brackets = parseInt($('#brackets').val());
    request_data._sum = $('#sum').is(':checked');
    request_data._sub = $('#sub').is(':checked');
    request_data._mult = $('#mult').is(':checked');
    request_data._div = $('#div').is(':checked');
    console.log(request_data);
    get_exps();
}

$('#next').on("click", function () {
    let content = '<input id="compl" placeholder="Сложность" class="form-control" aria-label="Large"></button>';
    let exptype = $('input[name="exptype"]:checked').val();
    if (exptype == undefined) {
        return;
    }
    else if (exptype == 'arithmetic') {
        content += '<input placeholder="Кол-во чисел в примере" id="count" class="form-control" aria-label="Large">';
        content += '<input placeholder="Макс. вложенность скобок" id="brackets" class="form-control" aria-label="Large">';
        content += `
        <input class="form-check-input" type="checkbox" id="sum" name="sum" value="sum">
        <label for="sum">+</label>
        <input class="form-check-input" type="checkbox" id="sub" name="sub" value="sub">
        <label for="sub">-</label>
        <input class="form-check-input" type="checkbox" id="mult" name="mult" value="mult">
        <label for="mult">*</label>
        <input class="form-check-input" type="checkbox" id="div" name="div" value="div">
        <label for="mult">/</label>
        `
        $('#next').off('click');
        $('#next').on('click', arithmetic_check);

    } else {

        $('#next').off('click');
        $('#next').on('click', equation_check);
    }

    $('#main').html(
        content
    );
})


function send_updates(points, solved) {
    $.ajax({
        url: "/game_process",
        type: "POST",
        contentType: 'application/json',
        data: JSON.stringify({
            rating: points,
            solved: solved
        }),
    })
}


function check() {
    console.log(request_data);
    let inputs = document.querySelectorAll("input");
    let rating = 0
    let solved = 0
    let i = 0
    for (let input of inputs) {
        if (input.value == data[1][i]) {
            if (request_data.type == 'equation') {
                rating += request_data.complexity;
            } else {
                rating += request_data.complexity * request_data.nums_count * 0.2;
            }
            solved++;
        }
        i++;
    }
    send_updates(rating, solved);
    total_rating += rating;
    total_solved += solved;
    get_exps();
}