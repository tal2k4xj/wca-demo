
package com.example.taskmanager;

import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;

public class TaskManager {
    private List<Task> tasks = new ArrayList<>();
    
    public void addTask(String title) {
        tasks.add(new Task(title));
    }
}
