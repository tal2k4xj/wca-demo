package com.example.taskmanager;

import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;

public class TaskManager {
    private List<Task> tasks;

    public TaskManager() {
        this.tasks = new ArrayList<>();
    }

    public void addTask(String title, String description, Priority priority) {
        Task task = new Task(title, description, priority);
        tasks.add(task);
    }

    public List<Task> getTasksByPriority(Priority priority) {
        return tasks.stream()
                   .filter(task -> task.getPriority() == priority)
                   .collect(Collectors.toList());
    }

    public List<Task> getOverdueTasks() {
        LocalDateTime now = LocalDateTime.now();
        return tasks.stream()
                   .filter(task -> !task.isCompleted() && 
                                 task.getDueDate() != null && 
                                 task.getDueDate().isBefore(now))
                   .collect(Collectors.toList());
    }

    public void markTaskAsComplete(int taskId) {
        tasks.stream()
             .filter(task -> task.getId() == taskId)
             .findFirst()
             .ifPresent(Task::markComplete);
    }
} 