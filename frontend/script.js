document.addEventListener('DOMContentLoaded', () => {
    const searchInput = document.getElementById('searchInput');
    const searchButton = document.getElementById('searchButton');
    const resultsContainer = document.getElementById('results');
    const suggestionsContainer = document.createElement('div');
    suggestionsContainer.classList.add('suggestions-dropdown');
    document.body.appendChild(suggestionsContainer);
    const productListView = document.getElementById('productList');
    const productOffersView = document.getElementById('productOffers');
    const offerResultsContainer = document.getElementById('offerResults');
    const productTitle = document.getElementById('productTitle');
    const backButton = document.getElementById('backButton');

    let timeout;

    // Event listener for search input to fetch suggestions
    searchInput.addEventListener('input', () => {
        clearTimeout(timeout);
        const query = searchInput.value.trim();
        if (query.length > 1) {
            timeout = setTimeout(() => fetchSuggestions(query), 300);
        } else {
            suggestionsContainer.innerHTML = '';
            suggestionsContainer.style.display = 'none';
        }
    });

    // Fetch autocomplete suggestions
    function fetchSuggestions(query) {
        fetch(`/autocomplete?query=${encodeURIComponent(query)}`)
            .then(response => response.json())
            .then(data => displaySuggestions(data))
            .catch(error => {
                console.error('Error fetching suggestions:', error);
            });
    }

    // Display autocomplete suggestions
    function displaySuggestions(suggestions) {
        suggestionsContainer.innerHTML = '';
        if (suggestions.length > 0) {
            suggestions.forEach(suggestion => {
                const suggestionElement = document.createElement('div');
                suggestionElement.classList.add('suggestion-item');
                suggestionElement.innerHTML = `
                    <img src="${suggestion.image_url}" alt="${suggestion.name}" class="suggestion-image">
                    <span>${suggestion.name}</span>
                    <span>${suggestion.price.toFixed(2)} €</span>
                `;
                suggestionElement.addEventListener('click', () => {
                    searchInput.value = suggestion.name;
                    suggestionsContainer.style.display = 'none';
                    performSearch(suggestion.id); // Trigger search based on product id
                });
                suggestionsContainer.appendChild(suggestionElement);
            });
            suggestionsContainer.style.display = 'block';
        } else {
            suggestionsContainer.style.display = 'none';
        }
    }

    // Perform product search
    async function performSearch(productId = null) {
        const query = productId ? productId : searchInput.value.trim();
        if (!query) return;

        try {
            const response = await fetch(`/search?query=${encodeURIComponent(query)}`);
            const data = await response.json();
            displayResults(data);
        } catch (error) {
            console.error('Error fetching search results:', error);
            resultsContainer.innerHTML = '<tr><td colspan="5" class="text-red-500 text-center">An error occurred while fetching results.</td></tr>';
        }
    }

    // Display product search results
    function displayResults(products) {
        resultsContainer.innerHTML = '';
        if (products.length === 0) {
            resultsContainer.innerHTML = '<tr><td colspan="5" class="text-center">No products found.</td></tr>';
            return;
        }

        products.forEach(product => {
            const productElement = document.createElement('tr');
            const firstoffer = product.offers[0]; // Show the first offer's price

            productElement.innerHTML = `
                <td class="py-4 px-4 border-b"><img src="${product.image_url}" alt="${product.name}" class="product-image"></td>
                <td class="py-4 px-4 border-b">${product.name}</td>
                <td class="py-4 px-4 border-b">${firstoffer.store_name}</td>
                <td class="py-4 px-4 border-b text-green-600 font-bold">${firstoffer.price.toFixed(2)} €</td>
                <td class="py-4 px-4 border-b"><button class="view-offers-button" data-id="${product.id}">
                    View Offers <i class="fas fa-arrow-right"></i>
                </button></td>
            `;
            productElement.querySelector('.view-offers-button').addEventListener('click', () => loadOffers(product.id, product.name));
            resultsContainer.appendChild(productElement);
        });
    }

    // Load product offers when the user clicks 'View Offers'
    async function loadOffers(productId, productName) {
        try {
            const response = await fetch(`/product/${productId}/offers`);
            const data = await response.json();
            displayOffers(data.offers, productName);
        } catch (error) {
            console.error('Error fetching product offers:', error);
            offerResultsContainer.innerHTML = '<tr><td colspan="3" class="text-red-500 text-center">An error occurred while fetching offers.</td></tr>';
        }
    }

    // Display offers for a specific product
    function displayOffers(offers, productName) {
        productTitle.textContent = `Offers for ${productName}`;
        offerResultsContainer.innerHTML = '';

        if (offers.length === 0) {
            offerResultsContainer.innerHTML = '<tr><td colspan="3" class="text-center">No offers found.</td></tr>';
            return;
        }

        offers.forEach(offer => {
            const offerElement = document.createElement('tr');
            offerElement.innerHTML = `
                <td class="py-4 px-4 border-b">${offer.store_name}</td>
                <td class="py-4 px-4 border-b text-green-600 font-bold">${offer.price.toFixed(2)} €</td>
                <td class="py-4 px-4 border-b"><a href="${offer.link_to_product}" target="_blank" class="view-product-button">
                    View Offer <i class="fas fa-arrow-right"></i>
                </a></td>
            `;
            offerResultsContainer.appendChild(offerElement);
        });

        // Hide product list and show offers view
        productListView.classList.add('hidden');
        productOffersView.classList.remove('hidden');
    }

    // Back button to return to the product list
    backButton.addEventListener('click', () => {
        productOffersView.classList.add('hidden');
        productListView.classList.remove('hidden');
    });
});
