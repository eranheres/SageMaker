import json
import tempfile
import argparse
import boto3
from urlparse import urlparse
import os

from inferences import predict, predictor


def visualize_detection(img_file, dets, classes=[], thresh=0.95):
    """
    visualize detections in one image
    Parameters:
    ----------
    img : numpy.array
        image, in bgr format
    dets : numpy.array
        ssd detections, numpy.array([[id, score, x1, y1, x2, y2]...])
        each row is one object
    classes : tuple or list of str
        class names
    thresh : float
        score threshold
    """
    import random as rnd
    import matplotlib.pyplot as plt
    import matplotlib.image as mpimg

    img = mpimg.imread(img_file)
    plt.imshow(img)
    height = img.shape[0]
    width = img.shape[1]
    colors = dict()
    for det in dets:
        (klass, score, x0, y0, x1, y1) = det
        if score < thresh:
            continue
        cls_id = int(klass)
        if cls_id not in colors:
            colors[cls_id] = (rnd.random(), rnd.random(), rnd.random())
        xmin = int(x0 * width)
        ymin = int(y0 * height)
        xmax = int(x1 * width)
        ymax = int(y1 * height)
        rect = plt.Rectangle((xmin, ymin), xmax - xmin,
                             ymax - ymin, fill=False,
                             edgecolor=colors[cls_id],
                             linewidth=3.5)
        plt.gca().add_patch(rect)
        class_name = str(cls_id)
        if classes and len(classes) > cls_id:
            class_name = classes[cls_id]
        plt.gca().text(xmin, ymin - 2,
                       '{:s} {:.3f}'.format(class_name, score),
                       bbox=dict(facecolor=colors[cls_id], alpha=0.5),
                       fontsize=12, color='white')
    plt.show()
    # plt.savefig('predicted-' + img_file)


images_folder = 'projects/object_detection/input/xbutton/test'
bucket = 'com.tabtale.dev.eran'
s3_resource = boto3.resource('s3')
s3_client = boto3.client('s3')


def plot_for_local_file(image_filename, endpoint, mime_type):
    object_categories = ['xbutton']
    threshold = 0.80
    p = predictor(mime_type, endpoint)
    res = predict(p, image_filename)
    detections = json.loads(res)
    visualize_detection(image_filename,
                        detections['prediction'],
                        object_categories,
                        threshold)


def plot_for_s3_file(path, endpoint, mime_type):
    u = urlparse(path)
    bucket = u.netloc
    image_key = u.path[1:]
    image_file_name = image_key.split('/')[-1]
    print("path==>",path)
    print("bucket ==>"+bucket)
    print("image_key ==>"+image_key)
    object = s3_resource.Bucket(bucket).Object(image_key)
    tmp = tempfile.NamedTemporaryFile()
    print(path + ' ==> ' + image_file_name)
    with open(tmp.name, 'wb') as f:
        object.download_fileobj(f)
        f.flush()
        plot_for_local_file(tmp.name, endpoint, mime_type)


def plot_for_s3_folder(bucket, images_folder, endpoint, mime_type):
    res = s3_client.list_objects_v2(Bucket=bucket, Prefix=images_folder)
    for x in res.get('Contents', []):
        image_key = x['Key']
        image_file_name = image_key.split('/')[-1]
        object = s3_resource.Bucket(bucket).Object(image_key)
        tmp = tempfile.NamedTemporaryFile()
        print(x['Key'] + ' ==> ' + image_file_name)
        with open(tmp.name, 'wb') as f:
            object.download_fileobj(f)
            f.flush()
            plot_for_local_file(tmp.name, endpoint, mime_type)


def main():
    parser = argparse.ArgumentParser(description="inference and plot an image")
    parser.add_argument('file_name', metavar='filename', type=str,
                        help='the filename to inferece or path to S3 folder')
    parser.add_argument('end_point', metavar='endpoint', type=str,
                        help='the model endpoint name')
    parser.add_argument('-d', dest='mime_type', type=str, default='image/png',
                        help='the MIME data type')
    args = parser.parse_args()
    u = urlparse(args.file_name)
    basename = os.path.basename(u.path)
    if u.scheme == 's3':
        plot_for_s3_file(args.file_name, args.end_point, args.mime_type)
    else:
        plot_for_local_file(u.path,
                            args.end_point,
                            args.mime_type)

    # p = predictor(args.data_type, args.end_point)
    # v = predict(p, args.file_name)
    # print(v)


if __name__ == "__main__":
    main()
