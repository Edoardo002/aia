import * as pdfjs from 'pdfjs-dist';
pdfjs.GlobalWorkerOptions.workerSrc = import.meta.url + 'pdfjs-dist/build/pdf.worker.mjs';

export function addNewContext(user_id) {
    var files = document.getElementById("userFiles").files;
    var name = document.getElementById("userFiles").value;
    name = name.replace(/.*[\/\\]/, '');

    if (files.length > 1 && files[0].type!=files[1].type) {
        alert('Multiple files must be of the same type!');
        return;
    }

    let readers= [];

    if (files[0].type == "application/pdf") {
        var pdff = new Pdf2TextClass();
        for(let i = 0;i < files.length;i++) {
            readers.push(readFileAsDataURL(files[i]));
        }
        Promise.all(readers).then(async (values) => {
            var content = '';
            let ind = 0;
            values.forEach((element) => {
                pdff.pdfToText(element, null, async (cont) => {
                    content = content.concat(cont);
                    content.replace(/[^a-zA-Z0-9&\/\\#,+()$~%.'":*?<>{}]/g, '');
                    ind+=1;
                    if (ind==values.length) {
                        const response = await fetch('http://127.0.0.1:8000/chatbot/loadContext', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json'
                            },
                            body: JSON.stringify({ user_id:user_id, context_name:name, context:content })
                        });
                        if (response.ok) {
                            window.dialog.close();
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
                });
            });
        });
    }
    else if (files[0].type == "text/plain") {
        for(let i = 0;i < files.length;i++) {
            readers.push(readFileAsText(files[i]));
        }
        Promise.all(readers).then(async (values) => {
            var content = '';
            values.forEach((element) => {
                content += element;
            });
            content.replace(/[^a-zA-Z0-9&\/\\#,+()$~%.'":*?<>{}]/g, '');
            const response = await fetch('http://127.0.0.1:8000/chatbot/loadContext', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ user_id:user_id, context_name:name, context:content })
            });
            if (response.ok) {
                window.dialog.close();
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
        });
    }
}

function readFileAsText(file){
    return new Promise(function(resolve,reject){
        let fr = new FileReader();

        fr.onload = function(){
            resolve(fr.result);
        };

        fr.onerror = function(){
            reject(fr);
        };

        fr.readAsText(file);
    });
}

function readFileAsDataURL(file){
    return new Promise(function(resolve,reject){
        let fr = new FileReader();

        fr.onload = function(){
            resolve(fr.result);
        };

        fr.onerror = function(){
            reject(fr);
        };

        fr.readAsDataURL(file);
    });
}

function Pdf2TextClass() {
    var self = this;
    this.complete = 0;

    this.pdfToText = function (data, callbackPageDone, callbackAllDone) {
        console.assert(data instanceof ArrayBuffer || typeof data == 'string');
        var loadingTask = pdfjsLib.getDocument(data);
        loadingTask.promise.then(function (pdf) {


            var total = pdf._pdfInfo.numPages;
            //callbackPageDone( 0, total );        
            var layers = {};
            for (var i = 1; i <= total; i++) {
                pdf.getPage(i).then(function (page) {
                    var n = page.pageNumber;
                    page.getTextContent().then(function (textContent) {

                        //console.log(textContent.items[0]);0
                        if (null != textContent.items) {
                            var page_text = "";
                            var last_block = null;
                            for (var k = 0; k < textContent.items.length; k++) {
                                var block = textContent.items[k];
                                if (last_block != null && last_block.str[last_block.str.length - 1] != ' ') {
                                    if (block.x < last_block.x)
                                        page_text += "\r\n";
                                    else if (last_block.y != block.y && (last_block.str.match(/^(\s?[a-zA-Z])$|^(.+\s[a-zA-Z])$/) == null))
                                        page_text += ' ';
                                }
                                page_text += block.str;
                                last_block = block;
                            }

                            textContent != null && console.log("page " + n + " finished."); //" content: \n" + page_text);
                            layers[n] = page_text + "\n\n";
                        }
                        ++self.complete;
                        //callbackPageDone( self.complete, total );
                        if (self.complete == total) {
                            window.setTimeout(function () {
                                var full_text = "";
                                var num_pages = Object.keys(layers).length;
                                for (var j = 1; j <= num_pages; j++)
                                    full_text += layers[j];
                                callbackAllDone(full_text);
                            }, 1000);
                        }
                    }); // end  of page.getTextContent().then
                }); // end of page.then
            } // of for
        });
    }; // end of pdfToText()
}; // end of class

export async function addSharepointContext(user_id) {

    const sp_link = document.getElementById('contextURL').value;
    const client_id = document.getElementById('clientId').value;
    const client_secret = document.getElementById('clientSecret').value;
    const document_library_id = document.getElementById('documentLib').value;
    const folder_path = document.getElementById('path').value;
    const response = await fetch('http://127.0.0.1:8000/chatbot/loadSharepoint', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ user_id:user_id, client_id:client_id, client_secret:client_secret, sp_link:sp_link, document_library_id:document_library_id, folder_path:folder_path })
            });
        if (response.ok) {
            window.dialog.close();
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
            window.dialog.close();
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