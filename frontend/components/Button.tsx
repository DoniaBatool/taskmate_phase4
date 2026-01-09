'use client';

import clsx from 'clsx';
import React from 'react';

type Props = React.ButtonHTMLAttributes<HTMLButtonElement> & {
  variant?: 'primary' | 'secondary' | 'ghost';
};

export function Button({ variant = 'primary', className, children, ...props }: Props) {
  const styles = clsx(
    'rounded-md px-4 py-2.5 text-sm font-medium transition-colors disabled:opacity-60 disabled:cursor-not-allowed min-h-[44px] inline-flex items-center justify-center',
    variant === 'primary' && 'btn-primary',
    variant === 'secondary' && 'btn-secondary',
    variant === 'ghost' && 'btn-ghost',
    className,
  );
  return (
    <button className={styles} {...props}>
      {children}
    </button>
  );
}
