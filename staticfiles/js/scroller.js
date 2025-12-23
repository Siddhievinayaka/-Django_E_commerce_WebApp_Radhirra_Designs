document.addEventListener('DOMContentLoaded', function () {
    const navbar = document.querySelector('header'); // or your navbar selector
    let lastScrollY = window.scrollY;

    window.addEventListener('scroll', function () {
        if (window.scrollY > lastScrollY && window.scrollY > 100) {
            navbar.style.transform = 'translateY(-74%)';
        } else {
            navbar.style.transform = 'translateY(0)';
        }
        lastScrollY = window.scrollY;
    }, { passive: true });
});
