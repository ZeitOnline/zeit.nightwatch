import os
import sys

from google.cloud import storage


def upload():
    if len(sys.argv) < 3:
        sys.stderr.write("Usage: gcs-upload filename gs://bucket/path/target")
        sys.exit(1)
    if len(sys.argv) >= 4:
        project = sys.argv[3]
    else:
        project = "zeitonline-engineering"  # default for nightwatch-zeit-de

    source = sys.argv[1]
    target = sys.argv[2].replace("gs://", "", 1)
    bucket, target = target.split("/", 1)

    bucket = storage.Client(project=project).bucket(bucket)
    blob = bucket.blob(target)
    with open(source, "rb") as f:
        blob.upload_from_file(f, size=os.stat(source).st_size)
