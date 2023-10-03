document.addEventListener("DOMContentLoaded", function () {
    const editButtons = document.querySelectorAll(".edit-button");
    const posts = document.querySelectorAll(".post");
    
    editButtons.forEach((editButton, index) => {
        editButton.addEventListener("click", function () {
            const post = editButton.closest(".post");
            const postContent = post.querySelector("p"); // Find the <p> element within the post
            const form = post.querySelector("form");
            const saveButton = post.querySelector(".save-button")
            postContent.style.display = "none"; // Hide the <p> element
            form.style.display ="block";
            editButton.style.display ="none";
            saveButton.style.display ="block";

        });
    });
});