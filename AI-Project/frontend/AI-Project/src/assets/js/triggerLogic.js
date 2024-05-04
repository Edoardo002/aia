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
            return true
        } else {
            alert('Something went wrong. Please retry later!')
            const error = await response.json();
            console.error(error);
            return false
        }
    };
    if (file.type == "application/pdf") {
    
    }
    else if (file.type == "text/plain") {
        fileReader.readAsText(file);
    }
}

export function addNewModel() {

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
        return data
    } else {
        const error = await response.json();
        console.error(error);
        return error
    }
}