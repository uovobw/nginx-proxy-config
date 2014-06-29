import paramiko, base64
import logging
import os
import errno
import socket

class RemoteExecutor(object):
    def __init__(self, host, port, username, keyfile):
        self.host = host
        self.port = port
        self.username = username
        self.keyfile = keyfile
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.WarningPolicy())
        self.key = self.__load_ssh_key__()

    def __load_ssh_key__(self):
        if not os.path.isfile(self.keyfile):
            raise ValueError("Cannot load key identity file " + self.keyfile)
        try:
            return paramiko.RSAKey.from_private_key_file(self.keyfile)
        except IOError as e:
            logging.error("Error accessing the key file " + str(e))
            raise RuntimeError(e)
        except paramiko.PasswordRequiredException as e:
            logging.error("Key requires a password!")
            raise RuntimeError(e)
        except paramiko.SSHException as e:
            logging.error("Invalid keyfile format")
            raise RuntimeError(e)

    def connect(self):
        try:
            self.client.connect(self.host, port=self.port, pkey=self.key, username=self.username, look_for_keys=False)
            logging.info("Connected to " + self.host + " as " + self.username)
        except socket.error as e:
            logging.error("Socket error " + str(e))
            raise RuntimeError(e)
        except paramiko.BadHostKeyException as e:
            logging.error("Host key could not be verified")
            raise RuntimeError(e)
        except paramiko.SSHException as e:
            logging.error("SSH Error:" + str(e))
            raise RuntimeError(e)
        except paramiko.AuthenticationException as e:
            logging.error("Could not connect: " + str(e))
            raise RuntimeError(e)

    def send_file(self, fd, remotename):
        sftp = self.client.open_sftp()
        try:
            sftp.putfo(fd, remotename)
        except Exception as e:
            logging.error("Cannot copy file to " + remotename + " due to " + str(e))
            raise e
        sftp.close()

    def send_command(self, command):
        try:
            self.client.exec_command(command)
        except paramiko.SSHException as e:
            logging.error("Failed to execute: " + str(e))
            raise e

    def check_file_exists(self, remotename):
        sftp = self.client.open_sftp()
        try:
            sftp.stat(remotename)
        except IOError as e:
            if e.errno == errno.ENOENT:
                return False
            logging.error("Could not check remote file existance: " + str(e))
            raise e
        sftp.close()
        return True

