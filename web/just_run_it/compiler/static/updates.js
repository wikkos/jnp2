function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

api_base= "../compiler/api/";

login = $('#username').text();

var done_count = -1;

function get_current_count(login) {
    var res;
    var xhr = new XMLHttpRequest();
    xhr.open('GET', api_base + "done_count/" + login, true);
    xhr.onload = function () {

        var json = JSON.parse(xhr.response);
        res = parseInt(json.count);
        done_count = res;
        all_sub = parseInt(json.count_all);
        console.log(res);
        //if (done_count !== -1 && res > done_count)
            alert("You have " + done_count + " submissions executed from " + all_sub);

    };
    xhr.send(null);
    return res;
}


get_current_count(login);

async function get_updates() {
    while (1) {
        get_current_count(login);
        await sleep(30000);
    }
}

get_updates();
