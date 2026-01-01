/**
 * PriorityBadge Component
 *
 * Displays a color-coded priority badge for tasks.
 * Supports three priority levels: high (red), medium (yellow), low (green).
 * WCAG 2.1 AA compliant with 4.5:1 contrast ratio in both light and dark modes.
 */

interface PriorityBadgeProps {
  priority: 'high' | 'medium' | 'low';
}

export function PriorityBadge({ priority }: PriorityBadgeProps) {
  const className = `priority-badge-${priority} px-2 py-0.5 rounded-full text-xs font-medium`;
  const label = priority.charAt(0).toUpperCase() + priority.slice(1);

  return (
    <span
      className={className}
      aria-label={`Priority: ${label}`}
      role="status"
    >
      {label}
    </span>
  );
}
