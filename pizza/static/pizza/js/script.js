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
    <div class="dashboard_single_container dashboard_container">
        <div v-for="single in singles" class="dashboard_single">
            <div class="dashboard_single_top">
                <header class="dashboard_single_top_header">
                    <h3> {{ single.name }} </h3>
                </header>
                <span v-if="single.status == 'up'" class="text-success">
                    <svg width="15" height="20" viewBox="0 0 15 20" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M0.219948 7.74415L6.96942 0.244396C7.03907 0.166918 7.12178 0.105454 7.21282 0.0635184C7.30386 0.0215828 7.40145 -6.14362e-07 7.5 -6.14362e-07C7.59855 -6.14362e-07 7.69614 0.0215828 7.78718 0.0635184C7.87822 0.105454 7.96093 0.166918 8.03058 0.244396L14.7801 7.74415C14.8851 7.86069 14.9566 8.00923 14.9856 8.17096C15.0145 8.3327 14.9997 8.50035 14.9429 8.6527C14.8861 8.80504 14.7899 8.93524 14.6664 9.02679C14.543 9.11835 14.3979 9.16715 14.2495 9.16702H8.24994V19.1667C8.24994 19.3877 8.17093 19.5997 8.03029 19.7559C7.88965 19.9122 7.6989 20 7.5 20C7.3011 20 7.11035 19.9122 6.96971 19.7559C6.82907 19.5997 6.75006 19.3877 6.75006 19.1667L6.75006 9.16702H0.750532C0.602121 9.16715 0.457013 9.11835 0.333577 9.02679C0.210142 8.93524 0.11393 8.80504 0.05712 8.6527C0.000310089 8.50035 -0.0145429 8.3327 0.0144426 8.17096C0.0434281 8.00923 0.114948 7.86069 0.219948 7.74415Z" fill="#84C285"/>
                    </svg>
                    {{ single.status_percent }}% 
                </span>
                <span v-else-if="single.status == 'down'" class="text-danger">
                    <svg width="16" height="21" viewBox="0 0 16 21" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M15.2169 12.8808L8.46738 20.3806C8.39773 20.4581 8.31502 20.5195 8.22398 20.5615C8.13294 20.6034 8.03535 20.625 7.9368 20.625C7.83824 20.625 7.74066 20.6034 7.64962 20.5615C7.55857 20.5195 7.47586 20.4581 7.40621 20.3806L0.656746 12.8808C0.551746 12.7643 0.480226 12.6158 0.451241 12.454C0.422255 12.2923 0.437107 12.1247 0.493917 11.9723C0.550727 11.82 0.64694 11.6898 0.770376 11.5982C0.893812 11.5067 1.03892 11.4578 1.18733 11.458H7.18686V1.45831C7.18686 1.2373 7.26587 1.02535 7.40651 0.86907C7.54715 0.712795 7.7379 0.625 7.9368 0.625C8.13569 0.625 8.32645 0.712795 8.46709 0.86907C8.60773 1.02535 8.68674 1.2373 8.68674 1.45831V11.458H14.6863C14.8347 11.4578 14.9798 11.5067 15.1032 11.5982C15.2267 11.6898 15.3229 11.82 15.3797 11.9723C15.4365 12.1247 15.4513 12.2923 15.4224 12.454C15.3934 12.6158 15.3219 12.7643 15.2169 12.8808Z" fill="#DD483D"/>
                    </svg>
                    {{ single.status_percent }}% 
                </span>
            </div>
            <div class="dashboard_single_bottom">
                <span v-html="single.shape"> {{ single.shape }}</span><span> {{ single.result }}</span>
            </div>
        </div>
    </div>
    
    `
})
app.component("charts", {
    props: {
        line_chart_x_values: Array,
        line_chart_y_values: Array,
        doughnut_chart_x_values: Array,
        doughnut_chart_y_values: Array,
        total_money_spent: String
    },
    mounted() {
        const total_money_spent = this.total_money_spent;
        const xValues = this.line_chart_x_values;
        const yValues = this.line_chart_y_values;
        var line_chart = document.getElementById("daily_creations");
        var spent_chart = document.getElementById("total_spent");
        var ctx = line_chart.getContext("2d")
        var gradient = ctx.createLinearGradient(0, 0, 0, 400);
        gradient.addColorStop(0, 'rgba(250,174,50,.8)');
        gradient.addColorStop(1, 'rgba(250,174,50,0)');
        new Chart(line_chart, {
            type: "line",
            data: {
                labels: xValues,
                datasets: [{
                    label: "First dataset",
                    fill: true,
                    lineTension: 0.4,
                    backgroundColor: gradient,
                    borderColor: 'rgba(250,174,50,1)',
                    borderWidth: 2,
                    pointBackgroundColor: "rgba(0,0,0,0)",
                    pointBorderWidth: 0,
                    pointHoverBackgroundColor: 'rgba(250,174,50,1)',
                    pointHoverBorderWidth: 0,
                    pointHoverBorderColor: 'rgba(250,174,50,1)',
                    data: yValues
                }]
            },
            options: {
                plugins: {
                    legend: {
                        display: false
                    },
                },
                scales: {
                    x: {
                        beginAtZero: true,
                        grid: {
                            display: false,
                        },
                        border: {
                            display: false,
                        },
                        ticks: {
                            color: 'grey',
                            padding: 15,
                        }
                    },
                    y: {
                        beginAtZero: true,
                        grid: {
                            tickColor: 'rgba(0,0,0,0)',
                        },
                        border: {
                            dash: [4, 6],
                            display: false,
                        },
                        ticks: {
                            color: 'grey',
                            padding: 15,
                            min: 6,
                            max: 16,
                        }
                    }
                },
                title: {
                    display: false,
                },
                // tooltips: {
                //     callbacks: {
                //         label: function(tooltipItem) {
                //             return tooltipItem.yLabel;
                //         }
                //     }
                // }
            }
        });
        var starValues = this.doughnut_chart_x_values;
        var dyValues = this.doughnut_chart_y_values;
        var barColors = [
            "#b91d47",
            "#00aba9",
            "#2b5797",
        ];
        var ctx = spent_chart.getContext("2d")
        const centerText = {
            id: 'centerText',
            afterDatasetsDraw(chart, args, pluginOptions) {
                const { ctx, data } = chart;
                const text = total_money_spent
                ctx.save()
                const x = chart.getDatasetMeta(0).data[0].x;
                const y = chart.getDatasetMeta(0).data[0].y;
                ctx.textAlign = "center";
                ctx.textBaseline = 'middle';
                ctx.font = 'bold 30px sans-serif';

                ctx.fillText(text, x, y)
            }
        }
        new Chart("total_spent", {
            type: "doughnut",
            data: {
                labels: starValues,
                datasets: [{
                    backgroundColor: barColors,
                    borderWidth: 1,
                    cutout: '85%',
                    spacing: 3,
                    borderRadius: 30,
                    data: dyValues
                }]
            },
            options: {
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            usePointStyle: true,
                        }
                    },
                    tooltips: {
                        cornerRadius: 3,
                    },
                },
            },
            plugins: [centerText]
        });
    },
    template: `
        <div class="dashboard_graph_container dashboard_container">
            <div class="dashboard_single dashboard_first_canvas">
                <h3>Daily Creations</h3>
                <canvas id="daily_creations"></canvas>
            </div>
            <div class="dashboard_single dashboard_second_canvas">
                <h3>Daily Expenditure</h3>
                <canvas id="total_spent"></canvas>
            </div>
        </div>
    `
})
app.mount("#app");