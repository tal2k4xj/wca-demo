```
// Assisted by watsonx Code Assistant 
`import javax.jws.WebService;
import javax.jws.WebMethod;

@WebService(name="HelloService", targetNamespace="http://example.com/hello")
public interface HelloService {
    @WebMethod
    String sayHello(String name);
}

public class HelloServiceImpl implements HelloService {
    @Override
    public String sayHello(String name) {
        return "Hello " + name + "!";
    }
} `
```