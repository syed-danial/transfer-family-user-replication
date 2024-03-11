import boto3
import os

def fetch_all_users_from_server(transfer_client, server_id):
    try:
        response = transfer_client.list_users(ServerId=server_id)
        user_list= response['Users']
        
        detailed_users = []
        for user in user_list:
            user_details = transfer_client.describe_user(ServerId=server_id, UserName=user['UserName'])
            detailed_users.append(user_details['User'])
        return detailed_users
    except Exception as e:
        print(f"Exception fetching users from server '{server_id}': {e}")
        return []

def user_exists_on_server(transfer_client, server_id, user):
    try:
        transfer_client.describe_user(ServerId=server_id, UserName=user['UserName'])
        return True
    except transfer_client.exceptions.ResourceNotFoundException:
        return False
    except Exception as e:
        print(f"Exception checking user existence on host server for '{user['UserName']}': {e}")
        return False

def create_user_on_dest_server(server_id, user, region):
    transfer_client = boto3.client('transfer', region_name=region)

    if not user_exists_on_server(transfer_client, server_id, user):
        if 'HomeDirectory' not in user:
            user['HomeDirectory'] = '/'
        try:
            create_user_params = {
                'ServerId': server_id,
                'UserName': user['UserName'],
                'HomeDirectory': user['HomeDirectory'],
                'Role': user['Role']
            }
            if 'Policy' in user:
                create_user_params['Policy'] = user['Policy']

            transfer_client.create_user(**create_user_params)
            print(f"User '{user['UserName']}' created on the destination server.")
        except Exception as e:
            print(f"Exception creating user on destination server for '{user['UserName']}': {e}")
    else:
        print(f"User '{user['UserName']}' already exists on the destination server.")

    
    for ssh_public_key in user['SshPublicKeys']:
        try:
            transfer_client.import_ssh_public_key(
                ServerId=server_id,
                UserName=user['UserName'],
                SshPublicKeyBody=ssh_public_key['SshPublicKeyBody']
            )
            print(f"Updated Public Keys for user '{user['UserName']}'")
        except Exception as e:
            print(f"Exception importing public ssh keys as: {e}")



def lambda_handler(event, context):
    host_server_id = os.environ['HOST_SERVER_ID']
    dest_server_id = os.environ['DEST_SERVER_ID']
    source_region = os.environ['SOURCE_REGION']
    dest_region = os.environ['DEST_REGION']
    
    source_client = boto3.client('transfer', region_name=source_region)
    source_users = fetch_all_users_from_server(source_client, host_server_id)

    for source_user in source_users:
        create_user_on_dest_server(dest_server_id, source_user, dest_region)
            
    return {
        'statusCode': 200,
        'body': 'Execution complete.'
    }
