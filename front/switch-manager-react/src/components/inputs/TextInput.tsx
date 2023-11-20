import { clsx } from "clsx";
import { UseFormRegister } from "react-hook-form";
import { forwardRef } from "react";

export interface TextInputProps
  extends Partial<JSX.IntrinsicElements["input"]> {
  label: string;
  name: string;
  register?: UseFormRegister<any>;
}

export default function TextInput({
  label,
  className,
  register,
  name,
  required,
  ...props
}: TextInputProps): JSX.Element {
  const _extraProps = register ? register(name, { required }) : {};
  return (
    <div className={clsx("[&>label]:focus-within:text-blue-400", className)}>
      <label htmlFor={label} className="font-thin text-xs">
        {label}
        {required ? "*" : ""}
      </label>
      <div className="bg-neutral-100 rounded py-1 px-2 w-full" id={label}>
        <input
          type="text"
          className="bg-transparent outline-none w-full text-xs"
          required={required}
          {..._extraProps}
          {...props}
        />
      </div>
    </div>
  );
}

export const TextInputWithRef = forwardRef<HTMLInputElement, TextInputProps>(
  ({ label, className, register, name, required, ...props }, ref) => {
    const _extraProps = register ? register(name, { required }) : {};
    return (
      <div className={clsx("[&>label]:focus-within:text-blue-400", className)}>
        <label htmlFor={label} className="font-thin text-xs">
          {label}
          {required ? "*" : ""}
        </label>
        <div className="bg-neutral-100 rounded py-1 px-2 w-full" id={label}>
          <input
            ref={ref}
            type="text"
            className="bg-transparent outline-none w-full text-xs"
            required={required}
            {..._extraProps}
            {...props}
          />
        </div>
      </div>
    );
  }
);
