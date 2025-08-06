
public class TaskManager {
    private List<Task> tasks = new ArrayList<>();
    
    public void addTask(String title) {
        tasks.add(new Task(title));
    }
}
