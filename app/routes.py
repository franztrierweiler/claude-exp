"""Flask routes for the web search application."""
from flask import Blueprint, render_template, request, jsonify
from app.search import SearchEngine
from app.formatter import AsciiFormatter

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    """Render the homepage with search form."""
    return render_template('index.html')


@bp.route('/search', methods=['POST'])
def search():
    """
    Handle search requests and return results as JSON.

    Expected JSON payload:
    {
        "query": "search query",
        "num_results": 5
    }

    Returns:
    {
        "success": true,
        "query": "search query",
        "results": [...]
    }
    """
    try:
        data = request.get_json()

        if not data or 'query' not in data:
            return jsonify({
                'success': False,
                'error': 'No query provided'
            }), 400

        query = data['query'].strip()
        if not query:
            return jsonify({
                'success': False,
                'error': 'Query cannot be empty'
            }), 400

        num_results = min(int(data.get('num_results', 5)), 5)

        # Perform search
        searcher = SearchEngine()
        search_results = searcher.search(query, num_results)

        if not search_results:
            return jsonify({
                'success': True,
                'query': query,
                'results': [],
                'message': 'No results found'
            })

        # Format results and download images for ASCII conversion
        formatter = AsciiFormatter(width=80)
        formatted_results = []

        for idx, result in enumerate(search_results, 1):
            ascii_art = None

            # Try to download and convert image to ASCII
            if result.get('image'):
                image_data = searcher.download_image(result['image'])
                if image_data:
                    ascii_art = formatter.image_to_ascii(image_data, width=60)

            formatted_result = formatter.format_result_for_web(result, idx, ascii_art)
            formatted_results.append(formatted_result)

        return jsonify({
            'success': True,
            'query': query,
            'results': formatted_results
        })

    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'An unexpected error occurred: {str(e)}'
        }), 500


@bp.route('/health')
def health():
    """Health check endpoint for Azure App Service."""
    return jsonify({
        'status': 'healthy',
        'service': 'web-search-app'
    })
