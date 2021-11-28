#!/usr/bin/python3
from concurrent import futures
import grpc
import argparse
import logging
import cv2
import numpy as np

import image_pb2_grpc
from image_pb2 import (
    NLImage,
    NLImageRotateRequest,
)

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class NLImageService(image_pb2_grpc.NLImageServiceServicer):
    def RotateImage(self, request, context):
        if request.rotation == NLImageRotateRequest.Rotation.NONE:
            return request.image

        ROTATIONS = {
            NLImageRotateRequest.Rotation.NINETY_DEG : cv2.ROTATE_90_COUNTERCLOCKWISE,
            NLImageRotateRequest.Rotation.ONE_EIGHTY_DEG : cv2.ROTATE_180,
            NLImageRotateRequest.Rotation.TWO_SEVENTY_DEG : cv2.ROTATE_90_CLOCKWISE,
        }

        # NOTE: np.uint8 won't support images w/ 10-bit color channels
        image_bytes_nparr = np.frombuffer(request.image.data, np.uint8)
        image_cv2 = cv2.imdecode(image_bytes_nparr, cv2.IMREAD_COLOR if 
            request.image.color else cv2.IMREAD_GRAYSCALE)

        # reference: https://avi.im/grpc-errors/#python
        if image_cv2.size == 0:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT,
                "Image data buffer is too short or contains invalid data")
        rotated_image = cv2.rotate(image_cv2, ROTATIONS[request.rotation])

        if request.rotation == NLImageRotateRequest.Rotation.ONE_EIGHTY_DEG:
            rotated_image_width = request.image.width
            rotated_image_height = request.image.height
        else:
            rotated_image_width = request.image.height
            rotated_image_height = request.image.width

        return NLImage(
            color = request.image.color,
            width = rotated_image_width,
            height = rotated_image_height,
            data = cv2.imencode(".PNG", rotated_image)[1].tobytes()
        )
    
    def MeanFilter(self, nl_image, context):
        # IDEA: make this a parameter in request proto to customize blur level
        # recommend changing to (15,15) to get noticeable blurring;
        KERNEL_SIZE = (3,3)

        image_bytes_nparr = np.frombuffer(nl_image.data, np.uint8)
        image_cv2 = cv2.imdecode(image_bytes_nparr, cv2.IMREAD_COLOR if 
            nl_image.color else cv2.IMREAD_GRAYSCALE)

        # reference: https://avi.im/grpc-errors/#python
        if image_cv2.size == 0:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT,
                "Image data buffer is too short or contains invalid data")
        mean_image = cv2.blur(image_cv2,KERNEL_SIZE)

        return NLImage(
            color = nl_image.color,
            width = nl_image.width,
            height = nl_image.height,
            data = cv2.imencode(".PNG", mean_image)[1].tobytes(),
        )
    

def serve(host, port):
    # for sake of this project, only one thread is needed 
    # for this server since there's only one client, 
    # but with multiple clients I would scale
    # this up, especially if requests contain large images
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    image_pb2_grpc.add_NLImageServiceServicer_to_server(
        NLImageService(), server
    )
    server.add_insecure_port(f"{host}:{port}")
    server.start()
    logger.info(f"Serving at {host}:{port}")
    server.wait_for_termination()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Configure host and port for server")
    parser.add_argument("--host",type=str,required=True)
    parser.add_argument("--port",type=int,required=True)

    args = parser.parse_args()
    serve(args.host, args.port)