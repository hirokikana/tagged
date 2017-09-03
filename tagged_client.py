import grpc

import tagged_pb2
import tagged_pb2_grpc

def run():
    channel = grpc.insecure_channel('localhost:50051')
    stub = tagged_pb2_grpc.TaggedStub(channel)
    tag = tagged_pb2.Tag(name='テスfhsdafsafsa')
    content = tagged_pb2.Content(path='keykey')
    response = stub.Add(tagged_pb2.AddRequest(tag=tag,content=content))
    print(response)

    response = stub.GetGivenedTag(tagged_pb2.Content(path='keykey'))
    print(response.tags)

if __name__ == '__main__':
    run()
    
