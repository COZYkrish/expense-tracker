const root = document.documentElement;
const toggle = document.getElementById("themeToggle");

// Apply theme on page load
const savedTheme = localStorage.getItem("theme") || "light";
root.setAttribute("data-theme", savedTheme);

// Toggle theme
if (toggle) {
    toggle.addEventListener("click", () => {
        const current = root.getAttribute("data-theme");
        const next = current === "dark" ? "light" : "dark";

        root.setAttribute("data-theme", next);
        localStorage.setItem("theme", next);
    });
}
function showToast(message, type = "success") {
    const toast = document.getElementById("toast");
    if (!toast) return;

    toast.textContent = message;
    toast.className = "";
    toast.classList.add("show", type);

    setTimeout(() => {
        toast.classList.remove("show");
    }, 3000);
}
