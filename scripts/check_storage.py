"""Exercise actual S3 upload/download; keep credentials out of evidence."""
import hashlib
import boto3
from botocore.exceptions import ClientError
from botocore.config import Config
from lab import config, ROOT, save, result
from progress import set_status

cfg = config()
client = boto3.client("s3", endpoint_url="http://localhost:9000",
    aws_access_key_id=cfg["MINIO_ROOT_USER"], aws_secret_access_key=cfg["MINIO_ROOT_PASSWORD"],
    region_name="us-east-1", config=Config(signature_version="s3v4", s3={"addressing_style": "path"}))
try:
    client.head_bucket(Bucket="demo")
except ClientError as error:
    if error.response["Error"]["Code"] != "404":
        raise
    client.create_bucket(Bucket="demo")
source = (ROOT / "web-frontend-server/html/index.html").read_bytes()
client.put_object(Bucket="demo", Key="index.html", Body=source, ContentType="text/html; charset=utf-8")
download = client.get_object(Bucket="demo", Key="index.html")["Body"].read()
assert download == source
objects = client.list_objects_v2(Bucket="demo")["Contents"]
evidence = save("R06-storage.json", result("R06", {
    "bucket": "demo", "key": "index.html", "uploaded_bytes": len(source),
    "downloaded_bytes": len(download), "sha256": hashlib.sha256(download).hexdigest(),
    "bytes_match": True, "objects": [item["Key"] for item in objects],
}))
set_status("R06", "DAT", evidence + "; upload/download byte-for-byte; Console screenshot later")
print("PASS: S3 bucket/upload/download and checksum match; " + evidence)
