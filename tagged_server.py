import grpc
from concurrent import futures
import time

import shelve

import tagged_pb2
import tagged_pb2_grpc

class Tagged(tagged_pb2_grpc.TaggedServicer):
    def Add(self, request, context):
        storage = shelve.open('./tagged_storage')
        if request.content.path in storage.keys() and storage[request.content.path].__class__ == list:
            current = storage[request.content.path]
            current.append(request.tag.name)
            storage[request.content.path] = current
        else:
            storage[request.content.path] = [request.tag.name]
        storage.close()
        return tagged_pb2.AddReply(result=True)

    def GetGivenedTag(self, request, context):
        reply = tagged_pb2.GetGivenedTagReply()

        storage = shelve.open('./tagged_storage')
        tags = storage[request.path]
        for tag in tags:
            reply.tags.add().name = tag
        
        return reply

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    tagged_pb2_grpc.add_TaggedServicer_to_server(Tagged(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    try:
        while True:
            time.sleep(1000)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()
