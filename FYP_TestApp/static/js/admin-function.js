document.addEventListener('DOMContentLoaded', function () {
    // Profile dropdown functionality (replacing hamburger menu)
    const profileDropdownBtn = document.getElementById('profile-dropdown-btn');
    const profileDropdown = document.getElementById('profile-dropdown');

    if (profileDropdownBtn && profileDropdown) {
        profileDropdownBtn.addEventListener('click', function (e) {
            e.stopPropagation();
            this.classList.toggle('active');
            profileDropdown.classList.toggle('show');

            // Close notification dropdown if open
            const notificationDropdown = document.getElementById('notification-dropdown');
            if (notificationDropdown && notificationDropdown.classList.contains('show')) {
                notificationDropdown.classList.remove('show');
            }
        });
    }


    // Notification functionality
    const notificationBtnHeader = document.getElementById('notification-btn-header');
    const notificationDropdownHeader = document.getElementById('notification-dropdown-header');

    if (notificationBtnHeader && notificationDropdownHeader) {
        notificationBtnHeader.addEventListener('click', function (e) {
            e.stopPropagation();
            notificationDropdownHeader.classList.toggle('show');

            // Close profile dropdown if open
            if (profileDropdown && profileDropdown.classList.contains('show')) {
                profileDropdown.classList.remove('show');
                if (profileDropdownBtn) {
                    profileDropdownBtn.classList.remove('active');
                }
            }

            // Remove notification indicator when opened
            const notificationDot = this.querySelector('span');
            if (notificationDot) {
                notificationDot.style.display = 'none';
            }
        });
    }

    // Theme toggle functionality
    const themeToggle = document.getElementById('theme-toggle');
    if (themeToggle) {
        // Check for saved theme preference or respect OS preference
        if (localStorage.getItem('darkMode') === 'true' ||
            (window.matchMedia('(prefers-color-scheme: dark)').matches &&
                localStorage.getItem('darkMode') === null)) {
            document.documentElement.classList.add('dark');
            themeToggle.checked = true;
        }

        themeToggle.addEventListener('change', function () {
            if (this.checked) {
                document.documentElement.classList.add('dark');
                localStorage.setItem('darkMode', 'true');
            } else {
                document.documentElement.classList.remove('dark');
                localStorage.setItem('darkMode', 'false');
            }
        });
    }

    // Close dropdowns when clicking outside
    document.addEventListener('click', function (e) {
        if (profileDropdown && profileDropdownBtn && !profileDropdown.contains(e.target) && e.target !== profileDropdownBtn) {
            profileDropdown.classList.remove('show');
            profileDropdownBtn.classList.remove('active');
        }

        if (notificationDropdownHeader && notificationBtnHeader && !notificationDropdownHeader.contains(e.target) && e.target !== notificationBtnHeader) {
            notificationDropdownHeader.classList.remove('show');
        }
    });

    // Post creation modal in home.html
    const titleBox = document.getElementById('title-box');
    const bodyBox = document.getElementById('body-box');
    const popupModal = document.getElementById('popup-modal');
    const closeModalBtn = document.getElementById('close-modal');
    const cancelPostBtn = document.getElementById('cancel-post');

    function openModal() {
        if (popupModal) {
            popupModal.classList.remove('hidden');
        }
    }

    function closeModal() {
        if (popupModal) {
            popupModal.classList.add('hidden');
        }
    }

    if (titleBox) titleBox.addEventListener('click', openModal);
    if (bodyBox) bodyBox.addEventListener('click', openModal);
    if (closeModalBtn) closeModalBtn.addEventListener('click', closeModal);
    if (cancelPostBtn) cancelPostBtn.addEventListener('click', closeModal);
}); 