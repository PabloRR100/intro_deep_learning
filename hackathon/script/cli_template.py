#!/usr/bin/env python3
import argparse
from similarity_template import PokemonSimilarity
import sys

def main():
    """
    TODO: Implement the main CLI functionality
    1. Set up argument parsing
    2. Initialize the similarity engine
    3. Process the input image
    4. Display the results
    5. Handle errors appropriately
    """
    # Create argument parser
    parser = argparse.ArgumentParser(
        description="Find the closest Pokemon match for an image URL",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    parser.add_argument(
        "--img-url",
        type=str,
        required=True,
        help="URL of the image to analyze"
    )
    
    # Parse arguments
    args = parser.parse_args()
    
    try:
        # TODO: Initialize the similarity engine
        # Hint: Create an instance of PokemonSimilarity
        similarity_engine = PokemonSimilarity()

        
        # TODO: Find the closest Pokemon match
        # Hint: Use the find_closest_pokemon method
        closest_pokemon = similarity_engine.find_closest_pokemon(args.img_url)
        print(f"Closest Pokemon: {closest_pokemon}")
        
        
    except Exception as e:
        print(f"❌ Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main() 