(function () {
    const nav = document.querySelector(".nav-bar");

    function onScroll() {
        if (!nav) return;
        nav.classList.toggle("nav-bar--scrolled", window.scrollY > 24);
    }

    window.addEventListener("scroll", onScroll, { passive: true });
    onScroll();

    const revealElements = document.querySelectorAll(".reveal");
    if (revealElements.length && "IntersectionObserver" in window) {
        const observer = new IntersectionObserver(
            (entries) => {
                entries.forEach((entry) => {
                    if (entry.isIntersecting) {
                        entry.target.classList.add("reveal--visible");
                        observer.unobserve(entry.target);
                    }
                });
            },
            { threshold: 0.12, rootMargin: "0px 0px -40px 0px" }
        );

        revealElements.forEach((el, index) => {
            el.style.transitionDelay = `${Math.min(index * 0.08, 0.4)}s`;
            observer.observe(el);
        });
    } else {
        revealElements.forEach((el) => el.classList.add("reveal--visible"));
    }
})();
