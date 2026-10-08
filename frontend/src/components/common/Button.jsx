import React from 'react';
import { LoadingSpinner } from './LoadingSpinner';

export function Button({
  children,
  variant = 'primary',
  loading = false,
  disabled = false,
  icon: Icon = null,
  onClick,
  className = '',
  type = 'button',
  ...props
}) {
  return (
    <button
      type={type}
      className={`btn btn-${variant} ${className}`}
      disabled={disabled || loading}
      onClick={onClick}
      {...props}
    >
      {loading ? (
        <LoadingSpinner size={18} />
      ) : (
        <>
          {Icon && <Icon size={18} />}
          {children}
        </>
      )}
    </button>
  );
}
