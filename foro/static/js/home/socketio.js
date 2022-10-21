const btnSendMessage = document.getElementById("sendbutton")
const inputMessage = document.querySelector(".inputMessage")
const listMessages = document.querySelector(".chat_messages")

const socket = io()

socket.on('message', function(msg){
    listMessages.innerHTML += `<li class="chat_message"><p>${msg}</p></li>`
})

const sendMessage = (e) => {
    e.preventDefault()

    let inputValue = inputMessage.value
    socket.send(inputValue)

    inputValue = ""

}

btnSendMessage.addEventListener("click", sendMessage)


