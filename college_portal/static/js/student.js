document.addEventListener("DOMContentLoaded", function () {

    const ctx = document.getElementById("attendanceChart");

    if (!ctx) return;

    new Chart(ctx, {
        type: "doughnut",
        data: {
            labels: ["Present", "Absent"],
            datasets: [{
                data: [82, 18],
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: "bottom"
                }
            }
        }
    });

});

setInterval(function(){

const now=new Date();

document.getElementById("liveDate").innerHTML=
now.toLocaleDateString();

document.getElementById("liveTime").innerHTML=
now.toLocaleTimeString();

},1000);

const menu=document.getElementById("menu-btn");

const sidebar=document.querySelector(".sidebar");

if(menu){
menu.onclick=function(){
sidebar.classList.toggle("active");
}
}