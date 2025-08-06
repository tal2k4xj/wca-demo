package scheduler;

import com.ibm.websphere.scheduler.BeanTaskInfo;
import com.ibm.websphere.scheduler.Scheduler;
import com.ibm.websphere.scheduler.SchedulerException;

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