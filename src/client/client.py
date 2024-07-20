import argparse
import grpc
import src.proto.image_pb2 as image_pb2
import src.proto.image_pb2_grpc as image_pb2_grpc

from dataclasses import dataclass
from src.client.utils import create_image, get_image_data

TIMEOUT = 10


@dataclass
class ClientConfig:
    """
    Dataclass for storing client configuration for the gRPC image processing service.

    Attributes:
        host (str): Hostname or IP address of the gRPC server.
        port (int): Port number on which the gRPC server is listening.
        input (str): File path of the input image to be processed.
        output (str): Destination file path for the processed image.
        rotate (str): Specifies the degree of rotation to be applied to the image.
        mean (bool): Flag indicating whether a mean filter should be applied to the image.
    """

    host: str
    port: int
    input: str
    output: str
    rotate: str
    mean: bool


def parse_args() -> ClientConfig:
    """
    Parses command-line arguments into a configuration object.

    Returns:
        ClientConfig: A configuration object populated with user-provided values.
    """

    parser = argparse.ArgumentParser(description="Image Rotation gRPC Client")
    parser.add_argument(
        "--host", type=str, required=True, help="The host of the gRPC server"
    )
    parser.add_argument(
        "--port", type=int, required=True, help="The port of the gRPC server"
    )
    parser.add_argument(
        "--input", type=str, required=True, help="Path to input image file"
    )
    parser.add_argument(
        "--output", type=str, required=True, help="Path to output image file"
    )
    parser.add_argument(
        "--rotate",
        type=str,
        required=True,
        choices=["NONE", "NINETY_DEG", "ONE_EIGHTY_DEG", "TWO_SEVENTY_DEG"],
        help="Rotation angle",
    )
    parser.add_argument(
        "--mean", action="store_true", help="Apply mean filter to the image"
    )
    return ClientConfig(**vars(parser.parse_args()))


def create_channel_and_stub(config: ClientConfig) -> tuple:
    """
    Creates a gRPC channel and stub for communication with the server.

    Parameters:
        config (ClientConfig): Client configuration holding the host and port.

    Returns:
        tuple: The gRPC channel and the stub for making RPC calls.
    """

    channel = grpc.insecure_channel(f"{config.host}:{config.port}")
    return channel, image_pb2_grpc.NLImageServiceStub(channel)


def wait_for_server_ready(channel: grpc.Channel) -> None:
    """
    Waits for the server to be ready for a specified timeout period.

    Parameters:
        channel (grpc.Channel): The gRPC channel connected to the server.

    Raises:
        grpc.FutureTimeoutError: If the server does not become ready within the timeout period.
    """

    print(f"Waiting for server to respond. Client will timeout in {TIMEOUT} seconds.")
    try:
        grpc.channel_ready_future(channel).result(timeout=TIMEOUT)
        print("Server is ready.")
    except grpc.FutureTimeoutError:
        print("Failed to connect to server within timeout.")
        raise


def execute_rpc_calls(
    stub: image_pb2_grpc.NLImageServiceStub, config: ClientConfig
) -> None:
    """
    Executes RPC calls to process the image according to specified configurations.

    Parameters:
        stub (NLImageServiceStub): The stub used to make RPC calls.
        config (ClientConfig): Configuration specifying how the image should be processed.

    Raises:
        Exception: General exceptions captured to handle any unexpected errors during RPC execution.
    """

    try:
        # Parse the input image
        img_bytes, width, height, color = get_image_data(config.input)
        image = image_pb2.NLImage(
            color=color, data=img_bytes, width=width, height=height
        )

        response = stub.RotateImage(
            image_pb2.NLImageRotateRequest(rotation=config.rotate, image=image)
        )

        # Apply mean filter on output picture
        if config.mean:
            response = stub.MeanFilter(response)

        # Create png/jpeg image from response data
        create_image(image_pb2=response, output_path=config.output)
        print(
            f"Response received: Color={response.color}, Width={response.width}, Height={response.height}"
        )

        # print("RotateImage Response:", response)
    except Exception as e:
        print(f"An error occurred while executing rpc calls: {e}")
        raise


def start_client(config: ClientConfig) -> None:
    """
    Main client function to setup and run the image processing client.

    Parameters:
        config (ClientConfig): Configuration containing all the necessary details to connect to the server and process the image.
    """

    print("Client has started and is set up with the following arguments:")
    for key, value in vars(config).items():
        print(f"{key.capitalize()}: {value}")

    channel, stub = create_channel_and_stub(config)
    try:
        wait_for_server_ready(channel)
        execute_rpc_calls(stub, config)
    except Exception as e:
        print(f"Error during client execution: {e}")
    finally:
        channel.close()


if __name__ == "__main__":
    config = parse_args()
    start_client(config)
