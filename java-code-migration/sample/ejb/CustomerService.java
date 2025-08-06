import javax.ejb.CreateException;
import javax.ejb.EJBHome;
import javax.ejb.EJBObject;
import javax.ejb.SessionBean;
import javax.ejb.SessionContext;
import java.rmi.RemoteException;

public interface CustomerServiceHome extends EJBHome {
    CustomerService create() throws CreateException, RemoteException;
}

public interface CustomerService extends EJBObject {
    Customer findCustomer(Long id) throws RemoteException;
    void updateCustomer(Customer customer) throws RemoteException;
}

public class CustomerServiceBean implements SessionBean {
    private SessionContext context;
    
    public Customer findCustomer(Long id) {
        // Database lookup logic
        return new Customer(id);
    }
    
    public void updateCustomer(Customer customer) {
        // Database update logic
    }
    
    public void setSessionContext(SessionContext ctx) {
        context = ctx;
    }
    
    public void ejbCreate() throws CreateException {}
    public void ejbActivate() {}
    public void ejbPassivate() {}
    public void ejbRemove() {}
}

// Simple Customer class for compilation
class Customer {
    private Long id;
    public Customer(Long id) {
        this.id = id;
    }
} 