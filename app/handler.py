"""Signed Upload - return an S3 presigned PUT URL for a private bucket."""
import json
import os

BUCKET = os.environ.get("UPLOAD_BUCKET", "")
EXPIRES = int(os.environ.get("PRESIGN_EXPIRES", "300"))
APP_VERSION = os.environ.get("APP_VERSION", "dev")

_client = None


def s3():
    global _client
    if _client is None:
        import boto3
        _client = boto3.client("s3")
    return _client


def response(status, body):
    return {
        "statusCode": status,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body),
    }


def lambda_handler(event, context):
    if isinstance(event.get("body"), str):
        try:
            body = json.loads(event["body"] or "{}")
        except json.JSONDecodeError:
            body = {}
    else:
        body = event if isinstance(event, dict) else {}

    key = str(body.get("key") or "").lstrip("/")
    content_type = str(body.get("content_type") or "application/octet-stream")
    if not key or ".." in key or key.startswith("/"):
        return response(400, {"error": "invalid key"})
    if not BUCKET:
        return response(500, {"error": "UPLOAD_BUCKET not set"})

    expires = max(1, min(EXPIRES, 300))
    url = s3().generate_presigned_url(
        ClientMethod="put_object",
        Params={"Bucket": BUCKET, "Key": key, "ContentType": content_type},
        ExpiresIn=expires,
    )
    return response(200, {
        "upload_url": url,
        "bucket": BUCKET,
        "key": key,
        "expires_in": expires,
        "version": APP_VERSION,
    })
