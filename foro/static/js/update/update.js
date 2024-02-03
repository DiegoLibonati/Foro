const elementsOfProfilePhoto = document.querySelectorAll(".pfphoto");
const elementsOfProfileBanner = document.querySelectorAll(".pfbanner");

const checkboxProfilePhoto = document.getElementById("removeprofilephoto");
const checkboxProfileBanner = document.getElementById("removeprofilebanner");

const profilePhoto = document.getElementById("profile_photo");
const profileBanner = document.getElementById("profile_banner");

const arrayPhoto = Array.from(elementsOfProfilePhoto);
const arrayBanner = Array.from(elementsOfProfileBanner);

checkboxProfilePhoto.addEventListener("change", (e) => {
  arrayPhoto.map((element) => {
    if (e.target.checked) {
      element.style.display = "None";
      profilePhoto.value = null;
    } else {
      element.style.display = "Block";
    }
  });
});

checkboxProfileBanner.addEventListener("change", (e) => {
  arrayBanner.map((element) => {
    if (e.target.checked) {
      element.style.display = "None";
      profileBanner.value = null;
    } else {
      element.style.display = "Block";
    }
  });
});
