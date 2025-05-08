document.addEventListener('DOMContentLoaded', function() {
    const openBtn = document.getElementById('open-send-modal');
    const modal = document.getElementById('send-modal');
    const closeBtn = document.getElementById('close-send-modal');
    const allUsersCheckbox = document.getElementById('all-users-checkbox');
    const recipientsGroup = document.getElementById('recipients-group');
    const select = document.getElementById('staySelected');
    const selectedList = document.getElementById('selected-list');

    // Show modal
    if (openBtn && modal) {
        openBtn.onclick = () => { modal.style.display = 'flex'; };
    }

    // Hide modal
    if (closeBtn && modal) {
        closeBtn.onclick = () => { modal.style.display = 'none'; };
    }
    window.onclick = (event) => {
        if (modal && event.target === modal) { modal.style.display = 'none'; }
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

   // Toggle selection on click (no Ctrl needed)
    select.addEventListener('mousedown', function(e) {
        if (e.target.tagName === 'OPTION') {
            e.preventDefault();
            e.target.selected = !e.target.selected;
            // Trigger change event so the list updates
            const event = new Event('change', { bubbles: true });
            select.dispatchEvent(event);
        }
    });

    // Show selected items below
    function updateSelectedList() {
        selectedList.innerHTML = '';
        Array.from(select.selectedOptions).forEach(opt => {
            const badge = document.createElement('span');
            badge.textContent = opt.text;
            badge.style = 'background: #c8e6c9; color: #256029; padding: 3px 8px; margin: 2px; border-radius: 4px; display: inline-block;';
            selectedList.appendChild(badge);
        });
    }
    select.addEventListener('change', updateSelectedList);
    updateSelectedList(); // Initial call
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
