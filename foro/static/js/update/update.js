const elementsOfProfilePhoto = document.querySelectorAll(".pfphoto")
const elementsOfProfileBanner = document.querySelectorAll(".pfbanner")

const checkboxProfilePhoto = document.getElementById("removeprofilephoto");
const checkboxProfileBanner = document.getElementById("removeprofilebanner");

const profilePhoto = document.getElementById("profile_photo")
const profileBanner = document.getElementById("profile_banner")

const arrayPhoto =  Array.from(elementsOfProfilePhoto)
const arrayBanner =  Array.from(elementsOfProfileBanner)   



checkboxProfilePhoto.addEventListener("change", (e) => {

    if (e.target.checked) {
        arrayPhoto.map(element => {
            element.style.display = "None"
            profilePhoto.value = null
        })
    } else {
        arrayPhoto.map(element => {
            element.style.display = "Block"
        })
    }

})


checkboxProfileBanner.addEventListener("change", (e) => {

    if (e.target.checked) {
        arrayBanner.map(element => {
            element.style.display = "None"
            profileBanner.value = null
        })
    } else {
        arrayBanner.map(element => {
            element.style.display = "Block"
        })
    }
    

})


