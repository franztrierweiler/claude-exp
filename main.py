#!/usr/bin/env python3
"""
Google Search CLI Tool
A command-line tool for performing Google searches and displaying results in ASCII format.
"""
import sys
import argparse
from search import GoogleSearcher
from formatter import AsciiFormatter


def main():
    """Main entry point for the CLI tool."""
    parser = argparse.ArgumentParser(
        description='Perform Google searches and display results in ASCII format'
    )
    parser.add_argument(
        'query',
        type=str,
        nargs='+',
        help='Search query (can be multiple words)'
    )
    parser.add_argument(
        '-n',
        '--num-results',
        type=int,
        default=5,
        help='Number of results to display (default: 5, max: 5)'
    )

    args = parser.parse_args()

    # Join query words into a single string
    query = ' '.join(args.query)

    # Limit results to 5
    num_results = min(args.num_results, 5)

    try:
        # Initialize searcher and formatter
        searcher = GoogleSearcher()
        formatter = AsciiFormatter()

        # Display header
        print(formatter.format_header(query, num_results))

        # Perform search
        results = searcher.search(query, num_results)

        if not results:
            print("\nNo results found or search failed.")
            return 1

        # Display results
        for idx, result in enumerate(results, 1):
            if result.get('image'):
                # Download and display image as ASCII
                image_data = searcher.download_image(result['image'])
                if image_data:
                    print(formatter.format_image_result(result, idx, image_data))
                else:
                    print(formatter.format_result(result, idx))
                    print("[Image could not be downloaded]\n")
            else:
                print(formatter.format_result(result, idx))

        # Display footer
        print(formatter.format_footer())

        return 0

    except ValueError as e:
        print(f"\nError: {e}")
        return 1
    except KeyboardInterrupt:
        print("\n\nSearch interrupted by user.")
        return 130
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        return 1


if __name__ == '__main__':
    sys.exit(main())
