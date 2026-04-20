const feedbackForm = document.getElementById('feedbackForm');
const submitBtn = document.getElementById('submitBtn');
const btnText = submitBtn.querySelector('.btn-text');
const loader = submitBtn.querySelector('.loader');
const toast = document.getElementById('toast');

// API Configuration
const API_URL = window.location.hostname === '127.0.0.1' || window.location.hostname === 'localhost'
    ? 'http://127.0.0.1:8000/submit-feedback'
    : 'https://YOUR-BACKEND-URL-ON-RENDER.com/submit-feedback'; // Replace with your Render URL later

feedbackForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    // Disable button and show loader
    submitBtn.disabled = true;
    btnText.style.opacity = '0.5';
    loader.style.display = 'block';

    const formData = new FormData(feedbackForm);
    const data = {
        name: formData.get('name'),
        email: formData.get('email'),
        rating: parseInt(formData.get('rating')),
        experience: formData.get('experience')
    };

    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        });

        const result = await response.json();

        if (response.ok) {
            showToast('Feedback submitted successfully! ✨', 'success');
            feedbackForm.reset();
        } else {
            showToast(result.detail || 'Failed to submit feedback. ❌', 'error');
        }
    } catch (error) {
        console.error('Error:', error);
        showToast('Server is currently unreachable. 🔌', 'error');
    } finally {
        // Reset button state
        submitBtn.disabled = false;
        btnText.style.opacity = '1';
        loader.style.display = 'none';
    }
});

function showToast(message, type) {
    toast.textContent = message;
    toast.className = `toast ${type} show`;
    
    setTimeout(() => {
        toast.className = 'toast';
    }, 4000);
}
