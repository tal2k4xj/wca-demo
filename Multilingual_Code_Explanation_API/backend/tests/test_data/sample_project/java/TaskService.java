package com.example.taskmanager;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;

public class TaskService {
    private final TaskManager taskManager;
    private final TaskNotifier notifier;

    public TaskService(TaskManager taskManager, TaskNotifier notifier) {
        this.taskManager = taskManager;
        this.notifier = notifier;
    }

    public void createTask(TaskDTO taskDTO) {
        validateTask(taskDTO);
        
        taskManager.addTask(
            taskDTO.getTitle(),
            taskDTO.getDescription(),
            taskDTO.getPriority()
        );

        if (taskDTO.getPriority() == Priority.URGENT) {
            notifier.sendUrgentTaskNotification(taskDTO);
        }
    }

    public List<Task> getOverdueTasks() {
        List<Task> overdueTasks = taskManager.getOverdueTasks();
        
        if (!overdueTasks.isEmpty()) {
            notifier.sendOverdueTasksReminder(overdueTasks);
        }
        
        return overdueTasks;
    }

    private void validateTask(TaskDTO taskDTO) {
        if (taskDTO.getTitle() == null || taskDTO.getTitle().trim().isEmpty()) {
            throw new IllegalArgumentException("Task title cannot be empty");
        }

        if (taskDTO.getDueDate() != null && 
            taskDTO.getDueDate().isBefore(LocalDateTime.now())) {
            throw new IllegalArgumentException("Due date cannot be in the past");
        }
    }
} 