import javax.xml.rpc.ServiceException;
import javax.xml.rpc.server.ServiceLifecycle;

public interface HelloService extends java.rmi.Remote {
    String sayHello(String name) throws java.rmi.RemoteException;
}

public class HelloServiceImpl implements HelloService, ServiceLifecycle {
    public String sayHello(String name) throws RemoteException {
        return "Hello " + name + "!";
    }

    public void init(Object context) throws ServiceException {
        // Initialization code
    }

    public void destroy() {
        // Cleanup code
    }
} 