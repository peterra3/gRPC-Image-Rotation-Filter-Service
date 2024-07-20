import grpc
import src.proto.image_pb2 as image_pb2
import src.proto.image_pb2_grpc as image_pb2_grpc
from PIL import Image, ImageFilter
import io


def open_and_verify_image(data: bytes) -> Image:
    """
    Opens an image from byte data and verifies its integrity.

    Parameters:
        data (bytes): The image data as a byte stream.

    Returns:
        PIL.Image.Image: An image object ready for processing if the verification is successful.

    Raises:
        IOError: If the image cannot be opened or verified, indicating the data might be corrupted.
    """

    image_stream = io.BytesIO(data)
    img = Image.open(image_stream)
    img.verify()  # Ensure the image can be opened
    image_stream.seek(0)  # Reset the stream after verification
    return Image.open(image_stream)


class NLImageServiceServicer(image_pb2_grpc.NLImageServiceServicer):
    """
    Provides implementations for the gRPC services defined in the protobuf.
    """

    def RotateImage(
        self, request: image_pb2.NLImageRotateRequest, context: grpc.ServicerContext
    ) -> image_pb2.NLImage:
        """
        Rotates an image based on the rotation degree specified in the request.

        Parameters:
            request (image_pb2.NLImageRotateRequest): Request containing image data and rotation specification.
            context (grpc.ServicerContext): Context of the gRPC call.

        Returns:
            NLImage: A new image that has been rotated as specified.
        """

        try:
            img = open_and_verify_image(request.image.data)

            # Perform rotation based on the enum
            rotation_degrees = {
                image_pb2.NLImageRotateRequest.NINETY_DEG: 90,
                image_pb2.NLImageRotateRequest.ONE_EIGHTY_DEG: 180,
                image_pb2.NLImageRotateRequest.TWO_SEVENTY_DEG: 270,
            }.get(
                request.rotation, 0
            )  # Default to 0 if no valid rotation specified

            rotated_img = img.rotate(rotation_degrees, expand=True)
            width, height = rotated_img.size

            # Save the rotated image back to bytes
            byte_arr = io.BytesIO()
            rotated_img.save(byte_arr, format="PNG")
            rotated_bytes = byte_arr.getvalue()

            return image_pb2.NLImage(
                color=request.image.color,
                data=rotated_bytes,
                width=width,
                height=height,
            )

        except IOError as e:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details(f"Invalid image data: {str(e)}")
            return image_pb2.NLImage()

        except Exception as e:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details(f"Failed to process image: {str(e)}")
            return image_pb2.NLImage()

    def MeanFilter(self, nl_image: image_pb2.NLImage, context) -> image_pb2.NLImage:
        """
        Applies a mean filter to an image to average out pixel values. The mean filter can be computed for each pixel in an image by
        taking the average of a pixel and all of its neighbors.

        Parameters:
            nl_image (image_pb2.NLImage): An NLImage protobuf message containing the image data.
            context (grpc.ServicerContext): Context of the gRPC call.

        Returns:
            NLImage: An image that has had a mean filter applied.
        """

        try:
            img = open_and_verify_image(nl_image.data)

            # Apply the mean filter
            filtered_img = img.filter(ImageFilter.BoxBlur(1))

            width, height = filtered_img.size

            # Save the filtered image back to bytes
            byte_arr = io.BytesIO()
            filtered_img.save(byte_arr, format="PNG")
            filtered_bytes = byte_arr.getvalue()

            return image_pb2.NLImage(
                color=nl_image.color,
                data=filtered_bytes,
                width=width,
                height=height,
            )

        except IOError as e:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details(f"Invalid image data: {str(e)}")
            return image_pb2.NLImage()

        except Exception as e:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details(f"Failed to process image: {str(e)}")
            return image_pb2.NLImage()
