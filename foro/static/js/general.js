try{
    const quitAlert = document.querySelector(".quit-alert")

    const removeAlert = (e) => {

        e.currentTarget.parentElement.remove()

    }
    
    quitAlert.addEventListener("click", removeAlert)
}catch(e){

}