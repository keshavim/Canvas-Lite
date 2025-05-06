document.addEventListener('DOMContentLoaded', function() {
    const openBtn = document.getElementById('open-send-modal');
    const modal = document.getElementById('send-modal');
    const closeBtn = document.getElementById('close-send-modal');
    const allUsersCheckbox = document.getElementById('all-users-checkbox');
    const recipientsGroup = document.getElementById('recipients-group');

    // Show modal
    openBtn.onclick = () => { modal.style.display = 'flex'; };

    // Hide modal
    closeBtn.onclick = () => { modal.style.display = 'none'; };
    window.onclick = (event) => {
        if (event.target === modal) { modal.style.display = 'none'; }
    };

    // Hide/show recipients select
    function toggleRecipients() {
        recipientsGroup.style.display = allUsersCheckbox.checked ? 'none' : 'block';
    }
    allUsersCheckbox.addEventListener('change', toggleRecipients);
    toggleRecipients(); // Initial state
});

document.getElementById('read-toggle').addEventListener('click', function() {
    if (this.textContent === 'Unread') {
        this.textContent = 'Read';
        this.classList.remove('btn-danger');
        this.classList.add('btn-success');
    } else {
        this.textContent = 'Unread';
        this.classList.remove('btn-success');
        this.classList.add('btn-danger');
    }
});