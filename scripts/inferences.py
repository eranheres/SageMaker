import argparse
from sagemaker.predictor import RealTimePredictor
from sagemaker.content_types import CONTENT_TYPE_CSV
from sagemaker.session import Session


def file_data(file_name):
    with open(file_name, 'rb') as image:
        f = image.read()
        b = bytearray(f)
        ne = open('n.txt', 'wb')
        ne.write(b)
    return b


def predictor(content_type, endpoint_name):
    endpoint_name = endpoint_name 
    sess = Session()
    return RealTimePredictor(
            endpoint=endpoint_name, 
            sagemaker_session=sess,
            content_type=content_type, 
            accept=CONTENT_TYPE_CSV)


def predict(predictor, file_name):
    data = file_data(file_name)
    return predictor.predict(data)


def main():
    parser = argparse.ArgumentParser(description="inference an image")
    parser.add_argument('file_name', metavar='filename', type=str,
                        help='the filename to inferece')
    parser.add_argument('end_point', metavar='endpoint', type=str,
                        help='the model endpoint name')
    parser.add_argument('-d', dest='data_type', type=str, default='image/png',
                        help='the MIME data type')
    args = parser.parse_args()
    p = predictor(args.data_type, args.end_point)
    v = predict(p, args.file_name)
    print (v)
  
if __name__ == "__main__":
    main()
