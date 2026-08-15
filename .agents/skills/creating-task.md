---
name: creating_task
description: Instructions for creating a new Task specification in the Tasks Kanban hub.
---

# Creating a New Task

When the user asks you to create a new task or backlog item for the Sagittarius Engine, you MUST follow these specific steps to ensure the task is properly integrated into the project's Kanban hub.

**Process gate:** Do not create a new task spec if the work is clearly a direct continuation of the current active task and the user has not asked for separate tracking. In that case, continue the existing task and update its task file instead of spawning a new one.

## 1. Determine the Next Task ID

1. Read `Tasks/README.md` to view the existing tasks (completed, in-progress, and backlog).
2. Find the highest existing `TASK-XXX` ID.
3. Your new task will be the next sequential ID. For example, if the highest is `TASK-014`, your new task is `TASK-015`.

## 2. Create the Task Specification File

Create a new Markdown file in the `Tasks/backlog/` directory.

- **Naming Convention**: `TASK-XXX_lowercase_snake_case_title.md` (e.g., `TASK-015_refactor_di_container.md`).
- **File Format**: The content of the file MUST follow this exact template:

```markdown
# TASK-XXX: [Descriptive Title]

- **Status**: 📝 Planned (Backlog)
- **Priority**: [P1 - High | P2 - Medium | P3 - Low]
- **Category**: [e.g., Core Architecture / Testing / Infrastructure]
- **Issues Addressed**: [Related Issue ID or Architecture Point]

---

## 🎯 Goal
[Provide a clear, 1-2 sentence description of what this task aims to achieve and why it is important.]

---

## 📐 Key Enhancements

1. **[Enhancement 1 Title]**:
   - [Detail 1]
   - [Detail 2]
2. **[Enhancement 2 Title]**:
   - [Detail 1]

---

## 📋 Implementation Checklist

- [ ] [Specific, actionable step 1]
- [ ] [Specific, actionable step 2]
- [ ] Write unit/integration tests to verify the behavior.
```

## 3. Register the Task in README.md

You MUST update `Tasks/README.md` to make the new task visible on the Kanban board.

1. Add a new row to the **Backlog** table under `### 🔵 Backlog (Tasks/backlog/)`:

   ```markdown
   | **TASK-XXX** | [Title] | [Category] | [Priority] | [TASK-XXX_title.md](backlog/TASK-XXX_title.md) |
   ```

2. Add the file to the **Directory Layout** tree under `├── backlog/`:

   ```markdown
   │   ├── TASK-XXX_title.md
   ```

## Best Practices

- **Atomic Tasks**: Keep tasks focused on a single architectural or feature goal. If it's too large, break it down into multiple tasks.
- **Actionable Checklists**: Ensure the `Implementation Checklist` is concrete enough that another AI Agent or human developer can pick it up and execute it without needing extensive historical context.
