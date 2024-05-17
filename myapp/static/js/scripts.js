document.addEventListener("DOMContentLoaded", function() {
    const openModalButton = document.getElementById("open-modal");
    const modal = document.getElementById("modal");
    const closeModalButton = document.getElementById("close-modal");

    openModalButton.addEventListener("click", function() {
        modal.style.display = "block";
    });

    closeModalButton.addEventListener("click", function() {
        modal.style.display = "none";
    });

    window.addEventListener("click", function(event) {
        if (event.target === modal) {
            modal.style.display = "none";
        }
    });
});


