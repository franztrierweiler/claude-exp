// Main JavaScript for ASCII Web Search

document.addEventListener('DOMContentLoaded', function() {
    // Get DOM elements
    const searchForm = document.getElementById('searchForm');
    const searchQuery = document.getElementById('searchQuery');
    const numResults = document.getElementById('numResults');
    const searchButton = document.getElementById('searchButton');
    const buttonText = searchButton.querySelector('.button-text');
    const loadingSpinner = searchButton.querySelector('.loading-spinner');
    const errorMessage = document.getElementById('errorMessage');
    const loadingMessage = document.getElementById('loadingMessage');
    const resultsContainer = document.getElementById('resultsContainer');
    const results = document.getElementById('results');
    const searchQueryDisplay = document.getElementById('searchQueryDisplay');
    const newSearchButton = document.getElementById('newSearchButton');

    // Handle form submission
    searchForm.addEventListener('submit', async function(e) {
        e.preventDefault();

        const query = searchQuery.value.trim();
        if (!query) {
            showError('Please enter a search query');
            return;
        }

        // Reset UI
        hideError();
        hideResults();
        showLoading();

        // Disable form
        searchButton.disabled = true;
        buttonText.style.display = 'none';
        loadingSpinner.style.display = 'inline';

        try {
            // Make search request
            const response = await fetch('/search', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    query: query,
                    num_results: parseInt(numResults.value)
                })
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'Search request failed');
            }

            if (!data.success) {
                throw new Error(data.error || 'Search was not successful');
            }

            // Display results
            hideLoading();
            displayResults(data);

        } catch (error) {
            hideLoading();
            showError(error.message || 'An error occurred while searching');
        } finally {
            // Re-enable form
            searchButton.disabled = false;
            buttonText.style.display = 'inline';
            loadingSpinner.style.display = 'none';
        }
    });

    // Handle new search button
    newSearchButton.addEventListener('click', function() {
        hideResults();
        hideError();
        searchQuery.value = '';
        searchQuery.focus();
        document.querySelector('.search-container').scrollIntoView({ behavior: 'smooth' });
    });

    // Display results
    function displayResults(data) {
        if (!data.results || data.results.length === 0) {
            showError(data.message || 'No results found');
            return;
        }

        searchQueryDisplay.textContent = data.query;
        results.innerHTML = '';

        data.results.forEach(result => {
            const resultElement = createResultElement(result);
            results.appendChild(resultElement);
        });

        resultsContainer.style.display = 'block';
        resultsContainer.scrollIntoView({ behavior: 'smooth' });
    }

    // Create a result element
    function createResultElement(result) {
        const div = document.createElement('div');
        div.className = 'result-item';

        const header = document.createElement('div');
        header.className = 'result-header';

        const number = document.createElement('div');
        number.className = 'result-number';
        number.textContent = `#${result.index}`;

        header.appendChild(number);

        const title = document.createElement('h3');
        title.className = 'result-title';
        title.textContent = result.title;

        const link = document.createElement('a');
        link.className = 'result-link';
        link.href = result.link;
        link.target = '_blank';
        link.rel = 'noopener noreferrer';
        link.textContent = result.link;

        const snippet = document.createElement('p');
        snippet.className = 'result-snippet';
        snippet.textContent = result.snippet;

        div.appendChild(header);
        div.appendChild(title);
        div.appendChild(link);
        div.appendChild(snippet);

        // Add ASCII art if available
        if (result.ascii_art) {
            const asciiContainer = document.createElement('div');
            asciiContainer.className = 'ascii-art-container';

            const asciiPre = document.createElement('pre');
            asciiPre.className = 'ascii-art';
            asciiPre.textContent = result.ascii_art;

            asciiContainer.appendChild(asciiPre);
            div.appendChild(asciiContainer);
        } else if (result.image_url) {
            const noImage = document.createElement('p');
            noImage.className = 'no-image';
            noImage.textContent = '[Image could not be converted to ASCII]';
            div.appendChild(noImage);
        }

        return div;
    }

    // Show error message
    function showError(message) {
        errorMessage.textContent = message;
        errorMessage.style.display = 'block';
        errorMessage.scrollIntoView({ behavior: 'smooth' });
    }

    // Hide error message
    function hideError() {
        errorMessage.style.display = 'none';
    }

    // Show loading message
    function showLoading() {
        loadingMessage.style.display = 'block';
    }

    // Hide loading message
    function hideLoading() {
        loadingMessage.style.display = 'none';
    }

    // Hide results
    function hideResults() {
        resultsContainer.style.display = 'none';
    }

    // Focus on search input on load
    searchQuery.focus();
});
