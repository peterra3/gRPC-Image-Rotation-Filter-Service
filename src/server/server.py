import argparse
import grpc
import src.proto.image_pb2_grpc as image_pb2_grpc

from src.server.services import NLImageServiceServicer
from concurrent import futures
from dataclasses import dataclass
from multiprocessing import cpu_count


@dataclass
class ServerConfig:
    """
    Configuration dataclass for gRPC server.

    Attributes:
        port (int): The port number on which the server should listen.
        host (str): The host name or IP address on which the server should bind.
    """

    port: int
    host: str


def parse_args() -> ServerConfig:
    """
    Parses command line arguments to configure the gRPC server.

    Returns:
        ServerConfig: Configuration object populated with command line arguments.
    """

    parser = argparse.ArgumentParser(description="Image Rotation gRPC Server")
    parser.add_argument(
        "--port",
        type=int,
        required=True,
        help="The port on which to serve the application",
    )
    parser.add_argument(
        "--host",
        type=str,
        required=True,
        help="The host on which to serve the application",
    )
    args = parser.parse_args()
    return ServerConfig(**vars(args))


def create_server() -> grpc.server:
    """
    Creates a gRPC server with a specified number of thread workers.

    Returns:
        grpc.Server: A new gRPC server instance.
    """
    num_workers = cpu_count() * 2
    return grpc.server(futures.ThreadPoolExecutor(max_workers=num_workers))


def register_services(server: grpc.Server) -> None:
    """
    Registers gRPC services with the server.

    Parameters:
        server (grpc.Server): The server to which the services will be registered.
    """

    image_pb2_grpc.add_NLImageServiceServicer_to_server(
        NLImageServiceServicer(), server
    )


def start_server(server: grpc.Server, config: ServerConfig) -> None:
    """
    Starts the gRPC server and binds it to a specified host and port from the configuration.

    Parameters:
        server (grpc.Server): The gRPC server to start.
        config (ServerConfig): Configuration object containing the host and port.
    """

    print("Server has started and is bound to the following:")
    for key, value in vars(config).items():
        print(f"{key.capitalize()}: {value}")

    try:
        server.add_insecure_port(f"{config.host}:{config.port}")
        server.start()
        server.wait_for_termination()
    except Exception as e:
        print(f"An error occurred while starting server: {e}")


if __name__ == "__main__":
    config = parse_args()
    server = create_server()
    register_services(server)
    start_server(server, config)
