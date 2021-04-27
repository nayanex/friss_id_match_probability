$(document).ready(function () {

    $('#probabilityButton').on('click', function () {

        var first_name1 = $('#first_name1').val();
        var last_name1 = $('#last_name1').val();
        var birth_date1 = $('#birth_date1').val();
        var bsn1 = $('#bsn1').val();

        var first_name2 = $('#first_name2').val();
        var last_name2 = $('#last_name2').val();
        var birth_date2 = $('#birth_date2').val();
        var bsn2 = $('#bsn2').val();

        req = $.ajax({
            url: '/probability',
            type: 'POST',
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify({
                persons: [
                    {
                        first_name: first_name1,
                        last_name: last_name1,
                        birth_date: birth_date1,
                        bsn: bsn1
                    },
                    {
                        first_name: first_name2,
                        last_name: last_name2,
                        birth_date: birth_date2,
                        bsn: bsn2
                    }
                ]
            })

        });

        req.done(function (data) {
            $('#probability').text(data.probability);

        });
    });
});