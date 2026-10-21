import json
import os
import unittest
from unittest import mock

os.environ["UPLOAD_BUCKET"] = "h3-p01-uploads"
os.environ["PRESIGN_EXPIRES"] = "120"
os.environ["APP_VERSION"] = "v1"

import handler  # noqa: E402


class UploadTests(unittest.TestCase):
    def test_presign_success(self):
        with mock.patch.object(handler, "s3") as s3:
            s3.return_value.generate_presigned_url.return_value = "https://example.com/put"
            res = handler.lambda_handler({"key": "inbox/a.txt", "content_type": "text/plain"}, None)
        self.assertEqual(res["statusCode"], 200)
        body = json.loads(res["body"])
        self.assertEqual(body["expires_in"], 120)
        self.assertTrue(body["upload_url"].startswith("https://"))
        self.assertEqual(body["version"], "v1")

    def test_rejects_bad_key(self):
        res = handler.lambda_handler({"key": "../etc/passwd"}, None)
        self.assertEqual(res["statusCode"], 400)

    def test_caps_expiry_at_300(self):
        old = handler.EXPIRES
        handler.EXPIRES = 999
        try:
            with mock.patch.object(handler, "s3") as s3:
                s3.return_value.generate_presigned_url.return_value = "https://example.com/put"
                res = handler.lambda_handler({"key": "a.txt"}, None)
            self.assertEqual(json.loads(res["body"])["expires_in"], 300)
            kwargs = s3.return_value.generate_presigned_url.call_args.kwargs
            self.assertEqual(kwargs["ExpiresIn"], 300)
        finally:
            handler.EXPIRES = old


if __name__ == "__main__":
    unittest.main()
