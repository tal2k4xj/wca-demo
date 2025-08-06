Here is an example of how you could convert the provided Java code to modern Java:

First, we need to import the necessary classes from the `scheduler` package:

```java
// Assisted by watsonx Code Assistant 
import com.ibm.websphere.scheduler.BeanTaskInfo;
import com.ibm.websphere.scheduler.Scheduler;
import com.ibm.websphere.scheduler.SchedulerException;
```

Next, we can create a new class called `WASScheduler` that provides the functionality to schedule and cancel tasks:

```java
// Assisted by watsonx Code Assistant 
public class WASScheduler {
    private Scheduler scheduler;
    
    public void scheduleTask(String taskName, String cronExpression) throws SchedulerException {
        BeanTaskInfo taskInfo = new BeanTaskInfo();
        taskInfo.setTaskName(taskName);
        taskInfo.setCronExpression(cronExpression);
        taskInfo.setTargetBean("com.example.tasks.MyTask");
        taskInfo.setTargetMethod("execute");
        
        scheduler.submit(taskInfo);
    }
    
    public void cancelTask(String taskName) throws SchedulerException {
        scheduler.cancel(taskName);
    }
}
```

In the `scheduleTask` method, we create a new `BeanTaskInfo` object and set its properties, including the task name, cron expression, target bean, and target method. We then submit the task to the scheduler using the `submit` method.

In the `cancelTask` method, we simply call the `cancel` method on the scheduler and pass in the task name. This will cancel the scheduled task.

Overall, the provided code is a simple example of how to use the scheduler in WebSphere Application Server. However, by using modern Java practices, such as creating classes and using dependency injection, you can improve the code and make it easier to maintain and modify in the future.