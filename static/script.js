document.addEventListener("DOMContentLoaded", () => {
    const textInput = document.getElementById("text-input");
    const imageInput = document.getElementById("image-input");

    textInput.addEventListener("input", () => {
        if (textInput.value.length > 300) {
            alert("⚠️ Text input too long. Consider summarizing.");
        }
    });

    imageInput.addEventListener("change", () => {
        const file = imageInput.files[0];
        if (file && !file.type.startsWith("image/")) {
            alert("🚫 Only image files are allowed.");
            imageInput.value = "";
        }
    });
});
