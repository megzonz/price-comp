document.addEventListener('DOMContentLoaded', () => {
    const searchInput = document.getElementById('searchInput');
    const searchButton = document.getElementById('searchButton');
    const resultsContainer = document.getElementById('results');

    searchButton.addEventListener('click', performSearch);
    searchInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            performSearch();
        }
    });

    async function performSearch() {
        const query = searchInput.value.trim();
        if (query === '') return;

        try {
            const response = await fetch(`/search?query=${encodeURIComponent(query)}`);
            const data = await response.json();
            displayResults(data.products);
        } catch (error) {
            console.error('Error fetching search results:', error);
            resultsContainer.innerHTML = '<tr><td colspan="5" class="text-red-500 text-center">An error occurred while fetching results.</td></tr>';
        }
    }

    function displayResults(products) {
        resultsContainer.innerHTML = '';
        if (products.length === 0) {
            resultsContainer.innerHTML = '<tr><td colspan="5" class="text-center">No products found.</td></tr>';
            return;
        }

        products.forEach(product => {
            // Log the raw product data for debugging
            console.log('Raw Product Data:', product);

            const productElement = document.createElement('tr');
            productElement.innerHTML = `
                <td class="py-4 px-4 border-b"><img src="${product.image_url}" alt="${product.name}" class="w-24 h-24 object-cover"></td>
                <td class="py-4 px-4 border-b">${product.name}</td>
                <td class="py-4 px-4 border-b">${product.store_name}</td>
                <td class="py-4 px-4 border-b text-green-600 font-bold">${product.price.toFixed(2)} €</td>
                <td class="py-4 px-4 border-b"><a href="${product.link_to_product}" target="_blank" class="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600">View Product</a></td>
            `;
            resultsContainer.appendChild(productElement);
        });
    }
});
