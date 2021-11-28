# gRPC Image Rotation Service

## Description

You've been given a protobuf definition file that defines an image rotation and mean filter [gRPC](https://grpc.io/)
interface. Your task is to create a server that implements this interface, and a client to test it.

Time permitting, implement the server as if it will operate in a production environment and be subsequently used and
worked on by a team of engineers. If you make compromises to keep your solution simple and timely, please be sure to
bring them up in the discussion part of your deliverables.

Your submission should assume we'll test by starting with a fresh Ubuntu 18.04 or Mac OS install (please let us know
which one). You should provide a script for us to run that will carry out any system setup (named `setup`),
and a build script (named `build`) that will execute any build steps needed by your solution. These should be located
in the top level directory of your submission. Please do not include build artifacts or generated code in your submission.

We will test your client and server together by giving the client a series of valid png and jpeg images. We'll test
your server on its own with a series of `NLImage` that are guaranteed to be valid protobuf messages, but whose
contents are not guaranteed correct (aka: the data within the valid protobuf message may not represent a valid image).

Your client (in the top level directory, named `client`) should provide an `--input` argument that specifies the location
of a jpeg or png, and an `--output` argument that specifies the path of the output image. It should also provide two
arguments that specify which endpoints to call on the input image to create the output image. `--rotate` which takes as
argument the text form of the rotation enum (EG: `NINETY_DEG`), and `--mean` which specifies that the mean filter should be
run on the input image. You don't need to support multiple of each individual argument, but should allow specifying both
`--rotate` and `--mean` at the same time. AKA: No need to allow multiple rotations or repeated applications of the mean
filter, but must allow a rotation and mean simultaneously. The client should also have `--port` and `--host` arguments
that specify the host and port of the server.

Your server (in the top level directory, named `server`) should provide a `--port` and `--host` which specify the
port and host the server will bind to.

You can use any [officially supported gRPC language](https://grpc.io/docs/).

## Deliverables

There are 4 deliverables that should come in the form of this git repository zipped and sent to us:

1. Specification of whether your solution requires a clean install of Ubuntu 18.04 or Mac OS.
2. A script, named `setup`, that installs any dependencies and sets up the system for your submission. It should be in the
   top level directory and be runnable via `./setup`.
3. A script, named `build`, that carries out any build steps your solution requires. It should be in the top level directory
   and runnable via `./build`.
4. A `gRPC` server that implements the `NLImageService` interface, provides `--port` and `--host` and
   is runnable via `./server --port <...> --host <...>` in the top level directory of your submission (it's okay
   if the `./server` executable just wraps a build artifact)
5. A client that provides `--port`, `--host`, `--input`, `--output`, `--rotate`, and `--mean` arguments and can be
   run from the top level directory of your submission via
   `./client --port <...> --host <...> --input <...> --output <...> --rotate <...> --mean` (it's okay if the `./client`
   executable just wraps a build artifact)
6. Discussion of limitations or known issues with your solution, how you'd change it for production given more time and
   resources, and any other thoughts you have about the problem, your solution, or the tools you used.
   w
