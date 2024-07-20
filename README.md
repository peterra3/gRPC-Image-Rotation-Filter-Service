# gRPC Image Rotation Filter Service


## Overview

This codebase is designed to create a gRPC server that implements an image rotation and mean filter interface as defined in a provided protobuf definition file. The server is robust enough for potential production use. Additionally, a client is included to test the server's functionality. Both the client and server will handle valid PNG and JPEG images, with the client supplying specific arguments for image manipulation.

### Table of Content
- [gRPC Image Rotation Service](#grpc-image-rotation-service)
  - [Overview](#overview)
    - [Table of Content](#table-of-content)
    - [Built With](#built-with)
  - [Requirements](#requirements)
  - [Getting Started](#getting-started)
    - [Setup](#setup)
    - [Running the Server](#running-the-server)
    - [Running the Client](#running-the-client)
  - [Discussion of Limitations and Known Issues](#discussion-of-limitations-and-known-issues)
    - [Current Limitations](#current-limitations)
    - [Known Issues](#known-issues)
    - [Proposed Enhancements for Production](#proposed-enhancements-for-production)
    - [Conclusion](#conclusion)
  
### Built With


* [![Python][Python]][Python-url]
* [![gRPC][gRPC]][gRPC-url]


## Requirements
This solution is designed to run on a clean installation of **Ubuntu 22.04**. Ensure that your system meets this requirement before proceeding.

## Getting Started
Follow these step-by-step instructions to get a development environment up and running.

### Setup

1. **Make Scripts Executable:**
   Ensure that all necessary bash scripts are executable. Run the following command in your terminal:

    ```bash
    chmod +x build.sh setup.sh server.sh client.sh
    ```

2. **Environment Setup:**
   Navigate to the project root directory and execute the setup and build scripts to prepare your environment:

    ```bash
    ./setup.sh  # Sets up the environment
    ./build.sh  # Builds the project
    ```

### Running the Server

To start the server, use the following command syntax:

```bash
./server.sh --port <PORT> --host <HOST>
```

**Example:**

```bash
./server.sh --port 77834 --host localhost
```

### Running the Client

You can run the client using the syntax below (separate terminal). This allows you to specify the server details, input and output image paths, the rotation angle (NONE, NINETY_DEG, ONE_EIGHTY_DEG, TWO_SEVENTY_DEG), and whether to apply a mean filter.

```bash
./client.sh --port <PORT> --host <HOST> --input <PATH_TO_INPUT_IMAGE> --output <PATH_TO_OUTPUT_IMAGE> --rotate <ROTATION> --mean
```

**Example:**

```bash
./client.sh --port 77834 --host localhost --input colored.jpg --output output.jpg --rotate NINETY_DEG --mean
```

## Discussion of Limitations and Known Issues

### Current Limitations
1. **Error Handling**: The error handling mechanisms need to be enhanced to gracefully manage and log exceptions that may occur during image processing or network communication.

2. **Security**: The implementation currently lacks comprehensive security measures such as TLS/SSL encryption, which are crucial for protecting data transmitted over networks.

3. **Scalability**: The server setup is basic and may not efficiently handle high traffic volumes or concurrent requests. Scaling the service to handle larger loads effectively is necessary for production deployment.

4. **Testing**: The project requires a thorough testing framework covering unit, integration, and end-to-end testing to ensure reliability and robustness.

5. **Image Processing Capabilities**: The service is currently limited to basic image rotations and mean filtering. Expanding capabilities to include more complex image processing functions could enhance utility.

6. **Format Support**: The service might currently support a limited number of image formats. Extending support to a wider array of formats would make the service more versatile.

### Known Issues
- The service might experience downtime or performance degradation under load due to the lack of optimized concurrency management.

### Proposed Enhancements for Production

1. **Enhanced Security**: Implement TLS/SSL encryption for all gRPC communications to ensure data integrity and confidentiality.

2. **Improved Error Handling and Logging**: 
   - Develop a comprehensive error handling strategy that includes detailed logging for errors and exceptions. This would help in diagnosing issues quickly and efficiently.
   - Enhance logging capabilities to provide insights into the system's operation and performance, which is invaluable for monitoring and troubleshooting.

3. **Scalability Improvements**:
   - Optimize the server's architecture to manage multiple simultaneous connections and requests using advanced concurrency patterns.
   - Consider containerization (e.g., Docker) and orchestration (e.g., Kubernetes) for easier deployment and scalability.

4. **Extended Image Processing Features**:
   - Integrate advanced image processing libraries like OpenCV to provide more functionalities such as advanced filters, color adjustments, and geometric transformations.

5. **Comprehensive Testing**: Establish a complete suite of automated tests to ensure each component functions correctly individually and when integrated, thereby reducing bugs and regressions.

6. **Performance Optimization**: 
   - Profile the application to identify bottlenecks.
   - Optimize critical sections of the code, especially those involved in image handling, to improve overall performance.

7. **Documentation and Maintenance**:
   - Ensure that all features and modules are well-documented to facilitate easy maintenance and future enhancements.
   - Adopt coding standards and perform regular code reviews to maintain code quality.
  
8. **Virtual Environment Management**: Utilize virtual environments to isolate and manage dependencies specifically for this application, ensuring that it does not conflict with other Python packages installed on the host system.

### Conclusion
By addressing these limitations and implementing the suggested enhancements, the gRPC Image Rotation Service can be significantly improved to handle production loads efficiently, securely, and reliably. 











<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->

[python-url]: https://www.python.org/
[python]: https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54
[grpc]: https://img.shields.io/badge/powered_by-gRPC-green?labelColor=red
[grpc-url]: https://grpc.io/
