# Force Delete
Python Script to Force Delete AWS Secrets Manager Secrets. With the release of [Boto3 1.26.40](https://github.com/boto/boto3/blob/develop/CHANGELOG.rst#:~:text=Added%20owning%20service%20filter%2C%20include%20planned%20deletion%20flag%2C%20and%20next%20rotation%20date%20response%20parameter%20in%20ListSecrets.) you can now pass an `IncludePlannedDeletion` flag to the Secrets Manager `list_secrets` operation. This allows you to target Secrets that have been scheduled for deletion. Useful for removing secrets from your environment during development. This is the same as setting the recovery window to 0 days, or using the AWS CLI command `aws secretsmanager delete-secret --secret-id <value> --force-delete-without-recovery`. If you are producing a lot of secrets during development, this eliminates the need to grab the ARNs each time you would need to run the equivalent CLI command. 

# Requirements
- An active AWS Account
- Python3
- Install the [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
- Boto3 version >= 1.26.40 -- `pip install boto3`
- AWS CLI configuration settings using `aws configure`. This script uses the `default` profile in `.aws/credentials`. If you have a profile with a different name, update the profile name. Example: `session = boto3.Session(profile_name='development')`

# Usage
- Clone the repo 
- Run `python3 force-delete-secrets.py`

# Note
This script is not intended for use in production. The use of this parameter causes the operation to skip the normal recovery window before the permanent deletion that Secrets Manager would normally impose with the RecoveryWindowInDays parameter. If you delete a secret with the ForceDeleteWithoutRecovery parameter, then you have no opportunity to recover the secret. You lose the secret permanently.