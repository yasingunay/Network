function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

function submitHandler(id, textareaValue) {
    fetch(`/edit/${id}`, {
        method: "POST",
        headers: { "Content-type": "application/json", "X-CSRFToken": getCookie("csrftoken") },
        body: JSON.stringify({
            content: textareaValue,
        })
    })
        .then(response => response.json())
        .then(data => {
            console.log(data);
        });
}

document.addEventListener("DOMContentLoaded", function () {
    const editButtons = document.querySelectorAll(".edit-button");

    editButtons.forEach((editButton, index) => {
        editButton.addEventListener("click", function () {
            const post = editButton.closest(".post");
            const postContent = post.querySelector("p"); // Find the <p> element within the post
            const textarea = post.querySelector("textarea");
            const saveButton = post.querySelector(".save-button");

            postContent.style.display = "none"; // Hide the <p> element
            textarea.style.display = "block";
            editButton.style.display = "none";
            saveButton.style.display = "block";

            saveButton.addEventListener("click", function () {
                const textareaValue = textarea.value;
                const PostId = post.getAttribute('data-post-id');

                submitHandler(PostId, textareaValue);

                postContent.innerHTML = textareaValue;
                postContent.style.display = "block";
                textarea.style.display = "none";
                editButton.style.display = "block";
                saveButton.style.display = "none";
            });
        });
    });
});
