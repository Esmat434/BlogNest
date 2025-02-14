// this is for notification icon
document.addEventListener('DOMContentLoaded', function() {
    // گرفتن المان با id
    const notificationIcon = document.getElementById('notification-icon');
    
    // گرفتن URL از ویژگی data-url
    const url = notificationIcon.getAttribute('data-url');
    
    // اضافه کردن event listener برای کلیک
    notificationIcon.addEventListener('click', function() {
        // هدایت به URL
        window.location.href = url;
    });
});

// this is for create post button
document.addEventListener('DOMContentLoaded', function() {
    // گرفتن المان با id
    const notificationIcon = document.getElementById('create-post-button');
    
    // گرفتن URL از ویژگی data-url
    const url = notificationIcon.getAttribute('data-url');
    
    // اضافه کردن event listener برای کلیک
    notificationIcon.addEventListener('click', function() {
        // هدایت به URL
        window.location.href = url;
    });
});

// voice searcher
document.addEventListener("DOMContentLoaded", () => {
    const voiceButton = document.getElementById("voice-button");
    const searchInput = document.querySelector("input[name='search-input']");
    const searchForm = document.querySelector(".search-box");

    if (!navigator.mediaDevices || !window.MediaRecorder) {
        alert("Your browser does not support audio recording.");
        return;
    }

    voiceButton.addEventListener("click", async () => {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            const mediaRecorder = new MediaRecorder(stream);
            const audioChunks = [];

            mediaRecorder.start();

            // جمع‌آوری داده‌های صوتی
            mediaRecorder.addEventListener("dataavailable", (event) => {
                audioChunks.push(event.data);
            });

            mediaRecorder.addEventListener("stop", async () => {
                const audioBlob = new Blob(audioChunks, { type: "audio/wav" });

                // ارسال صدا برای پردازش و تبدیل به متن
                const text = await processAudioToText(audioBlob);

                if (text) {
                    // درج متن در ورودی جستجو و ارسال فرم
                    searchInput.value = text;
                    searchForm.submit();
                } else {
                    alert("Unable to process the audio. Please try again.");
                }
            });

            // توقف ضبط پس از 5 ثانیه
            setTimeout(() => {
                mediaRecorder.stop();
            }, 5000);
        } catch (err) {
            console.error("Error accessing audio device:", err);
            alert("Failed to access microphone.");
        }
    });

    // ارسال صدا برای تبدیل به متن
    const processAudioToText = async (audioBlob) => {
        const formData = new FormData();
        formData.append("audio", audioBlob);

        try {
            const response = await fetch("{% url 'process_audio_to_text' %}", {
                method: "POST",
                body: formData,
                headers: {
                    "X-CSRFToken": "{{ csrf_token }}",
                },
            });

            if (response.ok) {
                const data = await response.json();
                return data.text; // متن تبدیل‌شده
            } else {
                console.error("Failed to process audio:", response.status);
                return null;
            }
        } catch (error) {
            console.error("Error processing audio:", error);
            return null;
        }
    };
});
