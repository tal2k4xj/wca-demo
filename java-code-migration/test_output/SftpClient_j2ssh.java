```
// Assisted by watsonx Code Assistant 
import com.sshtools.j2ssh.SshClient;
import com.sshtools.j2ssh.authentication.AuthenticationProtocolState;
import com.sshtools.j2ssh.authentication.PasswordAuthenticationClient;
import com.sshtools.j2ssh.configuration.ConfigurationManager;
import com.sshtools.j2ssh.configuration.SshServerConfiguration;
import com.sshtools.j2ssh.connection.ConnectionException;
import com.sshtools.j2ssh.connection.channel.ChannelException;
import com.sshtools.j2ssh.sftp.SftpClient;
import com.sshtools.j2ssh.transport.publickey.PublicKeyAuthenticationClient;

import java.io.File;
import java.io.IOException;

public class J2SSHFileTransfer {
    private SshClient sshClient;
    private SftpClient sftpClient;

    public void connect(String host, String username, String password) throws ConnectionException {
        sshClient = new SshClient();
        sshClient.setHost(host);
        sshClient.setPort(22);
        sshClient.setAuthenticationProtocol(new PasswordAuthenticationClient(username, password));
        sshClient.connect();
    }

    public void uploadFile(String localPath, String remotePath) throws ChannelException, IOException {
        sftpClient = sshClient.createSftpClient();
        sftpClient.put(new File(localPath), remotePath);
    }

    public void downloadFile(String remotePath, String localPath) throws ChannelException, IOException {
        sftpClient = sshClient.createSftpClient();
        sftpClient.get(remotePath, new File(localPath));
    }

    public void disconnect() {
        if (sftpClient != null) {
            sftpClient.close();
        }
        if (sshClient != null) {
            sshClient.disconnect();
        }
    }
}
```