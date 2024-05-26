export function addNewContext(user_id) {
    var files = document.getElementById("userFiles").files;
    var name = document.getElementById("userFiles").value;
    name = name.replace(/.*[\/\\]/, '');

    var file = files[0];
    var fileReader = new FileReader();
    var content;
    fileReader.onload = async function(fileReadEvent) {
        content=fileReadEvent.target.result;
        const response = await fetch('http://127.0.0.1:8000/chatbot/loadContext', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ user_id:user_id, context_name:name, context:content })
            });
        if (response.ok) {
            window.dialog.close();
            const data = await response.json();
            console.log(data);
            return data;
        } else {
            alert('Something went wrong. Please retry later!')
            const error = await response.json();
            console.error(error);
            return error;
        }
    };
    if (file.type == "application/pdf") {
    
    }
    else if (file.type == "text/plain") {
        fileReader.readAsText(file);
    }
}

export async function addNewModel(user_id) {

    const context_name = document.querySelector('input[name="context"]:checked').value;
    const model = document.querySelector('input[name="model"]:checked').value;
    const response = await fetch('http://127.0.0.1:8000/chatbot/addModel', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ user_id:user_id, context_name:context_name, model:model })
            });
        if (response.ok) {
            window.location.reload();
            const data = await response.json();
            console.log(data);
            return data;
        } else {
            alert('Something went wrong. Please retry later!')
            const error = await response.json();
            console.error(error);
            return error;
        }

}

export async function getContexts(user_id) {
    const response = await fetch('http://127.0.0.1:8000/chatbot/getContexts', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ user_id:user_id })
        });
    if (response.ok) {
        const data = await response.json();
        console.log(data);
        return data;
    } else {
        const error = await response.json();
        console.error(error);
        return error;
    }
}

export async function getModels(user_id) {
    const response = await fetch('http://127.0.0.1:8000/chatbot/getModels', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ user_id:user_id })
        });
    if (response.ok) {
        const data = await response.text();
        console.log(data);
        return data;
    } else {
        const error = await response.json();
        console.error(error);
        return error;
    }
}

export async function queryBot(user_id) {
    var list = document.getElementById("chatList");
    var el = document.createElement("li");
    const query = document.getElementById("queryBot").value;
    el.appendChild(document.createTextNode(query));
    list.appendChild(el);
    list.scrollTop = list.scrollHeight;
    document.getElementById("sendbtn").disabled=true;
    document.getElementById("queryBot").value="";
    const rag_model = document.getElementById("chatName").innerHTML;
    const response = await fetch('http://127.0.0.1:8000/chatbot/queryChatbot', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ user_id:user_id, rag_model:rag_model, query:query})
        });
    if (response.ok) {
        const data = await response.text();
        console.log(data);
        var result = data.substring(1, data.length-1).replace(/(\r\n|\n|\r)/gm,"<br>");
        var _el = document.createElement("li");
        _el.appendChild(document.createTextNode(result));
        list.appendChild(_el);
        list.scrollTop = list.scrollHeight;
        document.getElementById("sendbtn").disabled=false;
        return;
    } else {
        const error = await response.body;
        console.error(error);
        return error;
    }
}