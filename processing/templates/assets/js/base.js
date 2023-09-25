      const tabs = document.querySelectorAll(".tab");
        const configContents = document.querySelectorAll(".config-content");

        tabs.forEach((tab) => {
            tab.addEventListener("click", () => {
                const target = tab.getAttribute("data-target");
                tabs.forEach((t) => t.classList.remove("active"));
                tab.classList.add("active");
                configContents.forEach((content) => content.classList.remove("active"));
                document.getElementById(target).classList.add("active");
            });
        })