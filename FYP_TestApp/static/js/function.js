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

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }


    // Notification functionality
    const notificationBtnHeader = document.getElementById('notification-btn-header');
    const notificationDropdownHeader = document.getElementById('notification-dropdown-header');

    if (notificationBtnHeader && notificationDropdownHeader) {
        notificationBtnHeader.addEventListener('click', function (e) {
            e.stopPropagation();
            notificationDropdownHeader.classList.toggle('show');
            const csrftoken = getCookie('csrftoken');
            const user_id = document.getElementById("user_id").value

            fetch('/mark_notification/', {  // actually mark as read
                method: "POST",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded",
                    "X-CSRFToken": csrftoken
                },
                body: `user_id=${user_id}`
            })

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

    // // Mark all as read functionality for notification page
    // const markAllReadBtn = document.querySelector('.flex-1 .text-primary-600');
    // if (markAllReadBtn) {
    //     markAllReadBtn.addEventListener('click', function () {
    //         // Remove blue dot from all notifications
    //         document.querySelectorAll('.flex-1 .w-2.h-2.bg-blue-500').forEach(dot => {
    //             dot.style.display = 'none';
    //         });
    //         // Change background of unread notifications to white
    //         document.querySelectorAll('.flex-1 .bg-blue-50').forEach(item => {
    //             item.classList.remove('bg-blue-50', 'border-blue-200');
    //             item.classList.add('bg-white', 'border-gray-200');
    //         });
    //     });
    // }

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

    // Close modal when clicking outside
    if (popupModal) {
        popupModal.addEventListener('click', function (e) {
            if (e.target === popupModal) {
                closeModal();
            }
        });
    }

    // Close modal with Escape key
    document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape' && popupModal && !popupModal.classList.contains('hidden')) {
            closeModal();
        }
    });

    if (window.location.hash === '#commentTextarea') {
        const commentSection = document.getElementById('commentTextarea');
        if (commentSection) {
            commentSection.scrollIntoView({ behavior: 'smooth' });
            commentSection.focus();
        }
    }

    const filterBadWord = [
        // Sexual & pornographic
        "fuck", "fuk", "fck", "f*ck", "f@ck", "f***", "fuq", "fuxk", "phuck",
        "sex", "s3x", "s*ex", "seggs", "sx", "s*x",
        "porn", "p0rn", "p*rn", "pr0n", "pon", "purn", "phorn", "pron", "penis", "pen15", "pen1s",
        "boobs", "tits", "t!ts", "tit$", "boobz", "b00bs",
        "nude", "n00d", "n@ked", "nak3d", "naked", "nudes", "nudity",
        "pussy", "puss1", "pu55y", "p*ssy", "pusy", "pussee", "pusey",
        "dick", "d1ck", "d!ck", "d*ck", "d1k", "dic",
        "cock", "c0ck", "c*ck", "kawk", "kock",
        "cum", "c*m", "cumm", "cuum", "c0m", "cumming",
        "hentai", "henta1", "hental", "lewd",
        "slut", "slutt", "s1ut", "s!ut", "s1ltt",
        "whore", "wh0re", "h0e", "hoe", "h03",
        "rape", "rap3", "r@pe", "raep", "rapist",
        "cunt", "o0o",

        // Swearing and insults
        "shit", "sh1t", "sh!t", "sh*t", "sht", "shyt",
        "bitch", "b1tch", "b!tch", "b*tch", "biatch", "beetch",
        "asshole", "a$$hole", "as$hole", "ashole", "arsehole", "azzhole",
        "motherfucker", "mofo", "m0f0", "mthr fkr",
        "putang ina mo", "putang", "diao ni", "your mother", "your father",
        "shit", "shiet", "shlt", "sh1t",

        // Slurs & discriminatory
        "nigga", "n1gga", "n!gga", "n*gga", "niga", "ni99a", "nigger", "ni**er",
        "keling", "k@ling", "kel1ng",
        "cibai", "ci8ai", "cb", "c1bai", "cheebye", "chi bai", "chee bye", "jibai",
        "bodoh", "bodo", "b0doh",
        "sial", "sia1", "siaw",
        "sundal", "sundel", "sunndal",
        "bangsat", "b@ngsat", "b4ngsat",

        // Asian vulgarities
        "lanjiao", "lanj1ao", "lanjlao", "lan jiao", "lanjiaw", "l4njiao",
        "puki", "puk1", "pukl", "pooki",
        "kimak", "k1mak", "k*m*k", "ki mak",
        "pundek", "pndk", "pun dek",
        "mak kau hijau",

        // General
        "retard", "r3tard", "ret@rd", "idiot", "dumb", "dumba$$",
        "killyourself", "kms", "kys", "unalive", "go die",
        "terrorist", "islamophobe", "xenophobe", "homophobe",

        // Evading filters
        "f.u.c.k", "s.h.i.t", "b.i.t.c.h", "p.o.r.n", "n.i.g.g.a", "d.i.c.k", "c.u.m", "s.l.u.t",

        // Chinese vulgarities
        "他妈的", "你妈的", "操你妈", "操你", "去死", "傻逼", "傻B", "煞笔", "操", "屌", "干你娘",
        "草泥马", "妈的", "你妹", "狗娘养的", "日你", "贱人", "滚", "死全家", "肏", "婊子"
    ];

    function checkBadWords(text, warningElement) {
        const foundWords = filterBadWord.filter(word => text.includes(word));
        const submitButtons = document.querySelectorAll(".foul-button");

        if (foundWords.length > 0) {
            if (warningElement !== null) {
                warningElement.style.display = 'block';
                warningElement.textContent = `Warning: Inappropriate word(s) found – ${foundWords.join(', ')}`;
            }
            submitButtons.forEach(btn => {btn.disabled = true;})
            return false;
        } else {
            if (warningElement !== null) {
                warningElement.style.display = 'none';
            }
            submitButtons.forEach(btn => {btn.disabled = false;})
            return true;
        }
    }


    const inputs = document.querySelectorAll('.foul-checker');

    inputs.forEach(input => {
        // Create a warning element right after the input
        const warning = document.createElement('div');
        warning.className = 'badword-warning text-red-500 text-sm mt-1';
        warning.style.display = 'none';
        input.insertAdjacentElement('afterend', warning);

        let typingTimer;
        const doneTypingInterval = 100; // 100ms after user stops typing

        input.addEventListener('input', () => {
            clearTimeout(typingTimer);
            typingTimer = setTimeout(() => {
                const value = input.value.toLowerCase();
                checkBadWords(value, warning);
            }, doneTypingInterval);
        });

        input.addEventListener('keydown', () => {
            clearTimeout(typingTimer); // clear timer on keydown to reset
        });
    });

});

const filterBadWord = [
        // Sexual & pornographic
        "fuck", "fuk", "fck", "f*ck", "f@ck", "f***", "fuq", "fuxk", "phuck",
        "sex", "s3x", "s*ex", "seggs", "sx", "s*x",
        "porn", "p0rn", "p*rn", "pr0n", "pon", "purn", "phorn", "pron",
        "boobs", "tits", "t!ts", "tit$", "boobz", "b00bs",
        "nude", "n00d", "n@ked", "nak3d", "naked", "nudes", "nudity",
        "pussy", "puss1", "pu55y", "p*ssy", "pusy", "pussee", "pusey",
        "dick", "d1ck", "d!ck", "d*ck", "d1k", "dic",
        "cock", "c0ck", "c*ck", "kawk", "kock",
        "cum", "c*m", "cumm", "cuum", "c0m", "cumming",
        "hentai", "henta1", "hental", "lewd",
        "slut", "slutt", "s1ut", "s!ut", "s1ltt",
        "whore", "wh0re", "h0e", "hoe", "h03",
        "rape", "rap3", "r@pe", "raep", "rapist",
        "cunt", "o0o",

        // Swearing and insults
        "shit", "sh1t", "sh!t", "sh*t", "sht", "shyt",
        "bitch", "b1tch", "b!tch", "b*tch", "biatch", "beetch",
        "asshole", "a$$hole", "as$hole", "ashole", "arsehole", "azzhole",
        "motherfucker", "mofo", "m0f0", "mthr fkr",
        "putang ina mo", "putang", "diao ni", "your mother", "your father",
        "shit", "shiet", "shlt", "sh1t",

        // Slurs & discriminatory
        "nigga", "n1gga", "n!gga", "n*gga", "niga", "ni99a", "nigger", "ni**er",
        "keling", "k@ling", "kel1ng",
        "cibai", "ci8ai", "cb", "c1bai", "cheebye", "chi bai", "chee bye",
        "bodoh", "bodo", "b0doh",
        "sial", "sia1", "siaw",
        "sundal", "sundel", "sunndal",
        "bangsat", "b@ngsat", "b4ngsat",

        // Asian vulgarities
        "lanjiao", "lanj1ao", "lanjlao", "lan jiao", "lanjiaw", "l4njiao",
        "puki", "puk1", "pukl", "pooki",
        "kimak", "k1mak", "k*m*k", "ki mak",
        "pundek", "pndk", "pun dek",
        "mak kau hijau",

        // General
        "retard", "r3tard", "ret@rd", "idiot", "dumb", "dumba$$",
        "killyourself", "kms", "kys", "unalive", "go die",
        "terrorist", "islamophobe", "xenophobe", "homophobe",

        // Evading filters
        "f.u.c.k", "s.h.i.t", "b.i.t.c.h", "p.o.r.n", "n.i.g.g.a", "d.i.c.k", "c.u.m", "s.l.u.t",

        // Chinese vulgarities
        "他妈的", "你妈的", "操你妈", "操你", "去死", "傻逼", "傻B", "煞笔", "操", "屌", "干你娘",
        "草泥马", "妈的", "你妹", "狗娘养的", "日你", "贱人", "滚", "死全家", "肏", "婊子"
    ];

    function checkBadWords(text, warningElement) {
        const foundWords = filterBadWord.filter(word => text.includes(word));
        const submitButtons = document.querySelectorAll(".foul-button");

        if (foundWords.length > 0) {
            if (warningElement !== null) {
                warningElement.style.display = 'block';
                warningElement.textContent = `Warning: Inappropriate word(s) found – ${foundWords.join(', ')}`;
            }
            submitButtons.forEach(btn => {btn.disabled = true;})
            return false;
        } else {
            if (warningElement !== null) {
                warningElement.style.display = 'none';
            }
            submitButtons.forEach(btn => {btn.disabled = false;})
            return true;
        }
    }

// // Comment functionality
// function submitComment() {
//     const commentTextarea = document.getElementById('commentTextarea');
//     const commentText = commentTextarea.value.trim();
//
//     if (commentText === '') {
//         alert('Please enter a comment before posting.');
//         return;
//     }
//
//     // Create new comment element
//     const commentsContainer = document.querySelector('.mt-6 .space-y-4');
//     const newComment = document.createElement('div');
//     newComment.className = 'flex space-x-3';
//     newComment.innerHTML = `
//         <div class="flex-shrink-0">
//             <div class="h-8 w-8 rounded-full bg-primary-200 flex items-center justify-center text-primary-600 text-sm font-semibold">
//                 JD
//             </div>
//         </div>
//         <div class="flex-1">
//             <div class="bg-gray-50 rounded-lg p-3">
//                 <div class="flex items-center justify-between">
//                     <p class="text-sm font-medium text-gray-900">Janice</p>
//                     <p class="text-xs text-gray-500">Just now</p>
//                 </div>
//                 <p class="text-sm text-gray-700 mt-1">${commentText}</p>
//             </div>
//             <div class="flex items-center space-x-4 mt-2 ml-3">
//                 <button class="text-xs text-gray-500 hover:text-primary-600" onclick="likeComment(this)">Like</button>
//                 <button class="text-xs text-gray-500 hover:text-primary-600" onclick="replyToComment(this)">Reply</button>
//             </div>
//         </div>
//     `;
//
//     // Add the new comment to the top of the comments list
//     commentsContainer.insertBefore(newComment, commentsContainer.firstChild);
//
//     // Clear the textarea
//     commentTextarea.value = '';
//
//     // Update comment count
//     updateCommentCount();
//
//     // Show success message
//     showNotification('Comment posted successfully!', 'success');
// }

function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `fixed top-4 right-4 z-50 p-4 rounded-lg shadow-lg transition-all duration-300 transform translate-x-full`;

    if (type === 'success') {
        notification.classList.add('bg-green-500', 'text-white');
    } else {
        notification.classList.add('bg-blue-500', 'text-white');
    }

    notification.textContent = message;

    // Add to page
    document.body.appendChild(notification);

    // Animate in
    setTimeout(() => {
        notification.classList.remove('translate-x-full');
    }, 100);

    // Remove after 3 seconds
    setTimeout(() => {
        notification.classList.add('translate-x-full');
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 300);
    }, 3000);
}

// removed
// Reply functionality for comments
function replyToComment(button) {
    const commentContainer = button.closest('.flex-1');
    const replyBox = commentContainer.querySelector('.reply-box');

    if (replyBox) {
        replyBox.remove();
    } else {
        const newReplyBox = document.createElement('div');
        newReplyBox.className = 'reply-box mt-3';
        newReplyBox.innerHTML = `
            <div class="flex space-x-2">
                <textarea 
                    placeholder="Write a reply..."
                    class="flex-1 px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500 resize-none"
                    rows="2"
                ></textarea>
                <button 
                    onclick="submitReply(this)"
                    class="bg-primary-600 text-white px-4 py-2 rounded-lg hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 transition-colors"
                >
                    Reply
                </button>
            </div>
        `;
        commentContainer.appendChild(newReplyBox);
    }
}

// submission  of reply comment
function submitReply(button) {
    const replyBox = button.closest('.reply-box');
    const textarea = replyBox.querySelector('textarea');
    const replyText = textarea.value.trim();

    if (replyText === '') {
        alert('Please enter a reply before posting.');
        return;
    }

    // everything below removed
    // Get the parent comment to add the reply to
    const parentComment = replyBox.closest('.flex-1');
    const parentCommentContainer = parentComment.closest('.flex.space-x-3');

    // Create reply comment element
    const replyComment = document.createElement('div');
    replyComment.className = 'flex space-x-3 ml-8 mt-3';
    replyComment.innerHTML = `
        <div class="flex-shrink-0">
            <div class="h-6 w-6 rounded-full bg-primary-200 flex items-center justify-center text-primary-600 text-xs font-semibold">
                JD
            </div>
        </div>
        <div class="flex-1">
            <div class="bg-gray-100 rounded-lg p-2">
                <div class="flex items-center justify-between">
                    <p class="text-xs font-medium text-gray-900">Janice</p>
                    <p class="text-xs text-gray-500">Just now</p>
                </div>
                <p class="text-xs text-gray-700 mt-1">${replyText}</p>
            </div>
            <div class="flex items-center space-x-4 mt-1 ml-2">
                <button class="text-xs text-gray-500 hover:text-primary-600" onclick="likeComment(this)">Like</button>
                <button class="text-xs text-gray-500 hover:text-primary-600" onclick="replyToComment(this)">Reply</button>
            </div>
        </div>
    `;

    // Insert the reply after the parent comment
    parentCommentContainer.parentNode.insertBefore(replyComment, parentCommentContainer.nextSibling);

    // Remove the reply box
}

// comment post
function commentBtn() {
    // Scroll to comment section
    const commentSection = document.querySelector('#commentTextarea');
    if (commentSection) {
        commentSection.scrollIntoView({ behavior: 'smooth' });
        commentSection.focus();
    }
}

// save post
function bookMarkBtn() {
    const bookmarkIcon = document.getElementById('bookmarkIcon');
    const bookmarkCount = document.getElementById('bookmarkCount');

    if (bookmarkIcon && bookmarkCount) {
        const currentCount = parseInt(bookmarkCount.textContent) || 0;

        if (bookmarkIcon.classList.contains('far')) {
            // Bookmark the post
            bookmarkIcon.classList.remove('far');
            bookmarkIcon.classList.add('fas');
            bookmarkCount.textContent = currentCount + 1;
            showNotification('Post saved to bookmarks!', 'success');
        } else {
            // Remove bookmark
            bookmarkIcon.classList.remove('fas');
            bookmarkIcon.classList.add('far');
            bookmarkCount.textContent = currentCount - 1;
            showNotification('Post removed from bookmarks!', 'info');
        }
    }
}

// share post - prompt link
function shareBtn() {
    const shareCount = document.getElementById('shareCount');

    if (shareCount) {
        const currentCount = parseInt(shareCount.textContent) || 0;  // TODO: maybe swap with database info?
        shareCount.textContent = currentCount + 1;
    }

    // Show share options (you can customize this)
    if (navigator.share) {
        navigator.share({
            title: 'Check out this post on UniCompanion',
            text: 'Best resources for learning React in 2023?',
            url: window.location.href
        });
    } else {
        // Fallback for browsers that don't support Web Share API
        showNotification('Share feature coming soon!', 'info');
    }
}

// // Function to update comment count
// function updateCommentCount() {
//     const commentCountElement = document.getElementById('commentCountHeading');
//     const postCommentCount = document.getElementById('comment');
//     if (commentCountElement) {
//         const commentsContainer = document.querySelector('.mt-6 .space-y-4');
//         if (commentsContainer) {
//             const commentElements = commentsContainer.querySelectorAll('.flex.space-x-3');
//             const totalComments = commentElements.length;
//             commentCountElement.textContent = `Comments (${totalComments})`;
//             if (postCommentCount) {
//                 postCommentCount.textContent = totalComments;
//             }
//         }
//     }
// }

// report post
function reportContent(type, id, csrf) {
    const modal = document.getElementById('reportModal');
    const reasonsContainer = document.getElementById('reportReasons');
    reasonsContainer.innerHTML = '';
    // Add a textarea for user to enter their reason
    const textarea = document.createElement('textarea');
    textarea.id = 'reportReasonText';
    textarea.placeholder = "Please describe your reason for reporting...";
    textarea.className = 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500 resize-none';
    textarea.rows = 4;
    reasonsContainer.appendChild(textarea);

    modal.dataset.reportType = type;
    modal.dataset.reportId   = id;
    modal.dataset.csrf       = csrf;

    modal.classList.remove('hidden');


}

function closeReportModal() {
    document.getElementById('reportModal').classList.add('hidden');
}

function submitReport() {
    const modal      = document.getElementById('reportModal');
    const reasonText = document.getElementById('reportReasonText');
    if (!reasonText || reasonText.value.trim() === '') {
        alert('Please enter a reason for reporting.');
        return;
    }
    closeReportModal();

    const reportType = modal.dataset.reportType;
    const reportId   = modal.dataset.reportId;
    const csrf       = modal.dataset.csrf;
    let url          = "";

    if (reportType === "post") {
        url = "/report_post/"  // I can't really use django template commands...
    } else if (reportType === "comment") {
        url = "/report_comment/"
    } else if (reportType === "user") {
        url = "/report_user/"
    } else {
        console.log("what the hell happened");
        return;
    }

    fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
            "X-CSRFToken": csrf
        },
        body: `id=${reportId}&content=${reasonText.value}`
    })

    showNotification('Thank you for reporting. We will review this content.', 'success');
}

// // // Post creation functionality, no usage
// // function submitPost() {
// //     const titleInput = document.querySelector('#popup-modal input[placeholder="Title"]');
// //     const contentTextarea = document.querySelector('#popup-modal textarea[placeholder="Write your post content here..."]');
// //
// //     const title = titleInput.value.trim();
// //     const content = contentTextarea.value.trim();
// //
// //     if (!title || !content) {
// //         alert('Please fill in both title and content before posting.');
// //         return;
// //     }
// //
// //     // Create new post element
// //     const postsFeed = document.querySelector('.space-y-4');
// //     const newPost = document.createElement('div');
// //     newPost.className = 'post-card post-card-link bg-white rounded-lg shadow-sm p-6 transition duration-300 ease-in-out cursor-pointer hover:shadow-md';
// //     newPost.setAttribute('data-post-id', Date.now()); // Unique ID for the new post
// //
// //     newPost.innerHTML = `
// //         <div class="flex items-start justify-between">
// //             <div class="flex space-x-3">
// //                 <div class="flex-shrink-0">
// //                     <div class="h-10 w-10 rounded-full bg-primary-200 flex items-center justify-center text-primary-600">
// //                         <span class="text-sm font-semibold">JD</span>
// //                     </div>
// //                 </div>
// //                 <div>
// //                     <p class="text-sm font-medium text-gray-900">Janice</p>
// //                     <p class="text-xs text-gray-500">Computer Science • Just now</p>
// //                 </div>
// //             </div>
// //             <div class="flex items-start">
// //                 <div class="bg-primary-600 text-white text-xs font-bold px-3 py-1 rounded-md mr-2 inline-block">
// //                     New Post
// //                 </div>
// //             </div>
// //         </div>
// //         <div class="mt-4">
// //             <h3 class="text-lg font-semibold text-gray-900">${escapeHtml(title)}</h3>
// //             <p class="mt-2 text-gray-700">${escapeHtml(content)}</p>
// //         </div>
// //         <div class="mt-4 flex items-center justify-between">
// //             <div class="flex space-x-4">
// //                 <button class="flex items-center text-gray-500 hover:text-primary-600 transition-colors duration-200" onclick="toggleLike()">
// //                     <i class="far fa-thumbs-up mr-1"></i>
// //                     <span class="text-sm">0</span>
// //                 </button>
// //                 <button class="flex items-center text-gray-500 hover:text-primary-600" onclick="window.location.href='/indivPost'">
// //                     <i class="far fa-comment mr-1"></i>
// //                     <span class="text-sm">0</span>
// //                 </button>
// //                 <button class="p-2 rounded-full text-gray-500 hover:text-primary-600 hover:bg-primary-50" onclick="bookMarkBtn()" title="Bookmark this post">
// //                     <i class="far fa-bookmark"></i>
// //                     <span class="text-sm">0</span>
// //                 </button>
// //                 <button class="rounded-full text-gray-500 hover:text-primary-600 hover:bg-primary-50" onclick="shareBtn()" title="Share this post">
// //                     <i class="fas fa-share"></i>
// //                     <span class="text-sm">0</span>
// //                 </button>
// //                 <button class="p-2 rounded-full text-gray-500 hover:text-primary-600 hover:bg-primary-50" onclick="reportContent()" title="Report this post">
// //                     <i class="fas fa-flag"></i>
// //                     <span class="text-sm"></span>
// //                 </button>
//             </div>
//         </div>
//     `;
//
//     // Insert the new post at the top of the feed (after the "Recommended" heading)
//     const recommendedHeading = postsFeed.querySelector('.latest-heading');
//     if (recommendedHeading) {
//         const recommendedParagraph = recommendedHeading.parentElement;
//         postsFeed.insertBefore(newPost, recommendedParagraph.nextSibling);
//     } else {
//         // If no recommended heading, insert at the beginning
//         postsFeed.insertBefore(newPost, postsFeed.firstChild);
//     }
//
//     // Clear the form
//     titleInput.value = '';
//     contentTextarea.value = '';
//
//     // Close the modal
//     const popupModal = document.getElementById('popup-modal');
//     if (popupModal) {
//         popupModal.classList.add('hidden');
//     }
//
//     // Show success notification
//     showNotification('Post created successfully!', 'success');
//
//     // Make the new post card clickable
//     newPost.addEventListener('click', function (e) {
//         if (e.target.closest('button')) return;
//         window.location.href = '/indivPost';  // may have to change url to include post if or smth
//     });
// }

// // Helper function to escape HTML to prevent XSS
// function escapeHtml(text) {
//     const div = document.createElement('div');
//     div.textContent = text;
//     return div.innerHTML;
// }


