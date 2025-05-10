document.addEventListener('DOMContentLoaded', function () {
    const openBtn = document.getElementById('open-send-modal');
    const modal = document.getElementById('send-modal');
    const closeBtn = document.getElementById('close-send-modal');
    const allUsersCheckbox = document.getElementById('all-users-checkbox');
    const recipientsGroup = document.getElementById('recipients-group');

    // Show modal
    if (openBtn && modal) {
        openBtn.onclick = () => {
            modal.style.display = 'flex';
        };
    }

    // Hide modal
    if (closeBtn && modal) {
        closeBtn.onclick = () => {
            modal.style.display = 'none';
        };
    }
    window.onclick = (event) => {
        if (modal && event.target === modal) {
            modal.style.display = 'none';
        }
    };

    // Hide/show recipients select
    function toggleRecipients() {
        if (recipientsGroup && allUsersCheckbox) {
            recipientsGroup.style.display = allUsersCheckbox.checked ? 'none' : 'block';
        }
    }

    if (allUsersCheckbox) {
        allUsersCheckbox.addEventListener('change', toggleRecipients);
        toggleRecipients(); // Initial state
    }
});

