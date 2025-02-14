const editor = document.getElementById("editor");    
// Function to apply formatting
function applyFormatting(format) {
    const selectedText = getSelectionText();
    if (!selectedText) return;

    let formattedText;
    switch (format) {
        case "bold":
            formattedText = `**${selectedText}**`;
            break;
        case "italic":
            formattedText = `*${selectedText}*`;
            break;
        case "uppercase":
            formattedText = selectedText.toUpperCase();
            break;
        case "quote":
            formattedText = `> ${selectedText}`;
            break;
        case "ellipsis":
            formattedText = `${selectedText}...`;
            break;
        case "link":
            const url = prompt("Enter URL:", "http://");
            formattedText = `[${selectedText}](${url})`;
            break;
        case "list":
            formattedText = `- ${selectedText}`;
            break;
        case "code":
            formattedText = `\`${selectedText}\``;
            break;
        default:
            formattedText = selectedText;
    }

    replaceSelection(formattedText);
}
    
// Get selected text
function getSelectionText() {
    const start = editor.selectionStart;
    const end = editor.selectionEnd;
    return editor.value.substring(start, end);
}
    
// Replace selected text with formatted text
function replaceSelection(replacement) {
    const start = editor.selectionStart;
    const end = editor.selectionEnd;
    const text = editor.value;

    editor.value = text.substring(0, start) + replacement + text.substring(end);
    editor.setSelectionRange(start + replacement.length, start + replacement.length);
    editor.focus();
}
    
// Update word count dynamically
editor.addEventListener("input", () => {
    const words = editor.value.trim().split(/\s+/).filter(Boolean);
    document.getElementById("wordCount").innerText = words.length;
});

// Trigger hidden file input
function triggerFileInput(inputId) {
    document.getElementById(inputId).click();
}
    
// Handle file upload
function handleFileUpload(event) {
    const file = event.target.files[0];
    if (file) {
        alert(`File uploaded: ${file.name}`);
    }
}
    
// Handle image upload
function handleImageUpload(event) {
    const file = event.target.files[0];
    if (file) {
        alert(`Image uploaded: ${file.name}`);
    }
}
    
// Save content
function saveContent() {
    const content = editor.value;
    alert(`Content saved: ${content}`);
}