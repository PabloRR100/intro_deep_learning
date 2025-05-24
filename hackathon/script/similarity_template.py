# import torch
import pickle
from PIL import Image
# import io
import requests
# import base64
# from torchvision import transforms
# import torchvision.models as models
# from pathlib import Path
import timm
# import BytesIOfrom io import BytesIO
from io import BytesIO
import numpy as np
from PIL import Image as PILImage
# --- Device Selection ---
# TODO: Implement device selection logic
# Hint: Check for CUDA, MPS, or fallback to CPU
device = "cpu"  # Replace with your implementation

# --- Load Pretrained Model ---
def get_model():
    """
    TODO: Implement model loading
    - Load a pretrained model (e.g., ResNet18)
    - Remove the classification head
    - Set the model to evaluation mode
    - Move the model to the appropriate device
    
    Returns:
        torch.nn.Module: The prepared model
    """

    # Your implementation here
    return timm.create_model('mobilenetv3_small_100.lamb_in1k', pretrained=True)
    # pass

# --- Image Preprocessing ---
# TODO: Define your image transformation pipeline
# Hint: Consider resizing, normalization, and tensor conversion
# transform = transforms.Compose([])

def load_embeddings_from_pickle(path):
  with open(path, 'rb') as handle:
    embeddings = pickle.load(handle)
  return embeddings

class PokemonSimilarity:
    def __init__(self):
        """
        TODO: Initialize the similarity engine
        - Load the model
        - Load the database of Pokemon embeddings
        """
        self.model = get_model()
        self.db = self._load_db()

    def _load_db(self):
        """
        TODO: Implement database loading
        - Look for the embeddings file in different possible locations
        - Load the pickle file containing Pokemon embeddings
        - Handle cases where the file is not found
        
        Returns:
            list: List of dictionaries containing Pokemon embeddings and labels
        """
        with open('../solutions/embeddings.pickle', 'rb') as handle:
            return pickle.load(handle)
        # return  load_embeddings_from_pickle('../solutembeddings.pickle')

        

    def load_image(self, image_input):
        """
        TODO: Implement image loading
        Handle different input formats:
        - URL strings
        - Base64 encoded image strings
        - Bytes objects
        - PIL Image objects
        
        Args:
            image_input: Image in various formats
            
        Returns:
            PIL.Image: The loaded image in RGB format
        """
        # Your implementation here
        # img = None
        # if not isinstance(image_input, PILImage.Image):
        print(f"image_input: {image_input}")

        if isinstance(image_input, str) and (image_input.startswith("http://") or image_input.startswith("https://")):
        # if image_input.startswith("http://") or image_input.startswith("https://"):
            response = requests.get(image_input)
            response.raise_for_status()  # Lanza error si no se puede descargar
            img = Image.open(BytesIO(response.content))
        elif isinstance(image_input, str):
            img = PILImage.open(image_input)
        else:
            bytes_data = image_input.getvalue()
            img = Image.open(BytesIO(bytes_data)).convert("RGB")

            
        # elif isinstance(image_input, bytes):
    
        # elif isinstance(image_input, PILImage.Image):
        #     img = image_input
        # else: 
        #     img = Image.open(BytesIO(image_input))

        # img = PILImage.open(image_input)
        if img.mode =='RGBA': 
            img = img.convert('RGB')
        elif img.mode =='L':
            img = img.convert('RGB')
        elif img.mode =='P':
            img = img.convert('RGB')
        return img

    def get_embedding(self, image):
        """
        TODO: Implement embedding generation
        Generate a feature vector for the input image using the model
        
        Args:
            image (PIL.Image): Input image to generate embedding for
            
        Returns:
            numpy.ndarray: The image embedding
        """
        # Your implementation here
        self.model.eval()
        data_config = timm.data.resolve_model_data_config(self.model)
        transforms = timm.data.create_transform(**data_config, is_training=False)
        return self.model(transforms(image).unsqueeze(0))

    def cosine_similarity(self, a, b):
        """
        TODO: Implement cosine similarity
        Calculate the cosine similarity between two vectors
        
        Args:
            a: First vector
            b: Second vector
            
        Returns:
            float: Cosine similarity score
        """
        a = a.detach().numpy().flatten()
        b = b.detach().numpy().flatten()
        return np.dot(a,b) / (np.linalg.norm(a) * np.linalg.norm(b))

    def find_closest_pokemon(self, image_input):
        """
        TODO: Implement Pokemon matching
        1. Load the input image
        2. Generate its embedding
        3. Compare with all Pokemon embeddings in the database
        4. Return the name of the most similar Pokemon
        
        Args:
            image_input: Image in various formats (URL, base64, bytes, PIL Image)
            
        Returns:
            str: Name of the most similar Pokemon
        """
        # Your implementation here
        image = self.load_image(image_input)
        embedding = self.get_embedding(image)
        max_similarity = -1
        closest_pokemon = None
        
        for pokemons in self.db:
            suma_similarity = 0
            # value = 0
            for pokemon in self.db[pokemons]:
                # print(pokemon)
                similarity = self.cosine_similarity(embedding, pokemon['embedding'])
                suma_similarity = similarity + suma_similarity
            value = suma_similarity / len(self.db[pokemons])

            if value > max_similarity:
                max_similarity = value
                closest_pokemon = pokemons

        print(f"Pokemon: {closest_pokemon} - Similarity: {value}")
                # closest_pokemon = pokemons[0]['label']
        return closest_pokemon 


if __name__ == "__main__":
    similarity_engine = PokemonSimilarity()
    # print(similarity_engine.find_closest_pokemon("https://alfabetajuega.com/hero/2019/03/Squirtle-Looking-Happy.jpg?width=1200&aspect_ratio=16:9")) 
    