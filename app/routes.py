"""Flask routes for the web search application."""
import random
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
                'error': 'Aucune requête fournie'
            }), 400

        query = data['query'].strip()
        if not query:
            return jsonify({
                'success': False,
                'error': 'La requête ne peut pas être vide'
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
                'message': 'Aucun résultat trouvé'
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
            'error': f'Une erreur inattendue s\'est produite : {str(e)}'
        }), 500


@bp.route('/bebete-show')
def bebete_show():
    """
    Return a random French political figure from the 1980s as ASCII art.

    Returns:
    {
        "success": true,
        "name": "Jacques Chirac",
        "description": "...",
        "ascii_art": "..."
    }
    """
    # Dictionary of French political figures from the 1980s (without image URLs)
    political_figures = {
        1: {
            'name': 'Jacques Chirac',
            'description': 'Maire de Paris (1977-1995) et Premier ministre (1986-1988)',
            'traits': 'Chaleureux et proche du peuple, grand amateur de bière et de tête de veau. Connu pour ses petites phrases et son sens du contact. Surnommé "Le Bulldozer" pour son énergie débordante.',
            'search_query': 'Jacques Chirac portrait politique'
        },
        2: {
            'name': 'François Mitterrand',
            'description': 'Président de la République française (1981-1995)',
            'traits': 'Sphinx de la politique française, cultivé et lettré. Amateur de longues promenades solitaires et de mystères. Machiavélique et stratège hors pair, il adorait la littérature et les roses.',
            'search_query': 'François Mitterrand portrait président'
        },
        3: {
            'name': 'Georges Marchais',
            'description': 'Secrétaire général du Parti communiste français (1972-1994)',
            'traits': 'Verbe haut et franc-parler légendaire. Ouvrier métallurgiste devenu tribun populaire. Connu pour ses colères télévisées et son accent rocailleux. N\'avait pas sa langue dans sa poche.',
            'search_query': 'Georges Marchais portrait PCF'
        },
        4: {
            'name': 'Jean-Marie Le Pen',
            'description': 'Fondateur et président du Front National (1972-2011)',
            'traits': 'Tribun provocateur et polémiste redoutable. Borgne suite à une bagarre, il cultivait une image de dur. Maître des petites phrases choc et des jeux de mots douteux.',
            'search_query': 'Jean-Marie Le Pen portrait politique'
        },
        5: {
            'name': 'Raymond Barre',
            'description': 'Premier ministre (1976-1981)',
            'traits': 'Économiste rigoureux surnommé "Le meilleur économiste de France". Pédagogue et professoral, il aimait expliquer l\'économie aux Français. Gourmand notoire, amateur de bonne chère.',
            'search_query': 'Raymond Barre portrait premier ministre'
        },
        6: {
            'name': 'Michel Rocard',
            'description': 'Premier ministre (1988-1991)',
            'traits': 'Intellectuel de gauche pragmatique et réformiste. Technocrate humaniste au parler posé. Rival éternel de Mitterrand, il prônait la "deuxième gauche" et le dialogue social.',
            'search_query': 'Michel Rocard portrait politique'
        },
        7: {
            'name': 'Valéry Giscard d\'Estaing',
            'description': 'Président de la République française (1974-1981)',
            'traits': 'Aristocrate moderniste et technocrate brillant. Joueur d\'accordéon et amateur de football. Cultivait une image de jeunesse et de modernité. Hautain mais séduisant.',
            'search_query': 'Valéry Giscard d\'Estaing portrait président'
        },
        8: {
            'name': 'Simone Veil',
            'description': 'Ministre de la Santé (1974-1979) et présidente du Parlement européen (1979-1982)',
            'traits': 'Survivante de la Shoah au courage exceptionnel. Dignité et détermination incarnées. A fait voter la loi sur l\'IVG malgré les insultes. Européenne convaincue et humaniste.',
            'search_query': 'Simone Veil portrait ministre'
        },
        9: {
            'name': 'Laurent Fabius',
            'description': 'Premier ministre (1984-1986)',
            'traits': 'Jeune premier de la politique, brillant et ambitieux. Surnommé "l\'homme pressé". Technocrate raffiné au sourire carnassier. Le plus jeune Premier ministre de la Ve République.',
            'search_query': 'Laurent Fabius portrait politique'
        },
        10: {
            'name': 'Édith Cresson',
            'description': 'Première femme Premier ministre de France (1991-1992)',
            'traits': 'Battante et frondeuse, elle n\'avait pas froid aux yeux. Franc-parler et tempérament de feu. Victime de sexisme politique, elle a tenu tête dans un monde d\'hommes.',
            'search_query': 'Édith Cresson portrait premier ministre'
        }
    }

    try:
        # Pick a random number between 1 and 10
        random_number = random.randint(1, 10)
        figure = political_figures[random_number]
        print(f"[BEBETE] Selected figure #{random_number}: {figure['name']}")

        return jsonify({
            'success': True,
            'name': figure['name'],
            'description': figure['description'],
            'traits': figure['traits'],
            'ascii_art': None
        })

    except Exception as e:
        print(f"[BEBETE] Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': f'Une erreur s\'est produite : {str(e)}'
        }), 500


@bp.route('/health')
def health():
    """Health check endpoint for Azure App Service."""
    return jsonify({
        'status': 'healthy',
        'service': 'web-search-app'
    })
