console.log("hello")
function post(url, data, fn) {
    data = JSON.stringify(data);
    var xhr = new XMLHttpRequest();
    xhr.open("POST", url, true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.onreadystatechange = function() {
        document.querySelector("#state").innerHTML = "ret:" + xhr.readyState + ',' + xhr.status;
        if (xhr.readyState == 4 && (xhr.status == 200 || xhr.status == 304)) {
            let ret = JSON.parse(xhr.responseText)
            if (ret.Err != null) {
                fn(ret);
                return;
            }
            ret = JSON.parse(ret)
            fn(ret);
        }
    };
    xhr.send(data);
    document.querySelector("#state").innerHTML = "start";
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
    document.querySelector("#ID").innerHTML = retData.retData.ID;
    document.querySelector("#code").innerHTML = retData.retData.code;
    document.querySelector("#actor").innerHTML = retData.retData.actor;
    console.log(content)
    let img = document.querySelector("#craw_img");
    let imgsrc = retData.retData.save_path;
    imgsrc = "/good_img" + imgsrc.replace(/data/, "");
    //img.src = imgsrc;

    let el = document.querySelector('#data_pool');
    let childs = el.childNodes;
    for(let i = childs .length - 1; i >= 0; i--) {
        el.removeChild(childs[i]);
    }
}

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

document.querySelector("#bMag").onclick = function() {
    let search = document.querySelector("#tSearch").value;
    if (search == "")
    {
        search = document.querySelector("#code").innerHTML;
    }

    post("/my/", {
        cmd: "get_data_by_code",
        code: search
    }, (retData)=> {
        console.log(retData)
        let div = document.querySelector("#data_pool")
        for (let mag of retData.retData) {
            let p = document.createElement("p");
            p.innerHTML = mag.size + "\t\t" + mag.name;
            div.appendChild(p);
            let content = mag.mag;
            p.onclick = function (){
                let aux = document.createElement("input");
                aux.setAttribute("value", content);
                document.body.appendChild(aux);
                aux.select();
                document.execCommand("copy");
                document.body.removeChild(aux);
            }

        }
    });
}

document.querySelector("#bPage").onclick = function() {
    console.log(document.querySelector("#tPage").value)
    post("/my/", {
        cmd: "get_data_by_id",
        id: document.querySelector("#tPage").value
    }, (retData)=> {
        console.log(retData)
        onGetData(retData)
    });
}

document.querySelector("#bLast").onclick = function() {
    post("/my/", {
        cmd: "get_last_watch_id"
    }, (retData)=> {
        console.log(retData)
        document.querySelector("#tPage").value = retData.retData;
    });
}

document.querySelector("#bReset").onclick = function() {
    post("/my/", {
        cmd: "exit_self"
    }, (retData)=> {
        console.log('exit')
    });
}
