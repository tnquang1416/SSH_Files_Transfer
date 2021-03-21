import sys
import os
import paramiko


def upload_dir(sftp, source_path, target_path):
    try:
        print('Uploading %s to %s...' % (source_path, target_path))
        sftp.mkdir(path=target_path, mode=511)
    except IOError:
        print('IOError: Look like directory existed.')
    
    for item in os.listdir(source_path):
        temp_path = os.path.join(source_path, item)
        if os.path.isfile(temp_path):
            sftp.put(temp_path, '%s/%s' % (target_path, item))
        else:
            upload_dir(sftp, temp_path, '%s/%s' % (target_path, item))
    
    # end for
# end upload_dir

def main():
    print(os.name)

if __name__ == '__main__':
    try:
        path = 'ssh.tnquang.com'
        port = 22
        username = 'tnquang'
        password = '@my_pass'
        target_path = 'db'
        source_path = 'local_db'
        # Connect to remote host
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(path, port=port, username=username, password=password)

        # Setup sftp connection and transmit this script
        sftp = client.open_sftp()
        
        # visit all dir and file then uploading
        upload_dir(sftp, source_path, target_path)
        
        sftp.close()
        client.close()
    except IndexError:
        print("Index Error")

    # All done here.
    main()
