
function delete_contact(id) {
    $.get('/remove_contact?phoneNumber=' + id, function (data) {

        if (data.length > 0) {
            var table = document.getElementById("contact_list");

            for (let i = 0; i < data.length; i++) {
                table.deleteRow(data[i]);
            }

        }
    });

}
setInterval(log_updater, 1000);
function log_updater() {

    $.get('/get_logs', function (data) {        
        var table = document.getElementById("logs");
        console.log(data)
        for (let i = table.rows.length - 2; i < data.length; i++) {
            
            var row = table.insertRow(1);

            var cell1 = row.insertCell(0);
            var cell2 = row.insertCell(1);
            var cell3 = row.insertCell(2);
            var cell4 = row.insertCell(3);
            var cell5 = row.insertCell(4);

            cell1.innerHTML = table.rows.length - 3;
            cell2.innerHTML = data[i]["level"];
            cell3.innerHTML = data[i]["date"];
            cell4.innerHTML = data[i]["time"];
            cell5.innerHTML = data[i]["message"];
        }

    });
};

