document.addEventListener("DOMContentLoaded", function () {

    // ==========================
    // Attendance Chart
    // ==========================
    const ctx = document.getElementById("attendanceChart");

    if (ctx) {
        new Chart(ctx, {
            type: "doughnut",
            data: {
                labels: ["Present", "Absent"],
                datasets: [{
                    data: [3, 2],
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: "bottom"
                    }
                }
            }
        });
    }

    // ==========================
    // Live Date & Time
    // ==========================
    function updateClock() {

        const now = new Date();

        const date = document.getElementById("liveDate");
        const time = document.getElementById("liveTime");

        if(date) date.innerHTML = now.toLocaleDateString();

        if(time) time.innerHTML = now.toLocaleTimeString();

    }

    updateClock();

    setInterval(updateClock,1000);

    // ==========================
    // Mobile Sidebar
    // ==========================
// ==========================
// Mobile Sidebar
// ==========================

const menuBtn = document.getElementById("menu-btn");
const sidebar = document.querySelector(".sidebar");
const overlay = document.getElementById("overlay");

if (menuBtn && sidebar) {

    menuBtn.addEventListener("click", function () {

        sidebar.classList.toggle("active");

        if (overlay) {
            overlay.classList.toggle("active");
        }

    });

}

// Sidebar link click -> mobile me close
if (sidebar) {
    sidebar.querySelectorAll("a").forEach(function(link) {

        link.addEventListener("click", function() {

            if (window.innerWidth <= 991) {
                sidebar.classList.remove("active");

                if (overlay) {
                    overlay.classList.remove("active");
                }
            }

        });

    });
}

// Overlay click -> close
if (overlay) {

    overlay.addEventListener("click", function() {

        sidebar.classList.remove("active");
        overlay.classList.remove("active");

    });

}

// Resize
window.addEventListener("resize", function() {

    if (window.innerWidth > 991) {

        sidebar.classList.remove("active");

        if (overlay) {
            overlay.classList.remove("active");
        }

    }

});
    // ==========================
    // Window Resize
    // ==========================

    window.addEventListener("resize",function(){

        if(window.innerWidth > 991){

            sidebar.classList.remove("active");

        }

    });

});