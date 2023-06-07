$(document).ready(function() {
    var userid = document.getElementById('userid').value;
    var socket = io.connect('/equity_scanner_test', { query: "userid=" + userid });

    socket.on(userid, function(msg) {

        totals_result = msg.number['totals']
        document.getElementById('count_live').innerHTML = "&nbsp;Total Live Trade : " + totals_result['total_trade'];
        document.getElementById('total_mtm_live').innerHTML = "&nbsp;Total MTM : " + totals_result['total_mtm'];
        document.getElementById('total_margin_live').innerHTML = "&nbsp;Total margin : " + totals_result['total_margin'];
        document.getElementById('total_ns_live').innerHTML = "&nbsp;Total N/S : " + totals_result['total_ns'];
        const myBooks = []
        for (const [key, value] of Object.entries(msg.number['data'])) {
            console.log(value);
            myBooks.push(value)
        }

        let col = [];
        for (let i = 0; i < myBooks.length; i++) {
            for (let key in myBooks[i]) {
                if (col.indexOf(key) === -1) {
                    col.push(key);
                }
            }
        }

        // Create a table.
        const table = document.createElement("table");

        // Create table header row using the extracted headers above.
        let tr = table.insertRow(-1); // table row.
        for (let i = 0; i < col.length; i++) {
            let th = document.createElement("th"); // table header.
            th.innerHTML = col[i];
            tr.appendChild(th);
        }

        // add json data to the table as rows.
        for (let i = 0; i < myBooks.length; i++) {

            tr = table.insertRow(-1);

            for (let j = 0; j < col.length; j++) {
                let tabCell = tr.insertCell(-1);
                tabCell.innerHTML = myBooks[i][col[j]];
                $(tr).find('td:eq(1)').css('background', '#e7e3d5');
                $(tr).find('td:eq(2)').css('background', '#e7e3d5');
                $(tr).find('td:eq(3)').css('background', '#e7e3d5');
                $(tr).css('background', '#fbf5cd');
                if (parseFloat(myBooks[i]['Mtm']) > 0) {
                    $(tr).find('td:eq(5)').css('background', '#c6efce');
                    $(tr).find('td:eq(0)').css('background', '#c6efce');
                    $(tr).find('td:eq(5)').css('color', 'green');
                } else if (parseFloat(myBooks[i]['Mtm']) < 0) {
                    $(tr).find('td:eq(5)').css('background', '#ffc7ce');
                    $(tr).find('td:eq(0)').css('background', '#ffc7ce');
                    $(tr).find('td:eq(5)').css('color', 'red');
                } else {
                    $(tr).find('td').not(':eq(2)').css('color', 'black');
                }

                if (parseFloat(myBooks[i]['Nifty vs Stock']) > 0) {
                    $(tr).find('td:eq(11)').css('background', '#c6efce');
                    $(tr).find('td:eq(11)').css('color', 'green');
                } else if (parseFloat(myBooks[i]['Nifty vs Stock']) < 0) {
                    $(tr).find('td:eq(11)').css('background', '#ffc7ce');
                    $(tr).find('td:eq(11)').css('color', 'red');
                } else {
                    $(tr).find('td').not(':eq(2)').css('color', 'black');
                }
            }
        }
        $('#log2').html(table);

    });

});




$(document).ready(function() {
    var userid = document.getElementById('userid').value;
    $.ajax({
        type: 'GET',
        url: '/get_equity_acrvhive',
        data: { userid },
        success: function(data, textStatus, jqXHR) {
            console.log('success : ' + data);
            console.log('success : ' + typeof data);

            totals_result = JSON.parse(data)['totals']
            document.getElementById('count').innerHTML = "&nbsp;Total Trade Completed : " + totals_result['total_trade'];
            document.getElementById('total_bp').innerHTML = "&nbsp;Total B/P : " + totals_result['total_bp'];
            document.getElementById('total_ns').innerHTML = "&nbsp;Total N/S : " + totals_result['total_ns'];
            const obj = JSON.parse(data)['data'];
            // console.log(obj['data']);
            // console.log("Received number" + Object.entries(obj));

            const myBooks = []
            for (const [key, value] of Object.entries(obj)) {
                // console.log("new data",value)
                myBooks.push(value)
            }

            let col = [];
            for (let i = 0; i < myBooks.length; i++) {
                for (let key in myBooks[i]) {
                    if (col.indexOf(key) === -1) {
                        col.push(key);
                    }
                }
            }

            // Create a table.
            const table = document.createElement("table");

            // Create table header row using the extracted headers above.
            let tr = table.insertRow(-1); // table row.

            console.log(col.length)
            for (let i = 0; i < col.length; i++) {
                let th = document.createElement("th"); // table header.
                th.innerHTML = col[i];
                tr.appendChild(th);
            }

            // add json data to the table as rows.
            for (let i = 0; i < myBooks.length; i++) {

                tr = table.insertRow(-1);

                for (let j = 0; j < col.length; j++) {
                    let tabCell = tr.insertCell(-1);
                    // console.log(myBooks[i][col[j]]);
                    tabCell.innerHTML = myBooks[i][col[j]];
                    $(tr).find('td:eq(1)').css('background', '#e7e3d5');
                    $(tr).find('td:eq(2)').css('background', '#e7e3d5');
                    $(tr).find('td:eq(3)').css('background', '#e7e3d5');
                    $(tr).css('background', '#fbf5cd');
                    if (Number(myBooks[i]['Booked Profit']) > 0) {
                        $(tr).find('td:eq(6)').css('background', '#c6efce');
                        $(tr).find('td:eq(0)').css('background', '#c6efce');
                        $(tr).find('td:eq(6)').css('color', 'green');
                    } else if (Number(myBooks[i]['Booked Profit']) < 0) {
                        $(tr).find('td:eq(6)').css('background', '#ffc7ce');
                        $(tr).find('td:eq(0)').css('background', '#ffc7ce');
                        $(tr).find('td:eq(6)').css('color', 'red');
                    } else {
                        $(tr).find('td').not(':eq(2)').css('color', 'black');
                    }

                    if (Number(myBooks[i]['Nifty vs Stock']) > 0) {
                        $(tr).find('td:eq(10)').css('background', '#c6efce');
                        $(tr).find('td:eq(10)').css('color', 'green');
                    } else if (Number(myBooks[i]['Nifty vs Stock']) < 0) {
                        $(tr).find('td:eq(10)').css('background', '#ffc7ce');
                        $(tr).find('td:eq(10)').css('color', 'red');
                    } else {
                        $(tr).find('td').not(':eq(2)').css('color', 'black');
                    }

                }
            }



            // cell3.innerHTML = "0";
            // console.log(table)
            $('#log3').html(table);


        },
        error: function(data, jqXHR, textStatus, errorThrown, responseText) {
            console.log("Error occurred, " + errorThrown + " MMM" + responseText);

        }
    });
    //receive details from server


});