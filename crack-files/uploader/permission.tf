resource "aws_lambda_permission" "url" {
  statement_id  = "AllowPublicInvoke"
  action        = "lambda:InvokeFunctionUrl"
  function_name = "upload-helper"
  principal     = "*"
}
