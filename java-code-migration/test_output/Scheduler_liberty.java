Here is the Liberty implementation of the WebSphere scheduler:

```java
// Assisted by watsonx Code Assistant 
package scheduler;

import javax.enterprise.concurrent.ManagedScheduledExecutorService;
import javax.enterprise.concurrent.ManagedScheduledFuture;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.ScheduledFuture;
import java.util.concurrent.TimeUnit;

public class WASScheduler {
    private ScheduledExecutorService scheduler;
    
    public void scheduleTask(String taskName, String cronExpression) {
        Runnable task = new MyTask();
        ScheduledFuture<?> future = scheduler.schedule(task, 0, TimeUnit.SECONDS);
    }
    
    public void cancelTask(String taskName) {
        // TODO: find the ScheduledFuture for the task and cancel it
    }
}
```

Note that the implementation is incomplete as it does not handle persistence settings, transaction boundaries, error handling, and other important aspects of a real-world implementation. However, it provides a good starting point for migrating the WebSphere scheduler to Liberty.