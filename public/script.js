async function enviarmensagem(){
    const mensagem = document.getElementById("usuario").value
    const chat = document.getElementById("chat")
    if(!mensagem.trim()){
        alert("digite uma mensagem")

        return
    
    }
    chat.innerHTML += `<p class='user'> <strong> voce: </strong> ${mensagem}</p>`
    document.getElementById("usuario").value = "" 

    const response = await fetch("/chat", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({mensagem})
    })
    const data = await response.json()
    chat.innerHTML += `<p class='bot'> <strong> relampago marquinhos: </strong> ${data.resposta}</p>`
    chat.scrollTop = chat.scrollHeight

}