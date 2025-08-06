package com.example.taskmanager;

import java.util.List;

public interface TaskNotifier {
    void sendUrgentTaskNotification(TaskDTO task);
    void sendOverdueTasksReminder(List<Task> tasks);
} 