document.addEventListener("DOMContentLoaded", function () {

    const menuBtn = document.getElementById("menu-btn");
    const sidebar = document.querySelector(".sidebar");

    if (!menuBtn || !sidebar) return;

    // Menu button
    menuBtn.addEventListener("click", function (e) {

        e.stopPropagation();

        sidebar.classList.toggle("active");

    });

    // Sidebar link click
    sidebar.querySelectorAll("a").forEach(function (link) {

        link.addEventListener("click", function () {

            if (window.innerWidth <= 991) {
                sidebar.classList.remove("active");
            }

        });

    });

    // Outside click
    document.addEventListener("click", function (e) {

        if (window.innerWidth <= 991) {

            if (
                !sidebar.contains(e.target) &&
                !menuBtn.contains(e.target)
            ) {
                sidebar.classList.remove("active");
            }

        }

    });

    // Resize
    window.addEventListener("resize", function () {

        if (window.innerWidth > 991) {
            sidebar.classList.remove("active");
        }

    });

});