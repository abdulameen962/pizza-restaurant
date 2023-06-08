const app = Vue.createApp({
    delimiters: ["[[", "]]"],
    data() {
        return {}
    },
    mounted() {
        var inners = document.querySelectorAll("ul.socialaccount_providers li a");
        var checkbox = document.querySelector("[type='checkbox']");
        var aside = document.querySelector("aside");
        var navbar = document.querySelector(".responsive_content .responsive_content_nav");
        if (inners) {
            inners.forEach(function(e) {
                if (e.innerHTML == "Sign in with Google") {
                    e.innerHTML = `
                    Sign in with Google<img src="/static/predictions/css/images/Google.svg" alt="google"/>
                    `
                    e.style.display = "flex";
                } else if (e.innerHTML == "Sign in with Instagram") {
                    e.innerHTML = `
                    <img src="/static/predictions/css/images/instagram.svg" alt="google"/>
                    `
                    e.style.display = "none";
                } else if (e.innerHTML == "Sign in with Facebook") {
                    e.innerHTML = `
                    <img src="/static/predictions/css/images/facebook.svg" alt="google"/>
                    `
                    e.style.display = "none";
                }
            })
        }
        if (checkbox) {
            checkbox.checked = true;
        }
        if (navbar) {
            var section = document.querySelector(".aside_nav section");
            if (window.matchMedia("(max-width: 991px)").matches) {
                var mainheader = document.querySelector("section div .navbar-brand");
                mainheader.remove();
                aside.append(mainheader);
                aside.insertBefore(mainheader, aside.children[0]);
                var notification = document.querySelector(".nav_side .dropdown");
                notification.remove()
                var responsive_content = document.querySelector(".responsive_content");
                responsive_content.append(notification);
                responsive_content.insertBefore(notification, responsive_content.children[0]);
                navbar.onclick = () => {
                    if (section.className == "") {
                        //get the form to add
                        var searchbar = document.querySelector(".nav_side form");
                        if (searchbar) {
                            searchbar.remove();
                            //get the maindiv
                            var maindiv = section.children[0];
                            maindiv.append(searchbar);
                            maindiv.insertBefore(searchbar, maindiv.children[0])
                        };
                        //change the searcbar icon
                        navbar.innerHTML = `<svg class="responsive_content_nav_icon"  width="12" height="12" viewBox="0 0 12 12" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M11 1L1 11M1 1L11 11" stroke="#B2B4BE" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                        </svg>
                        `;
                        section.classList.add("active_section");
                    } else if (section.className == "active_section") {
                        section.classList.remove("active_section");
                        navbar.innerHTML = `<svg class="responsive_content_nav_icon"  width="12" height="9" viewBox="0 0 12 9" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M0 0.5C0 0.367392 0.0526785 0.240215 0.146447 0.146447C0.240215 0.0526785 0.367392 0 0.5 0H11.5C11.6326 0 11.7598 0.0526785 11.8536 0.146447C11.9473 0.240215 12 0.367392 12 0.5C12 0.632608 11.9473 0.759785 11.8536 0.853553C11.7598 0.947321 11.6326 1 11.5 1H0.5C0.367392 1 0.240215 0.947321 0.146447 0.853553C0.0526785 0.759785 0 0.632608 0 0.5ZM0 4.5C0 4.36739 0.0526785 4.24021 0.146447 4.14645C0.240215 4.05268 0.367392 4 0.5 4H11.5C11.6326 4 11.7598 4.05268 11.8536 4.14645C11.9473 4.24021 12 4.36739 12 4.5C12 4.63261 11.9473 4.75979 11.8536 4.85355C11.7598 4.94732 11.6326 5 11.5 5H0.5C0.367392 5 0.240215 4.94732 0.146447 4.85355C0.0526785 4.75979 0 4.63261 0 4.5ZM0 8.5C0 8.36739 0.0526785 8.24021 0.146447 8.14645C0.240215 8.05268 0.367392 8 0.5 8H11.5C11.6326 8 11.7598 8.05268 11.8536 8.14645C11.9473 8.24021 12 8.36739 12 8.5C12 8.63261 11.9473 8.75979 11.8536 8.85355C11.7598 8.94732 11.6326 9 11.5 9H0.5C0.367392 9 0.240215 8.94732 0.146447 8.85355C0.0526785 8.75979 0 8.63261 0 8.5Z" fill="#B2B4BE"/>
                        </svg>
                        `;
                    }
                }
            }
        }
    },
    methods: {}
})

app.component("dashboard-singles", {
    props: {
        singles: Array
    },
    template: `
    <div class="dashboard_single_container">
        <div v-for="single in singles" class="dashboard_single">
            <div class="dashboard_single_top">
                <header class="dashboard_single_top_header">
                    <h3> {{ single.name }} </h3>
                </header>
                <span v-if="single.status == 'up'" class="text-success"> {{ single.status_percent }} </span>
                <span v-else-if="single.status == 'down'" class="text-danger"> {{ single.status_percent }}% </span>
            </div>
            <div class="dashboard_single_bottom">
                <span v-html="single.shape"> {{ single.shape }} {{ single.result }} </span>
            </div>
        </div>
    </div>
    
    `
})

app.mount("body");