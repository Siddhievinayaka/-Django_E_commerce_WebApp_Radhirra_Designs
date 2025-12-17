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
    const header = document.getElementById('main-header');
    let lastScrollTop = 0;

    window.addEventListener('scroll', function () {
        let scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        if (scrollTop > lastScrollTop && scrollTop > header.offsetHeight) {
            // Downscroll
            header.style.transform = 'translateY(-74%)';
        } else {
            // Upscroll
            header.style.transform = 'translateY(0)';
        }
        lastScrollTop = scrollTop <= 0 ? 0 : scrollTop; // For Mobile or negative scrolling
    });

    // --- Custom Dropdown Function ---
    const dropdowns = document.querySelectorAll('.hs-dropdown');

    // Function to close all dropdowns
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

        toggle.addEventListener('click', (event) => {
            event.stopPropagation(); // Prevent the document click from firing immediately
            const isHidden = menu.classList.contains('hidden');

            // First, close all dropdowns.
            closeAllDropdowns();

            // If the clicked menu was hidden, show it.
            if (isHidden) {
                menu.classList.remove('hidden');
                // Use a small timeout to allow the CSS transition to apply
                setTimeout(() => {
                    menu.classList.remove('opacity-0');
                    menu.classList.add('opacity-100');
                }, 10);
            }
        });
    });

    // Add a listener to the document to close dropdowns when clicking outside
    document.addEventListener('click', (event) => {
        const isClickInsideDropdown = Array.from(dropdowns).some(d => d.contains(event.target));

        if (!isClickInsideDropdown) {
            closeAllDropdowns();
        }
    });

    // --- Product Image Gallery ---
    const mainImage = document.getElementById('main-image');
    const thumbnailImages = document.querySelectorAll('.thumbnail-image');

    if (mainImage && thumbnailImages.length > 0) {
        thumbnailImages.forEach(thumbnail => {
            thumbnail.addEventListener('click', () => {
                // Set the main image src to the clicked thumbnail's src
                mainImage.src = thumbnail.src;

                // Remove active border from all thumbnails
                thumbnailImages.forEach(img => {
                    img.classList.remove('border-2', 'border-primary');
                });

                // Add active border to the clicked thumbnail
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
            console.log('productId:', productId, 'Action:', action);

            console.log('USER:', user);
            if (user === 'AnonymousUser') {
                addCookieItem(productId, action);
            } else {
                updateUserOrder(productId, action);
            }
        });
    }

    function addCookieItem(productId, action) {
        console.log('Not logged in..');

        if (action == 'add') {
            if (cart[productId] == undefined) {
                cart[productId] = { 'quantity': 1 };
            } else {
                cart[productId]['quantity'] += 1;
            }
        }

        if (action == 'remove') {
            cart[productId]['quantity'] -= 1;

            if (cart[productId]['quantity'] <= 0) {
                console.log('Remove Item');
                delete cart[productId];
            }
        }

        if (action == 'remove_item') {
            console.log('Remove Item');
            delete cart[productId];
        }

        console.log('Cart:', cart);
        document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/";
        location.reload();
    }


    function updateUserOrder(productId, action) {
        console.log('User is logged in, sending data...');

        const url = '/update_item/';

        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({ 'productId': productId, 'action': action })
        })
            .then((response) => {
                return response.json();
            })
            .then((data) => {
                console.log('Data:', data);
                location.reload();
            });
    }

    // --- Hero Slider ---
    const heroSlider = new Swiper('.hero-slider', {
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
});