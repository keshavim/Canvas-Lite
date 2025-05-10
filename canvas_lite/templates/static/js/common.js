document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('select[multiple]').forEach(function (select) {
        var selectedList = document.getElementById(select.id + '-selected-list');
        if (!selectedList) return;

        function updateSelectedList() {
            selectedList.innerHTML = '';
            Array.from(select.selectedOptions).forEach(function (opt) {
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

window.addEventListener('DOMContentLoaded', function () {
    document.body.style.visibility = 'visible';
});