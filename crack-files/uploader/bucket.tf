resource "aws_s3_bucket" "stats" {
  bucket = "team-upload-stats"
}

resource "aws_s3_bucket_policy" "stats" {
  bucket = aws_s3_bucket.stats.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Principal = "*"
      Action    = ["s3:GetObject"]
      Resource  = ["${aws_s3_bucket.stats.arn}/*"]
    }]
  })
}
