document.addEventListener('DOMContentLoaded', function() {
    const modal = document.getElementById('send-modal');
    const openBtn = document.getElementById('open-send-modal');
    const closeBtns = document.querySelectorAll('.close, #cancel-send');
    const allUsersCheckbox = document.getElementById('all-users-checkbox');
    const recipientsSelect = document.getElementById('recipients-select');

    // Toggle modal
    openBtn.onclick = () => modal.style.display = 'block';
    closeBtns.forEach(btn => {
        btn.onclick = () => {
            modal.style.display = 'none';
            document.getElementById('send-form').reset();
        }
    });

    // Close modal when clicking outside
    window.onclick = (event) => {
        if (event.target === modal) {
            modal.style.display = 'none';
            document.getElementById('send-form').reset();
        }
    }

    // Handle all users checkbox
    allUsersCheckbox.addEventListener('change', function() {
        recipientsSelect.disabled = this.checked;
    });

    // Handle form submission
    document.getElementById('send-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        const formData = new FormData(e.target);

        try {
            const response = await fetch(e.target.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                }
            });

            if (response.ok) {
                modal.style.display = 'none';
                e.target.reset();
                // Optional: Refresh messages or show success message
                window.location.reload();
            } else {
                alert('Error sending message');
            }
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred');
        }
    });
});
