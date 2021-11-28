# Deliverables


- See `setup` file in top level directory for setup script
- See `build` file in top level directory for build script
- See `server.py` for server implementation and `server` script for execution
- See `client.py` for client implementation and `client` script for execution
- See `Discussion` below

# Discussion

- Hot reload for gRPC services so you can update server code without re-running the gRPC server
- Deprecate usage of Pillow in client.py to consolidate image processing with only pen-CV library. Currently, Pillow is being relied on for detecting whether
  an image is grayscale/RGB in a clean fashion, containing images in memory to pass its data via RPCs


## Usage

### Compile protos

`python3 -m grpc_tools.protoc -I proto/ --python_out=. --grpc_python_out=. proto/image.proto`

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
