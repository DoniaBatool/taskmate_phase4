'use client';

import React from 'react';
import { Task } from '@/lib/types';
import { Button } from './Button';
import { PriorityBadge } from './PriorityBadge';
import clsx from 'clsx';

type Props = {
  task: Task;
  onComplete: (task: Task) => void;
  onEdit: (task: Task) => void;
  onDelete: (task: Task) => void;
};

export function TaskItem({ task, onComplete, onEdit, onDelete }: Props) {
  return (
    <div className="task-item flex items-start justify-between gap-3 rounded-md p-4">
      <div className="flex flex-col gap-1">
        <div className="flex items-center gap-2">
          <span
            className={clsx('task-title text-lg font-semibold', task.completed && 'line-through completed')}
          >
            {task.title}
          </span>
          <PriorityBadge priority={task.priority} />
          {task.completed ? (
            <span className="rounded-full bg-green-500/20 px-2 py-0.5 text-xs text-green-200">Done</span>
          ) : null}
        </div>
        {task.description ? (
          <p className="task-description text-sm">{task.description}</p>
        ) : null}
      </div>
      <div className="flex gap-2">
        <Button variant="secondary" onClick={() => onComplete(task)}>
          {task.completed ? 'Uncomplete' : 'Complete'}
        </Button>
        <Button variant="ghost" onClick={() => onEdit(task)}>
          Edit
        </Button>
        <Button variant="ghost" onClick={() => onDelete(task)}>
          Delete
        </Button>
      </div>
    </div>
  );
}
