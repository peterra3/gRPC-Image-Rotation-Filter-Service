import io
from PIL import Image, ImageStat


def is_colored(img: Image) -> bool:
    """
    Determines whether an image is colored.

    Parameters:
        img (Image): The image to check.

    Returns:
        bool: True if the image is colored, False if it is grayscale.
    """

    if img.mode != "RGB":
        img = img.convert("RGB")
    stat = ImageStat.Stat(img)

    # If the average of the sums of the channels is equal to the sum of any one channel, it's grayscale
    if sum(stat.sum) / 3 == stat.sum[0]:
        return False  # Grayscale
    else:
        return True  # Colored


def get_image_data(file_path: str) -> tuple:
    """
    Retrieves image data along with its dimensions and color status.

    Parameters:
        file_path (str): The path to the input file specified by user when running client.

    Returns:
        tuple: Contains the image bytes, width, height, and color status (True if colored, False if grayscale).
    """

    # Open the image file
    with Image.open(file_path) as img:
        # Get dimensions
        width, height = img.size

        # Convert image data to bytes, retaining the original format if possible
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format=img.format)
        img_bytes = img_byte_arr.getvalue()

        # Determine if the image is colored
        color = is_colored(img)

        return img_bytes, width, height, color


def create_image(image_pb2, output_path) -> None:
    """
    Creates an image file from protobuf data returned by server

    Parameters:
        image_pb2 (ImagePB2): Protobuf containing image data.
        output_path (str): The path where the image will be saved.
    """

    # Create a BytesIO object from the byte data
    image_stream = io.BytesIO(image_pb2.data)

    # Open the image as a PIL Image object
    image = Image.open(image_stream)

    image.save(output_path)
