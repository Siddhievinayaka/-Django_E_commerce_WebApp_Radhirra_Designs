document.addEventListener('DOMContentLoaded', function () {
    // Elements
    const menuButton = document.getElementById('menu-button');
    const sidebar = document.getElementById('sidebar');
    const sidebarOverlay = document.getElementById('sidebar-overlay');
    const closeSidebarButton = document.getElementById('close-sidebar-button');
    const searchButton = document.getElementById('search-button');
    const searchDropdown = document.getElementById('search-dropdown');

    // --- Sidebar ---
    function openSidebar() {
        if (sidebar && sidebarOverlay) {
            sidebar.classList.remove('-translate-x-full');
            sidebarOverlay.classList.remove('hidden');
            sidebarOverlay.classList.remove('opacity-0');
        }
    }

    function closeSidebar() {
        if (sidebar && sidebarOverlay) {
            sidebar.classList.add('-translate-x-full');
            sidebarOverlay.classList.add('opacity-0');
            setTimeout(() => sidebarOverlay.classList.add('hidden'), 300);
        }
    }

    // --- Search ---
    function toggleSearch() {
        if (searchDropdown) {
            const isHidden = searchDropdown.classList.contains('hidden');
            if (isHidden) {
                searchDropdown.classList.remove('hidden');
                requestAnimationFrame(() => {
                    searchDropdown.classList.remove('opacity-0');
                });
            } else {
                searchDropdown.classList.add('opacity-0');
                setTimeout(() => searchDropdown.classList.add('hidden'), 300);
            }
        }
    }

    // --- Event Listeners ---
    if (menuButton) menuButton.addEventListener('click', openSidebar);
    if (closeSidebarButton) closeSidebarButton.addEventListener('click', closeSidebar);
    if (sidebarOverlay) sidebarOverlay.addEventListener('click', closeSidebar);
    if (searchButton) searchButton.addEventListener('click', toggleSearch);

    // --- Header Scroll ---
    // const header = document.getElementById('main-header');
    // if (header) {
    //     let lastScrollTop = 0;
    //     header.style.transition = 'transform 0.3s ease';

    //     window.addEventListener('scroll', function () {
    //         let scrollTop = window.pageYOffset || document.documentElement.scrollTop;

    //         if (scrollTop > lastScrollTop && scrollTop > header.offsetHeight) {
    //             // Downscroll (FIXED: px instead of %)
    //             header.style.transform = 'translateY(-74%)';
    //         } else {
    //             // Upscroll
    //             header.style.transform = 'translateY(0)';
    //         }

    //         lastScrollTop = scrollTop <= 0 ? 0 : scrollTop;
    //     });
    // }

    // --- Custom Dropdown Function ---
    const dropdowns = document.querySelectorAll('.hs-dropdown');

    function closeAllDropdowns() {
        dropdowns.forEach(dropdown => {
            const menu = dropdown.querySelector('.hs-dropdown-menu');
            if (menu && !menu.classList.contains('hidden')) {
                menu.classList.add('hidden', 'opacity-0');
                menu.classList.remove('opacity-100');
            }
        });
    }

    dropdowns.forEach(dropdown => {
        const toggle = dropdown.querySelector('.hs-dropdown-toggle');
        const menu = dropdown.querySelector('.hs-dropdown-menu');

        if (!toggle || !menu) return;

        toggle.addEventListener('click', (event) => {
            event.stopPropagation();
            const isHidden = menu.classList.contains('hidden');

            closeAllDropdowns();

            if (isHidden) {
                menu.classList.remove('hidden');
                setTimeout(() => {
                    menu.classList.remove('opacity-0');
                    menu.classList.add('opacity-100');
                }, 10);
            }
        });
    });

    document.addEventListener('click', (event) => {
        const isClickInsideDropdown = Array.from(dropdowns).some(d => d.contains(event.target));
        if (!isClickInsideDropdown) closeAllDropdowns();
    });

    // --- Product Image Gallery ---
    const mainImage = document.getElementById('main-image');
    const thumbnailImages = document.querySelectorAll('.thumbnail-image');

    if (mainImage && thumbnailImages.length > 0) {
        thumbnailImages.forEach(thumbnail => {
            thumbnail.addEventListener('click', () => {
                mainImage.src = thumbnail.src;
                thumbnailImages.forEach(img => img.classList.remove('border-2', 'border-primary'));
                thumbnail.classList.add('border-2', 'border-primary');
            });
        });
    }

    // --- Cart Update Logic ---
    const updateBtns = document.getElementsByClassName('update-cart');

    for (let i = 0; i < updateBtns.length; i++) {
        updateBtns[i].addEventListener('click', function () {
            const productId = this.dataset.product;
            const action = this.dataset.action;

            if (user === 'AnonymousUser') {
                addCookieItem(productId, action);
            } else {
                updateUserOrder(productId, action);
            }
        });
    }

    function addCookieItem(productId, action) {
        if (action == 'add') {
            if (cart[productId] == undefined) {
                cart[productId] = { quantity: 1 };
            } else {
                cart[productId].quantity += 1;
            }
        }

        if (action == 'remove') {
            cart[productId].quantity -= 1;
            if (cart[productId].quantity <= 0) delete cart[productId];
        }

        if (action == 'remove_item') delete cart[productId];

        document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/";
        location.reload();
    }

    function updateUserOrder(productId, action) {
        fetch('/update_item/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({ productId, action })
        })
            .then(res => res.json())
            .then(() => location.reload());
    }

    // --- Hero Slider (GUARDED) ---
    const heroSliderElement = document.querySelector('.hero-slider');

    if (heroSliderElement && window.Swiper) {
        new Swiper('.hero-slider', {
            loop: true,
            effect: 'fade',
            autoplay: {
                delay: 5000,
                disableOnInteraction: false,
            },
            pagination: {
                el: '.swiper-pagination',
                clickable: true,
            },
            navigation: {
                nextEl: '.swiper-button-next',
                prevEl: '.swiper-button-prev',
            },
        });
    }
});
