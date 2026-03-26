import { useId, useState } from "react";

type PasswordFieldProps = {
  name: string;
  placeholder: string;
  required?: boolean;
  defaultValue?: string;
};

export function PasswordField({ name, placeholder, required = false, defaultValue }: PasswordFieldProps) {
  const [isVisible, setIsVisible] = useState(false);
  const inputId = useId();

  return (
    <div className="password-field">
      <input
        defaultValue={defaultValue}
        id={inputId}
        name={name}
        placeholder={placeholder}
        required={required}
        type={isVisible ? "text" : "password"}
      />
      <button
        aria-controls={inputId}
        aria-label={isVisible ? `Hide ${placeholder}` : `Show ${placeholder}`}
        className="password-toggle"
        onClick={() => setIsVisible((current) => !current)}
        type="button"
      >
        <svg aria-hidden="true" className="password-toggle-icon" viewBox="0 0 24 24">
          <path
            d="M2 12C4.8 7.8 8.1 5.7 12 5.7S19.2 7.8 22 12c-2.8 4.2-6.1 6.3-10 6.3S4.8 16.2 2 12Z"
            fill="none"
            stroke="currentColor"
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth="1.8"
          />
          <circle
            cx="12"
            cy="12"
            fill="none"
            r="3.2"
            stroke="currentColor"
            strokeWidth="1.8"
          />
          {isVisible ? null : (
            <path
              d="M4 4l16 16"
              fill="none"
              stroke="currentColor"
              strokeLinecap="round"
              strokeWidth="1.8"
            />
          )}
        </svg>
      </button>
    </div>
  );
}
