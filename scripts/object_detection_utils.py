import boto3
import json 
from urlparse import urlparse
from StringIO import StringIO

s3_resource = boto3.resource('s3')
s3_client   = boto3.client('s3')

def read_s3_file(bucket, key):
    obj = s3_resource.Object(bucket, key)
    return obj.get()['Body'].read().decode('utf-8') 

def write_s3_file(data_str, bucket, key):
    print('writing file data to ==> ' + key)
    handle = StringIO(data_str)
    s3_client.put_object(Bucket=bucket, Key=key, Body=handle.read())

def copy_s3_file(bucket, from_key, to_folder):
    copy_source = {'Bucket': bucket, 'Key': from_key[1:] }
    to = to_folder[1:] + '/' + from_key.split('/')[-1]
    print('copy: '+from_key+' ==> '+to)
    s3_resource.Object(bucket, to).copy(copy_source)
        
def convert_augmented_format_to_json_format(augmented, attribute_name):
    out = {}
    out['file'] = augmented['source-ref'].split('/')[-1]
    out['image_size'] = augmented[attribute_name]['image_size']
    if augmented[attribute_name]['annotations']:
        out['annotations'] = augmented[attribute_name]['annotations']
    else:
        out['annotations'] = []
    if augmented[attribute_name+'-metadata']['class-map'] and augmented[attribute_name+'-metadata']['class-map']['0']:
        out['categories'] = [{'class_id': 0, 'name': augmented[attribute_name+'-metadata']['class-map']['0']}]
    else:
        out['categories'] = []
    return out
        
def convert_augmented_samples_to_files_samples(attribute_name, bucket, augmented_manifest, output_prefix):
    images_folder = output_prefix + '/images'
    annotations_folder = output_prefix + '/annotations'
    augmented = [json.loads(x) for x in read_s3_file(bucket, augmented_manifest).split('\n') if len(x)!=0]
    for aug in augmented:
        image_link = urlparse(aug['source-ref'])
        copy_s3_file(image_link.netloc, image_link.path, images_folder)
        json_annotation_file = convert_augmented_format_to_json_format(aug, attribute_name)
        annotation_key = annotations_folder[1:] + '/' + '.'.join(image_link.path.split('/')[-1].split('.')[:-1]) + '.json' 
        d = json.dumps(json_annotation_file)
        write_s3_file(d, bucket, annotation_key) 
    print (len(augmented))
   