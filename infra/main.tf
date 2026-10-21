# Set 1 - Signed Upload. Write your infrastructure here.
# See BRIEF.md for the exact names that are verified.
#
# TODO ECR repository         ${local.prefix}-upload (IMMUTABLE, scan on push)
# TODO S3 bucket              ${local.prefix}-uploads-${local.account_id} (BPA all true, SSE-S3, deny SecureTransport=false)
# TODO IAM role + policy      ${local.prefix}-upload-role (permissions_boundary!)
# TODO CloudWatch log group   /aws/lambda/${local.prefix}-upload (retention 14)
# TODO Lambda function        ${local.prefix}-upload (package_type = "Image", arm64)
# TODO Lambda function URL    authorization_type = "AWS_IAM"
# Env: UPLOAD_BUCKET, PRESIGN_EXPIRES (<=300), APP_VERSION
