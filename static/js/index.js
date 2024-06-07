var count = 0;
var data = new Array();

$.ajax({
    url: "/",
    type: "POST",
    contentType: 'application/json',
    data: JSON.stringify({}),
    success: function (result) {
        count = result[0].length;
        let main_part = $('#main');
        for (let i = 0; i < count; i++) {
            main_part.html(
                main_part.html() + `<p id=${i}>${result[0][i]}</p><input id=${i} placeholder="Ваш ответ">`
            )
        }
        data = result;

    },
    error: function () { return 'error' },
})

$('#check').on("click", function () {
    let inputs = document.querySelectorAll("input");
    let point = 0;
    let i = 0;
    for (let input of inputs) {
        console.log(input.value)
        console.log(data[1][i])
        if (input.value == data[1][i]) {
            point++;
            alert(`${point}`);
        }
        i++;
    }
})

