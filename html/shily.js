console.log("hello")
function post(url, data, fn) {
    data = JSON.stringify(data);
    var xhr = new XMLHttpRequest();
    xhr.open("POST", url, true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.onreadystatechange = function() {
        if (xhr.readyState == 4 && (xhr.status == 200 || xhr.status == 304)) {
            let ret = JSON.parse(xhr.responseText)
            if (ret.Err != null) {
                fn(ret);
                return;
            }
            fn(JSON.parse(ret));
        }
    };
    xhr.send(data);
}

function getIndex() {
    let index = localStorage.getItem('index')
    if (index != null) {
        return parseInt(index);
    }

    return 1;
}

function setIndex(index) {
    localStorage.setItem('index', index);
}

function formatRetData(retData) {
    retData = retData.retData
    return "ID:" + retData['ID'] + "\n"
        // + "code:" + retData['code'] + "\n"
        // + "actor:" + retData['actor'] + "\n"
}

function onGetData(retData) {
    if (retData.Err != 0) {
        return;
    }
    setIndex(parseInt(retData.retData.ID));
    let content = document.querySelector("#content")
    content.innerHTML = formatRetData(retData)
    console.log(content)
    let img = document.querySelector("#craw_img");
    console.log(retData.retData.save_path);
    let imgsrc = retData.retData.save_path;
    imgsrc.replace(/data\//, "");
    img.src = "/good_img/" + imgsrc;
    console.log(img);
}

post("/my/", {
    cmd: "get_data_by_id",
    id: getIndex()
}, (retData)=> {
    console.log(retData)
    onGetData(retData)
});

document.querySelector("#bPrev").onclick = function() {
    post("/my/", {
        cmd: "get_data_by_id",
        id: getIndex() - 1
    }, (retData)=> {
        console.log(retData)
        onGetData(retData)
    });
}

document.querySelector("#bNext").onclick = function() {
    post("/my/", {
        cmd: "get_data_by_id",
        id: getIndex() + 1
    }, (retData)=> {
        console.log(retData)
        onGetData(retData)
    });
}