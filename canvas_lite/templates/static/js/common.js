document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('select[multiple]').forEach(function(select) {
        // Use the select's id to find the right badge container
        var selectedList = document.getElementById(select.id + '-selected-list');
        console.log(select.id + '-selected-list');
        if (!selectedList) return;

        // Toggle selection on click (no Ctrl needed)
        select.addEventListener('click', function(e) {
            console.log("Clicked", e.target);
            if (e.target.tagName === 'OPTION') {
                e.preventDefault();
                e.target.selected = !e.target.selected;
                var event = new Event('change', { bubbles: true });
                select.dispatchEvent(event);
                console.log("inner hello");
            }
        });

        function updateSelectedList() {
            selectedList.innerHTML = '';
            Array.from(select.selectedOptions).forEach(function(opt) {
                var badge = document.createElement('span');
                badge.textContent = opt.text;
                badge.style = 'background: #c8e6c9; color: #256029; padding: 3px 8px; margin: 2px; border-radius: 4px; display: inline-block;';
                selectedList.appendChild(badge);
            });
        }
        select.addEventListener('change', updateSelectedList);
        updateSelectedList();
    });
});