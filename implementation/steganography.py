import base64
import logging
from PIL import Image
from meth.pvd import PVDAlgorithm

logging.basicConfig(filename='steganography.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s') # basic action logging config

class Steganography:
    def embed_text(self, image_path, text):
        logging.info(f"Embedding text into image: {image_path}")
        image = Image.open(image_path)
        if image.mode != 'RGB': # convert to RGB if not already
            image = image.convert('RGB')
        data = base64.b64encode(text.encode())
        logging.info(f"Encrypted data length: {len(data)}")
        data_with_end_marker = data + b'###END###' # add end marker
        image = PVDAlgorithm.embed(image, data_with_end_marker)
        return image

    def save_image(self, image, save_path): # utility function to save image
        image.save(save_path)
        logging.info(f"Saved stego image to: {save_path}")

    def decode_text(self, image_path):
        logging.info(f"Decoding text from image: {image_path}")
        image = Image.open(image_path)
        data = PVDAlgorithm.extract(image)
        data = data.replace('###END###', '')
        decrypted_data = self._apply_decryption(data.encode('latin1')) # decode if encryption enabled, latin1 encoding
        logging.info(f"Decrypted data length: {len(decrypted_data)}")
        return decrypted_data.decode()

    def _apply_decryption(self, data):
        missing_padding = len(data) % 4 # base64 requires data length to be multiple of 4
        if missing_padding:
            data += b'=' * (4 - missing_padding) # pads with '=' to meet requirement
        return base64.b64decode(data)
