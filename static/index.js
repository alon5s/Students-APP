const input = document.getElementById("search");
input.addEventListener('input', () => {
    var keyword = input.value.toLowerCase();

    var table = document.getElementById("students_table");
    var rows = table.getElementsByTagName("tr");
    for (var i = 0; i < rows.length; i++) {
        var row = rows[i];
        var name = row.getElementsByTagName("td")[0];
        var email = row.getElementsByTagName("td")[1];
        if (name && email) {
            var text0 = name.textContent.toLowerCase();
            var text1 = email.textContent.toLowerCase();
            if (text0.indexOf(keyword) > -1 || text1.indexOf(keyword) > -1) {
                row.style.display = "";
            } else {
                row.style.display = "none";
            }
        }
    }
})