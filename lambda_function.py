import generator
import boto3
from urllib.parse import urlparse


def lambda_handler(event, context):
    if "domain" in event:
        domain = event["domain"]

        try:
            if not (domain.startswith("https://") or domain.startswith("http://")):
                domain = f"null://{domain}"
            domain = urlparse(domain).hostname

            body = generator.genSecurityTxtForDomain((0, domain), return_body=True)
            if body:
                bucket = "gotsecuritytxt.com"
                key = f"gen/{domain}"

                s3r = boto3.resource("s3")
                s3Obj = s3r.Object(bucket, key)
                s3Obj.put(
                    ACL="public-read",
                    Body=body.encode("utf-8"),
                    ContentType="text/html",
                    CacheControl="public, max-age=60",
                )
            print(f"{event['domain']} - success.")
        except Exception:
            print(f"{event['domain']} - failed.")
