document.addEventListener("DOMContentLoaded", () => {

    document.querySelectorAll(".mf-alert").forEach(alert => {

        const close = () => {

            alert.style.animation = "mfAlertOut .35s ease forwards";

            setTimeout(() => {

                alert.remove();

            },350);

        };

        alert.querySelector(".mf-alert-close")
            .addEventListener("click", close);

        let timer = setTimeout(close,5000);

        alert.addEventListener("mouseenter",()=>{

            clearTimeout(timer);

        });

        alert.addEventListener("mouseleave",()=>{

            timer = setTimeout(close,3000);

        });
        
    });

});
