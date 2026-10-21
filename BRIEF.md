# Set 1 - Signed Upload

**Scenario.** Event registration needs a private S3 drop-box. Clients must upload with a short-lived presigned PUT URL issued by a Lambda Function URL (IAM auth). The code in `app/` is ready; ship it. A teammate also opened `crack-files/` for a related "upload helper" PR — review it before it merges.

Read `RULES.md` first. `<id>` below is your participant ID, for example `p07`.

---

## Part A - Build and deploy (50 points, verified live)

| What | Exact name or setting |
|---|---|
| ECR repository | `h3-<id>-upload`, scan on push **on**, tag mutability **IMMUTABLE** |
| Image | `h3-<id>-upload:v1`, built from `app/`, with env `APP_VERSION=v1` baked in |
| S3 bucket | `h3-<id>-uploads-<account-id>` using `local.account_id`, Block Public Access all **true**, default encryption **SSE-S3**, bucket policy **Deny** when `aws:SecureTransport` is `false` |
| IAM role for Lambda | `h3-<id>-upload-role` with `permissions_boundary = var.permissions_boundary_arn` |
| Log group | `/aws/lambda/h3-<id>-upload`, retention **14** days |
| Lambda | `h3-<id>-upload`, `package_type = "Image"`, `architectures = ["arm64"]`, env `UPLOAD_BUCKET`, `PRESIGN_EXPIRES` (<= 300) |
| Function URL | `authorization_type = "AWS_IAM"` |

**Tasks**
1. **A1 Package (8).** Root `Dockerfile` from `public.ecr.aws/lambda/python:3.12`, copy `app/handler.py`, CMD `handler.lambda_handler`, bake `APP_VERSION`. Tests: `python3 -m unittest discover -s app`.
2. **A2 Registry (6).** ECR + push `:v1`.
3. **A3 IaC (8).** `infra/*.tf` passes `terraform fmt -check` and `validate`. No hardcoded account IDs or keys.
4. **A4 Working deployment (18).** Invoke returns a PUT URL with `expires_in` <= 300; PUT a small object; object exists; bucket policy denies insecure transport.
5. **A5 Hardening (5).** SSE-S3, all BPA flags, log retention 14.
6. **A6 CI (5).** `.github/workflows/deploy.yml` (static): unit tests, OIDC (`role-to-assume`, `id-token: write`), build/push ECR, terraform fmt/validate/plan.

**Test it yourself**
```bash
python3 tools/check_build.py --id <id>
```

## Part B - Break: review `crack-files/` (40 points)

At least **6** planted issues across secrets, exposure, IAM/trust, containers, CI, and app code. Fix in place and document in `FINDINGS.md`. Deleting a file does not count.

## Part C - Operate (10 points)
Submit on time. Keep keys/state out of the zip. Default tags must be present. Answer the ops questions in `FINDINGS.md`.

## Submit
```bash
python3 tools/submit.py --id <id>
```
Do **not** run `terraform destroy`.
