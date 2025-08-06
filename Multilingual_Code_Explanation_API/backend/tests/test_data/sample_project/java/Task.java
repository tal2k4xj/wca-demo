package com.example.taskmanager;

import java.time.LocalDateTime;
import java.util.concurrent.atomic.AtomicInteger;

public class Task {
    private static final AtomicInteger idGenerator = new AtomicInteger(0);
    
    private final int id;
    private String title;
    private String description;
    private Priority priority;
    private LocalDateTime createdAt;
    private LocalDateTime dueDate;
    private boolean completed;
    private LocalDateTime completedAt;

    public Task(String title, String description, Priority priority) {
        this.id = idGenerator.incrementAndGet();
        this.title = title;
        this.description = description;
        this.priority = priority;
        this.createdAt = LocalDateTime.now();
        this.completed = false;
    }

    public void markComplete() {
        this.completed = true;
        this.completedAt = LocalDateTime.now();
    }

    // Getters and setters
    public int getId() { return id; }
    
    public String getTitle() { return title; }
    public void setTitle(String title) { this.title = title; }
    
    public String getDescription() { return description; }
    public void setDescription(String description) { this.description = description; }
    
    public Priority getPriority() { return priority; }
    public void setPriority(Priority priority) { this.priority = priority; }
    
    public LocalDateTime getDueDate() { return dueDate; }
    public void setDueDate(LocalDateTime dueDate) { this.dueDate = dueDate; }
    
    public boolean isCompleted() { return completed; }
    public LocalDateTime getCompletedAt() { return completedAt; }
    public LocalDateTime getCreatedAt() { return createdAt; }
} 