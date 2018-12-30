from sagemaker.predictor import RealTimePredictor
from sagemaker.content_types import CONTENT_TYPE_CSV
from sagemaker.session import Session

def file_data(file_name):
    with open(file_name, 'rb') as image:
        f = image.read()
        b = bytearray(f)
        ne = open('n.txt','wb')
        ne.write(b)
    return b

def predictor(content_type, endpoint_name):
    endpoint_name = endpoint_name 
    sess = Session()
    return RealTimePredictor(endpoint=endpoint_name, sagemaker_session=sess,content_type=content_type, accept=CONTENT_TYPE_CSV)

def predict(predictor, file_name):
    data = file_data(file_name)
    ret = predictor.predict(data)
    print (ret)
    
    
p = predictor('image/png', 'xbutton-endpoint-1')
predict(p, '2.11-18.34.6.png')