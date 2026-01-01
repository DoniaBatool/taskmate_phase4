'use client';

import React from 'react';
import clsx from 'clsx';

type Props = {
  children: React.ReactNode;
  className?: string;
};

export function Card({ children, className }: Props) {
  return (
    <div className={clsx('card-theme rounded-lg p-6 shadow-lg transition-all duration-300', className)}>
      {children}
    </div>
  );
}
