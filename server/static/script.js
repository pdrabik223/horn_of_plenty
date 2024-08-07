
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


function delete_wifi(id) {
    $.get('/remove_wifi?name=' + id, function (data) {

        if (data.length > 0) {
            var table = document.getElementById("wifi_list");

            for (let i = 0; i < data.length; i++) {
                table.deleteRow(data[i]);
            }

        }
    });

}
setInterval(log_updater, 1000);
function log_updater() {

    var table = document.getElementById("logs");
    url = '/get_logs?count=0'
    if (table.rows.length != NaN){
    
        url = '/get_logs?count='+String(table.rows.length - 2)
    }
    
    $.get(url, function (data) {        
        for (let i = 0; i < data.length; i++) {
            
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

