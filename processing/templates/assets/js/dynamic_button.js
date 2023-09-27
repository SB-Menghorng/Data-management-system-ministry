document.addEventListener("DOMContentLoaded", function() {
    const domesticWebsiteSelect = document.getElementById("domesticWebsite");
    const internationalWebsiteSelect = document.getElementById("internationalWebsite");
    const additionalInfoDomestic = document.getElementById("additionalInfoDomestic");
    const additionalInfoInternational = document.getElementById("additionalInfoInternational");
    const additionalInfoInternational1 = document.getElementById("additionalInfoInternational1");
    const additionalInfoInternational2 = document.getElementById("additionalInfoInternational2");
    const internationalCategory = document.getElementById("internationalCategory");
    const domesticCategory = document.getElementById("domesticCategory");
    const element = document.getElementById("inputdir");


    // Define category options for different websites
    const websiteCategoryOptions = {
        website1: ['all', 'merchandise trade', 'national account'],
        website2: [ 'all',
                    'monetary_and_financial_statistics_data',
                    'balance_of_payment_data',
                    'banks_reports',
                    'mfis_reports',
                    'flcs_reports'],
        website3: ['Category 5', 'Category 6'] // Add your actual options for Website 3
    };

    // Function to show additional information inputs
    function showAdditionalInfo(additionalInfoElement) {
        additionalInfoElement.style.display = "block";
    }

    // Function to hide additional information inputs
    function hideAdditionalInfo(additionalInfoElement) {
        additionalInfoElement.style.display = "none";
    }

    // Function to update category options based on the selected website
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

    // Call hideAdditionalInfo to set the default state
    hideAdditionalInfo(additionalInfoInternational);
    hideAdditionalInfo(additionalInfoInternational1);
    hideAdditionalInfo(additionalInfoInternational2);

    // Event listener for international website selection
    internationalWebsiteSelect.addEventListener("change", function() {
        // TODO: Implement event handling for international website selection
        if (this.value === "website2") {
            showAdditionalInfo(additionalInfoInternational);
            hideAdditionalInfo(additionalInfoInternational1);
            hideAdditionalInfo(additionalInfoInternational2);
        } else if (this.value === "website5") {
            showAdditionalInfo(additionalInfoInternational1);
            hideAdditionalInfo(additionalInfoInternational);
            hideAdditionalInfo(additionalInfoInternational2);
        } else if (this.value === "website7") {
            showAdditionalInfo(additionalInfoInternational2);
            hideAdditionalInfo(additionalInfoInternational1);
            hideAdditionalInfo(additionalInfoInternational);
        } else if (this.value === "website8"){
            hideAdditionalInfo(additionalInfoInternational);
            hideAdditionalInfo(additionalInfoInternational1);
            hideAdditionalInfo(additionalInfoInternational2);
            // hideAdditionalInfo(element);
        }
        else {
            hideAdditionalInfo(additionalInfoInternational);
            hideAdditionalInfo(additionalInfoInternational1);
            hideAdditionalInfo(additionalInfoInternational2);
        }
    });
});