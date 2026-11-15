
const form = document.getElementById("contact-form");
const statusMessage = document.getElementById("form-status");

form.addEventListener("submit", async function (event) {
    event.preventDefault();

    const button = form.querySelector("button");
    button.disabled = true;
    button.textContent = "Sending...";

    const formData = {
        name: form.elements["name"].value.trim(),
        email: form.elements["email"].value.trim(),
        message: form.elements["message"].value.trim()
    };

    try {
        const response = await fetch("http://127.0.0.1:5000/api/contact", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(formData)
        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.error || "Message could not be sent.");
        }

        statusMessage.textContent = "Message sent successfully!";
        form.reset();

    } catch (error) {
        statusMessage.textContent =
            "Unable to send message. Please check whether the Python backend is running.";
        console.error(error);

    } finally {
        button.disabled = false;
        button.textContent = "Send Message";
    }
});
