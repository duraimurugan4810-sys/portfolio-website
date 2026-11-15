
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
    
const response = await fetch("https://api.web3forms.com/submit", {
    method: "POST",
    headers: {
        "Content-Type": "application/json",
        "Accept": "application/json"
    },
    body: JSON.stringify({
        access_key: "ead42cfa-d901-434e-8153-fa2acbf91337",
        name: formData.name,
        email: formData.email,
        message: formData.message,
        subject: "New Portfolio Contact Message",
        from_name: "Durai Murugan Portfolio"
    })
});

const result = await response.json();

if (!response.ok || !result.success) {
    throw new Error(result.message || "Message could not be sent.");
}

statusMessage.textContent = "Message sent successfully!";
form.reset();

} catch (error) {
    statusMessage.textContent =
        error.message || "Unable to send message.";
    console.error(error);

} finally {
    button.disabled = false;
    button.textContent = "Send Message";
}
});
