import datetime

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from botocore.signers import CloudFrontSigner
from decouple import config


def rsa_signer(message):
    CF_PRIVATE_KEY_FILE = config('CF_PRIVATE_KEY_FILE')
    with open(CF_PRIVATE_KEY_FILE, 'rb') as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
            backend=default_backend()
        )
    return private_key.sign(message, padding.PKCS1v15(), hashes.SHA1())


def get_cdn_presigned_url(url, expiration):
    
    PUBLIC_KEY_ID = config('CF_SIGNER_PUBLIC_KEY')

    cloudront_signer = CloudFrontSigner(PUBLIC_KEY_ID, rsa_signer)

    signed_url = cloudront_signer.generate_presigned_url(
        url,
        date_less_than=expiration
    )

    return signed_url


if __name__ == "__main__":
    # Assuming default distribution  at root of bucket(`/`)
    CF_DOMAIN_NAME = config('CF_DOMAIN_NAME')
    key = 'apps/test/newt.png'
    url = f"{CF_DOMAIN_NAME}/{key}"

    expiration = datetime.datetime.now() + datetime.timedelta(minutes=5)
    print(expiration.strftime("%m/%d/%Y, %H:%M:%S"))
    signed_url = get_cdn_presigned_url(
        url=url,
        expiration=expiration,
    )

    print(f"PRIVATE: {signed_url}")
