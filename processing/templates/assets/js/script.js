document.addEventListener("DOMContentLoaded", function() {
    const domesticWebsiteSelect = document.getElementById("domesticWebsite");
    const domesticCategory = document.getElementById("domesticCategory");


    const internationalSectors = document.getElementById("internationalSectors");
    const inSectorsOption= document.getElementById("inSectorsOption");
    const inDestinationDirectory = document.getElementById('inDestinationDirectory')
    const inflationYear = document.getElementById('inflationYear')


    const date = document.getElementById("date");
    const startEnd = document.getElementById("start-end");
    const monthYear = document.getElementById("month-year");

    // Function to show additional information inputs
    function showAdditionalInfo(additionalInfoElement) {
        additionalInfoElement.style.display = "block";
    }

    // Function to hide additional information inputs
    function hideAdditionalInfo(additionalInfoElement) {
        additionalInfoElement.style.display = "none";
    }

    // Define category options for different websites
    const websiteCategoryOptions = {
        GDP: ['All', 'Merchandise trade', 'National account'],
        NBC: [ 'All',
               'Monetary and financial statistics data',
               'Balance of payment data',
               'Banks reports',
               'Microfinance Institution(MFI) reports',
               'Financial Literacy Centres(FLCs) reports'],
    };

    const internationalSectorOption = {
        ExchangeRate: ['Thailand', 'ADB', 'Bangladesh', 'Indonesia', 'China', 'All'],
        Export: ['Sri Lanka'],
        OpecBasketPrice: ['OPEC Basket Price'],
        InflationRate: ['Inflation Rate', 'Consumer Price Index']
    }

    // Function to update category options based on the selected website
    function internationalOptionChange(selectElement, website) {
        selectElement.innerHTML = '';
        internationalSectorOption[website].forEach(category => {
            const option = document.createElement('option');
            option.value = category;
            option.textContent = category;
            selectElement.appendChild(option);
        });
    }

    function updateCategories(selectElement, website) {
    selectElement.innerHTML = '';
    websiteCategoryOptions[website].forEach(category => {
        const option = document.createElement('option');
        option.value = category;
        option.textContent = category;
        selectElement.appendChild(option);
    });
}
    updateCategories(domesticCategory, domesticWebsiteSelect.value);

    // Event listener for domestic website selection
    domesticWebsiteSelect.addEventListener("change", function() {
        updateCategories(domesticCategory, this.value);
    });

    // showAdditionalInfo(ExchangeRateWebsite)

    hideAdditionalInfo(startEnd);
    hideAdditionalInfo(monthYear);
    hideAdditionalInfo(date);

    showAdditionalInfo(inDestinationDirectory)
    hideAdditionalInfo(inflationYear)

    internationalOptionChange(inSectorsOption, internationalSectors.value)

    internationalSectors.addEventListener("change", function(){
        internationalOptionChange(inSectorsOption, this.value);
        if (this.value === 'InflationRate'){
                showAdditionalInfo(inflationYear)
                hideAdditionalInfo(startEnd);
                hideAdditionalInfo(monthYear);
                hideAdditionalInfo(date);
                hideAdditionalInfo(inDestinationDirectory)
        } else if (this.value === 'ExchangeRate'){
                hideAdditionalInfo(startEnd);
                hideAdditionalInfo(monthYear);
                hideAdditionalInfo(date);
                showAdditionalInfo(inDestinationDirectory)
                hideAdditionalInfo(inflationYear)
        }
    })


    // Event listener for international website selection
     // Call hideAdditionalInfo to set the default state

    inSectorsOption.addEventListener("change", function() {
        // TODO: Implement event handling for international website selection


        if (this.value === "All") {
            showAdditionalInfo(startEnd);
            hideAdditionalInfo(date);
            hideAdditionalInfo(monthYear);
        } else if (this.value === "ADB") {
            hideAdditionalInfo(startEnd);
            hideAdditionalInfo(date);
            hideAdditionalInfo(monthYear);
        } else if (this.value === "Bangladesh") {
            hideAdditionalInfo(startEnd);
            hideAdditionalInfo(date);
            showAdditionalInfo(monthYear);
        } else if (this.value === "China"){
            showAdditionalInfo(inDestinationDirectory);
            showAdditionalInfo(startEnd);
            hideAdditionalInfo(date);
            hideAdditionalInfo(monthYear);
            // hideAdditionalInfo(element);
        } else if (this.value === "Indonesia"){
            hideAdditionalInfo(startEnd);
            showAdditionalInfo(date);
            hideAdditionalInfo(monthYear);
            // hideAdditionalInfo(element);
        }else if (this.value === "Thailand"){
            hideAdditionalInfo(startEnd);
            hideAdditionalInfo(date);
            hideAdditionalInfo(monthYear);
            // hideAdditionalInfo(element);
        } else if (this.value === "Sri Lanka"){
            hideAdditionalInfo(startEnd);
            hideAdditionalInfo(date);
            hideAdditionalInfo(monthYear);
            // hideAdditionalInfo(element);
        }else if (this.value === "Inflation Rate"){
            showAdditionalInfo(inflationYear)
            hideAdditionalInfo(startEnd);
            hideAdditionalInfo(date);
            hideAdditionalInfo(monthYear);
            // hideAdditionalInfo(element);
        } else if (this.value === 'Consumer Price Index'){
            hideAdditionalInfo(startEnd);
            hideAdditionalInfo(date);
            hideAdditionalInfo(monthYear);
            hideAdditionalInfo(inflationYear)
            // hideAdditionalInfo(element);
        }else {
            hideAdditionalInfo(startEnd);
            hideAdditionalInfo(date);
            hideAdditionalInfo(monthYear);
        }
    });
});