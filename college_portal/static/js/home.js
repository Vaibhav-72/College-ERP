// ===========================================
// HERO SLIDER
// ===========================================

const heroSlider = document.querySelector("#heroSlider");

if (heroSlider) {

    new bootstrap.Carousel(heroSlider, {

        interval: 5000,

        ride: "carousel",

        pause: false,

        touch: true

    });

}



// ===========================================
// SMOOTH SCROLL
// ===========================================

document.documentElement.style.scrollBehavior = "smooth";



// ===========================================
// BACK TO TOP BUTTON
// ===========================================

const topBtn = document.querySelector(".top-btn");

window.addEventListener("scroll", () => {

    if (window.scrollY > 300) {

        topBtn.style.opacity = "1";

        topBtn.style.visibility = "visible";

    }

    else {

        topBtn.style.opacity = "0";

        topBtn.style.visibility = "hidden";

    }

});



// ===========================================
// NAVBAR SHADOW
// ===========================================

const navbar = document.querySelector(".custom-navbar");

window.addEventListener("scroll", () => {

    if (window.scrollY > 80) {

        navbar.style.padding = "8px 0";

        navbar.style.boxShadow = "0 15px 35px rgba(0,0,0,.15)";

    }

    else {

        navbar.style.padding = "12px 0";

        navbar.style.boxShadow = "0 8px 25px rgba(0,0,0,.08)";

    }

});



// ===========================================
// COUNTER ANIMATION
// ===========================================

const counters = document.querySelectorAll(".counter-section h2");

let started = false;

window.addEventListener("scroll", () => {

    const section = document.querySelector(".counter-section");

    if (!section) return;

    if (window.scrollY > section.offsetTop - 500 && !started) {

        started = true;

        counters.forEach(counter => {

            let text = counter.innerText;

            let end = parseInt(text);

            let count = 0;

            let speed = end / 100;

            let interval = setInterval(() => {

                count += speed;

                if (count >= end) {

                    counter.innerText = text;

                    clearInterval(interval);

                }

                else {

                    counter.innerText = Math.floor(count) + "+";

                }

            },20);

        });

    }

});



// ===========================================
// IMAGE HOVER EFFECT
// ===========================================

document.querySelectorAll(".gallery-img").forEach(img=>{

    img.addEventListener("mouseenter",()=>{

        img.style.transform="scale(1.08)";

    });

    img.addEventListener("mouseleave",()=>{

        img.style.transform="scale(1)";

    });

});


// PRELOADER

window.addEventListener("load",()=>{

setTimeout(()=>{

document.getElementById("loader").style.opacity="0";

document.getElementById("loader").style.visibility="hidden";

},1500);

});