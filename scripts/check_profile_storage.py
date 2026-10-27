"""Implement and verify E05: MinIO public avatar and coursework documents."""
import hashlib
import json
from pathlib import Path
import boto3
from botocore.config import Config
from botocore.exceptions import ClientError
import requests
from playwright.sync_api import sync_playwright

from browser import launch
from lab import ROOT, EVIDENCE, config, save, result
from progress import set_status

cfg = config()
s3_endpoint = "http://localhost:9000"
client = boto3.client(
    "s3",
    endpoint_url=s3_endpoint,
    aws_access_key_id=cfg["MINIO_ROOT_USER"],
    aws_secret_access_key=cfg["MINIO_ROOT_PASSWORD"],
    region_name="us-east-1",
    config=Config(signature_version="s3v4", s3={"addressing_style": "path"})
)

def ensure_bucket(name):
    try:
        client.head_bucket(Bucket=name)
    except ClientError as e:
        if e.response["Error"]["Code"] in ("404", "NoSuchBucket"):
            client.create_bucket(Bucket=name)
        else:
            raise

ensure_bucket("profile-pics")
ensure_bucket("documents")

# Set public-read policy on profile-pics
public_policy = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "PublicReadProfilePics",
            "Effect": "Allow",
            "Principal": "*",
            "Action": ["s3:GetObject"],
            "Resource": ["arn:aws:s3:::profile-pics/*"]
        }
    ]
}
client.put_bucket_policy(Bucket="profile-pics", Policy=json.dumps(public_policy))

avatar_source = ROOT / "object-storage-server/avatar.jpg"
assert avatar_source.exists(), "avatar.jpg must exist in object-storage-server"
avatar_bytes = avatar_source.read_bytes()
avatar_hash = hashlib.sha256(avatar_bytes).hexdigest()

client.put_object(
    Bucket="profile-pics",
    Key="avatar.jpg",
    Body=avatar_bytes,
    ContentType="image/jpeg"
)

# Upload coursework report PDF to documents
report_source = ROOT / "report/BaoCao_Local_521H0092.pdf"
assert report_source.exists(), "Coursework PDF must exist"
report_bytes = report_source.read_bytes()
report_hash = hashlib.sha256(report_bytes).hexdigest()

client.put_object(
    Bucket="documents",
    Key="BaoCao_Local_521H0092.pdf",
    Body=report_bytes,
    ContentType="application/pdf"
)

# 1. Anonymous test: avatar must be publicly accessible via GET
avatar_url = f"{s3_endpoint}/profile-pics/avatar.jpg"
anon_resp = requests.get(avatar_url, timeout=10)
assert anon_resp.status_code == 200, f"Expected 200 for public avatar, got {anon_resp.status_code}"
assert anon_resp.content == avatar_bytes, "Downloaded avatar does not match source bytes"

# 2. Documents must be private: anonymous GET should return 403 Forbidden
doc_url = f"{s3_endpoint}/documents/BaoCao_Local_521H0092.pdf"
doc_anon_resp = requests.get(doc_url, timeout=10)
assert doc_anon_resp.status_code == 403, f"Expected 403 for private document, got {doc_anon_resp.status_code}"

# 3. Authenticated retrieval of document via S3 client
doc_obj = client.get_object(Bucket="documents", Key="BaoCao_Local_521H0092.pdf")
downloaded_doc_bytes = doc_obj["Body"].read()
assert hashlib.sha256(downloaded_doc_bytes).hexdigest() == report_hash

# 4. Browser captures of MinIO Console
EVIDENCE.mkdir(parents=True, exist_ok=True)
with sync_playwright() as p:
    browser = launch(p)
    page = browser.new_page(viewport={"width": 1440, "height": 1000})
    page.goto("http://localhost:9001/")
    page.locator("#accessKey").fill(cfg["MINIO_ROOT_USER"])
    page.locator("#secretKey").fill(cfg["MINIO_ROOT_PASSWORD"])
    page.get_by_role("button", name="Login", exact=True).click()
    page.get_by_text("profile-pics", exact=True).first.wait_for(timeout=30000)
    page.screenshot(path=str(EVIDENCE / "E05-minio-buckets.png"), full_page=True)
    page.get_by_text("profile-pics", exact=True).first.click()
    page.get_by_text("avatar.jpg", exact=True).first.wait_for(timeout=30000)
    page.screenshot(path=str(EVIDENCE / "E05-minio-avatar.png"), full_page=True)
    browser.close()

details = {
    "profile_pics": {
        "bucket": "profile-pics",
        "key": "avatar.jpg",
        "public_url": avatar_url,
        "anonymous_status": anon_resp.status_code,
        "content_type": anon_resp.headers.get("content-type"),
        "sha256": avatar_hash,
        "bytes": len(avatar_bytes)
    },
    "documents": {
        "bucket": "documents",
        "key": "BaoCao_Local_521H0092.pdf",
        "anonymous_status": doc_anon_resp.status_code,
        "sha256": report_hash,
        "bytes": len(report_bytes)
    }
}

path = save("E05-storage.json", result("E05", details))
set_status("E05", "DAT", f"{path}; feat/profile-object-storage; python scripts/check_profile_storage.py; E05-minio-avatar.png")
print("PASS E05: profile-pics/avatar.jpg is public (200), documents/BaoCao_Local_521H0092.pdf is private (403), console screenshots captured.")
