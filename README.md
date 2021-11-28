# Deliverables

1. Clean install of Ubuntu 18.04
2. See `setup` file in top level directory
3. See `build` file in top level directory
4. See `server.py` for server implementation and `server` script for execution
5. See `client.py` for client implementation and `client` script for execution
6. See `Discussion` below

# Discussion

- Hot reload for gRPC services so you can update server code without re-running the gRPC server
- Deprecate usage of Pillow in client.py to consolidate image processing with only pen-CV library. Currently, Pillow is being relied on for detecting whether
  an image is grayscale/RGB in a clean fashion, containing images in memory to pass its data via RPCs

# NOTES (for myself)

## Compile protos

`python3 -m grpc_tools.protoc -I proto/ --python_out=. --grpc_python_out=. proto/image.proto`

## Usage

#### Client

`./client --input <input> --output <output> [--rotate {NONE | NINETY_DEG | ONE_EIGHTY_DEG | TWO_SEVENTY_DEG}] [--mean] --host <host> --port <port>`

#### Server

`./server --host <host> --port <port>`

## Example (for easy copy-paste :D)

(in separate terminals)

### Client

`./client --input ./assets/AM04NES.jpeg --output ./image.png --rotate NINETY_DEG --mean --host localhost --port 50052`

### Server

`./server --host localhost --port 50052`

saves a 90 degree rotated mean image at `image.png`
