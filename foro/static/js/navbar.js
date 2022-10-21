const navbar = document.querySelector(".navbar_container_list")
const btnOpenNavbar = document.querySelector(".bi-list")
const btnCloseNavbar = document.querySelector(".bi-x")

const openNavbar = () => {
    navbar.classList.add("navbar-open")

    btnOpenNavbar.style.display = "none"
    btnCloseNavbar.style.display = "block"
}

const closeNavbar = () => {
    navbar.classList.remove("navbar-open")

    btnOpenNavbar.style.display = "block"
    btnCloseNavbar.style.display = "none"
}

btnOpenNavbar.addEventListener("click", openNavbar)
btnCloseNavbar.addEventListener("click", closeNavbar)