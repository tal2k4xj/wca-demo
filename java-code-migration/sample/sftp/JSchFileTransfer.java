import com.jcraft.jsch.*;
import java.io.*;

public class JSchFileTransfer {
    private Session session;
    private ChannelSftp channelSftp;
    
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
    
    public void uploadFile(String localPath, String remotePath) throws SftpException {
        channelSftp.put(localPath, remotePath);
    }
    
    public void downloadFile(String remotePath, String localPath) throws SftpException {
        channelSftp.get(remotePath, localPath);
    }
    
    public void disconnect() {
        if (channelSftp != null) {
            channelSftp.disconnect();
        }
        if (session != null) {
            session.disconnect();
        }
    }
} 