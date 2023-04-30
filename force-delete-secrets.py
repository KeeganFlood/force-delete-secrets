import boto3
from botocore.exceptions import ClientError


def delete_all_secrets(client, secret_arn_list: list) -> None:
    """Deletes all secrets scheduled for deletion"""
    print('Deleting all Secrets scheduled for deletion....')
    for arn in secret_arn_list:
        try:
            client.delete_secret(SecretId=arn, ForceDeleteWithoutRecovery=True)
            print(f'Deleted Secret: {arn}')
        except ClientError as error:
            if error.response['Error']['Code'] == 'ResourceNotFoundException':
                print(f'The requested secret: {arn} was not found')
            elif error.response['Error']['Code'] == 'InvalidRequestException':
                print(f'The request was invalid due to: {error}')
            elif error.response['Error']['Code'] == 'InvalidParameterException':
                print(f'The request has invalid params: {error}')
            elif error.response['Error']['Code'] == 'DecryptionFailure':
                print(
                    f"The requested secret can't be decrypted using the provided KMS key: {error}")
            elif error.response['Error']['Code'] == 'InternalServiceError':
                print(f"An error occured on service side: {error}")
    return None


def get_secret_arns(client) -> list:
    """Get list of secret ARNs"""
    print('Retrieving secret ARNs....')
    response = client.list_secrets(IncludePlannedDeletion=True)
    next_token = response.get('NextToken', False)
    if 'SecretList' in response:
        results = list()
        for secret in response['SecretList']:
            if 'DeletedDate' in secret:
                results.append(secret['ARN'])
            else:
                continue
    while next_token:
        response = client.list_secrets(
            IncludePlannedDeletion=True, NextToken=next_token)
        if 'SecretList' in response:
            for secret in response['SecretList']:
                if 'DeletedDate' in secret:
                    results.append(secret['ARN'])
                else:
                    continue
        next_token = response.get('NextToken', False)
    return results


def main() -> None:
    """Force delete those pesky secrets"""
    session = boto3.Session(profile_name='default')
    client = session.client('secretsmanager')
    secret_arn_list = get_secret_arns(client)
    delete_all_secrets(client, secret_arn_list)
    print('Finished - Secrets have been deleted')


if __name__ == "__main__":
    main()
