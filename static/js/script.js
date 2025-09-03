        document.addEventListener('DOMContentLoaded', function() {
            const burgerMenu = document.querySelector('.burger-menu');
            const nav = document.querySelector('nav');
            
            burgerMenu.addEventListener('click', function() {
                this.classList.toggle('active');
                nav.classList.toggle('active');
            });
            
            // Close menu when clicking on a link
            const navLinks = document.querySelectorAll('nav a');
            navLinks.forEach(link => {
                link.addEventListener('click', function() {
                    burgerMenu.classList.remove('active');
                    nav.classList.remove('active');
                });
            });
            
            // Close menu when clicking outside
            document.addEventListener('click', function(event) {
                const isClickInsideNav = nav.contains(event.target);
                const isClickOnBurger = burgerMenu.contains(event.target);
                
                if (!isClickInsideNav && !isClickOnBurger && nav.classList.contains('active')) {
                    burgerMenu.classList.remove('active');
                    nav.classList.remove('active');
                }
            });
        });
// ---------------------Animation--------------------------------------
const skillsTrack = document.querySelector('.skills-track');
const skillsContainer = document.querySelector('.skills-container');

// Pause on hover
skillsTrack.addEventListener('mouseenter', function() {
    skillsContainer.classList.add('pause');
});

// Resume when not hovering
skillsTrack.addEventListener('mouseleave', function() {
    skillsContainer.classList.remove('pause');
});
// Pause-Resume Button
const Button = document.querySelectorAll("#playPauseBtn");
let ispause = true;

Button.forEach((val) => {
    val.addEventListener("click", () => {

        if(ispause) {
            skillsContainer.classList.add('pause');
            Button.innerText = "▶";

        }
        else{
            skillsContainer.classList.remove('pause');
            Button.innerText = "❚❚"
        }
        ispause = !ispause;
    })
})
