console.log("hello")
function post(url, data, fn) {
    data = JSON.stringify(data);
    var xhr = new XMLHttpRequest();
    xhr.open("POST", url, true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.onreadystatechange = function() {
        if (xhr.readyState == 4 && (xhr.status == 200 || xhr.status == 304)) {
            fn(JSON.parse(JSON.parse(xhr.responseText)));
        }
    };
    xhr.send(data);
}

post("/my/", {
    cmd: "get_data_by_id",
    id: 1
}, (retData)=> {
    console.log(retData)
    let img = document.querySelector("#craw_img");
    console.log(img);
    img.src = "/good_img/48.png";
    console.log(img);
});