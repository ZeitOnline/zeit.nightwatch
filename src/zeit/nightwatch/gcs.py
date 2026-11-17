import mimetypes
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
    # Without a content type GCS stores application/octet-stream: browsers
    # download the report instead of rendering it, and tools that read objects
    # as text refuse it. For compressed files guess_type names the inner type
    # (.tar.gz -> application/x-tar), so those keep the default.
    content_type, encoding = mimetypes.guess_type(target)
    with open(source, "rb") as f:
        blob.upload_from_file(
            f, size=os.stat(source).st_size, content_type=None if encoding else content_type
        )
