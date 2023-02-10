



// Menu


const dropdownMenu = document.querySelector(".dropdown-menu");
const dropdownButton = document.querySelector(".dropdown-button");

if (dropdownButton) {
  dropdownButton.addEventListener("click", () => {
    dropdownMenu.classList.toggle("show");
  });
}

// Upload Image
const photoInput = document.querySelector("#avatar");
const photoPreview = document.querySelector("#preview-avatar");
if (photoInput)
  photoInput.onchange = () => {
    const [file] = photoInput.files;
    if (file) {
      photoPreview.src = URL.createObjectURL(file);
    }
  };

// Scroll to Bottom
const conversationThread = document.querySelector(".room__box");
if (conversationThread) conversationThread.scrollTop = conversationThread.scrollHeight;


// // notification
// const notification = document.querySelector(".notification");
// const cancelDelete = document.querySelector("#cancel-delete");
// const showNotificationBtns = document.querySelectorAll("#show-notification")
// cancelDelete.addEventListener("click", () => {
//   console.log('clicked')
//   notification.classList.add("hidden");
// })

// showNotificationBtns.forEach(btn => {
//   btn.addEventListener("click", () => { 
//     notification.classList.remove("hidden");
//   })
// })


