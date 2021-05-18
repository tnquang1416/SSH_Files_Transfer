import sys
import os
import paramiko
import argparse


file_list = []

parser = argparse.ArgumentParser()
parser.add_argument("--port", type=str, default='123456', help="")
parser.add_argument("--host", type=str, default='ssh.tnquang.com', help="")
parser.add_argument("--username", type=str, default='tnquang', help="")
parser.add_argument("--password", type=str, default='12345', help="")
parser.add_argument("--source", type=str, help="")
parser.add_argument("--target", type=str, help="")

opt = parser.parse_args()


def print_msg():
    msg = ''
    msg += 'Download from %s to %s ' % (opt.source, opt.target)
    msg += 'on %s at port %s.' % (opt.host, opt.port)

    print(msg)

# end print_msg

def download_dir(sftp, src_path, tg_path):
    print('--> Downloading %s to %s...' % (src_path, tg_path))
    os.makedirs(tg_path, exist_ok=True);
    
    for item in sftp.listdir(src_path):
        temp = '%s/%s' % (src_path, item)
        temp_tg = '%s/%s' % (tg_path, item)
        
        if is_sftp_file(sftp, temp):
            sftp.get(temp, temp_tg)
        else:
            download_dir(sftp, temp, temp_tg)

# end download_dir

def is_sftp_file(sftp, path):
    lstatout=str(sftp.lstat(path)).split()[0]
    if 'd' in lstatout: return False
    
    return True
    
# end is_sftp_file

def download(sftp):
    if(os.path.isfile(opt.source)):
        sftp.get(opt.source, opt.target)
        return;

    download_dir(sftp, opt.source, opt.target)
    
# end download

def main():
    pass

if __name__ == '__main__':
    print(opt)
    print_msg()
    try:
        # Connect to remote host
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(opt.host, port=opt.port, username=opt.username, password=opt.password)

        # Setup sftp connection and transmit this script
        sftp = client.open_sftp()
        
        download(sftp)
        
        sftp.close()
        client.close()
    except IndexError:
        print("Index Error")

    main()
