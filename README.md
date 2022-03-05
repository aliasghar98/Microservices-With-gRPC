# Microservices-With-gRPC
Implementing python microservices using Google Remote Procedure Call framework.

Instructions:

1. Navigate to recommendations folder and run "python3 recommendations.py" on one terminal to run Recommendations microservice since it acts as server for Catalog microservice.

2. Navigate to catalog folder and run "FLASK_APP=catalog.py flask run" one another terminal to run Catalog microservice Web Application. 

3. Open "localhost:5000".



In case of any changes to recommendations.proto file:

1. Navigate to protobufs folder and run command:
"python3 -m grpc_tools.protoc -I ../protobufs --python_out=. --grpc_python_out=. ../protobufs/recommendations.proto"

This will build python files corresponding to protobuf files.

2. Navigate to recommendations folder and run command:
"python3 -m grpc_tools.protoc -I ../protobufs --python_out=. --grpc_python_out=. ../protobufs/recommendations.proto"

3. Navigate to catalog folder and run command:
"python3 -m grpc_tools.protoc -I ../protobufs --python_out=. --grpc_python_out=. ../protobufs/recommendations.proto"

