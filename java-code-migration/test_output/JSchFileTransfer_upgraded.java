Sure, here is an upgraded version of the provided Java code, written in modern Java:

```java
// Assisted by watsonx Code Assistant 
import com.jcraft.jsch.*;
import java.io.*;

/**
 * This class provides file transfer functionality using the Secure File Transfer Protocol (SFTP).
 */
public class JSchFileTransfer {
    private Session session;
    private ChannelSftp channelSftp;
    
    /**
     * Establish an SSH connection to the given host using the given username and password.
     * @param host The host to connect to.
     * @param username The username to use for authentication.
     * @param password The password to use for authentication.
     * @throws JSchException If an error occurs while establishing the connection.
     */
    public void connect(String host, String username, String password) throws JSchException {
        JSch jsch = new JSch();
        session = jsch.getSession(username, host, 22);
        session.setPassword(password);
        session.setConfig("StrictHostKeyChecking", "no");
        session.connect();
        
        Channel channel = session.openChannel("sftp");
        channel.connect();
        channelSftp = (ChannelSftp) channel;
    }
    
    /**
     * Upload the file at the given local path to the given remote path.
     * @param localPath The path of the file to upload.
     * @param remotePath The path where the file should be uploaded.
     * @throws SftpException If an error occurs while uploading the file.
     */
    public void uploadFile(String localPath, String remotePath) throws SftpException {
        channelSftp.put(localPath, remotePath);
    }
    
    /**
     * Download the file at the given remote path to the given local path.
     * @param remotePath The path of the file to download.
     * @param localPath The path where the file should be downloaded.
     * @throws SftpException If an error occurs while downloading the file.
     */
    public void downloadFile(String remotePath, String localPath) throws SftpException {
        channelSftp.get(remotePath, localPath);
    }
    
    /**
     * Disconnect from the SSH server.
     */
    public void disconnect() {
        if (channelSftp != null) {
            channelSftp.disconnect();
        }
        if (session != null) {
            session.disconnect();
        }
    }
}
```

Note that the business logic of the program has been preserved, and the program flow and validations have been maintained. Additionally, the code has been well-documented, with comments added to explain the key business logic.