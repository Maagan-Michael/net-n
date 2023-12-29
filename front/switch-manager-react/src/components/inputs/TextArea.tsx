import { clsx } from "clsx";
import { UseFormRegister } from "react-hook-form";
import { forwardRef } from "react";
import { useTranslation } from "react-i18next";

export interface TextAreaProps
  extends Partial<JSX.IntrinsicElements["textarea"]> {
  label: string;
  name: string;
  register?: UseFormRegister<any>;
}

export default function TextArea({
  label,
  className,
  register,
  name,
  required,
  ...props
}: TextAreaProps): JSX.Element {
  const _extraProps = register ? register(name, { required }) : {};
  const { i18n } = useTranslation();
  return (
    <div className={clsx("[&>label]:focus-within:text-blue-400", className)}>
      <label
        htmlFor={label}
        className={clsx(
          i18n.dir() === "rtl" ? "text-right" : "text-left",
          "font-thin text-xs w-full inline-block"
        )}
      >
        {label}
        {required ? "*" : ""}
      </label>
      <div className="bg-neutral-100 rounded py-1 px-2 w-full" id={label}>
        <textarea
          className="bg-transparent outline-none w-full text-xs"
          dir={i18n.dir()}
          required={required}
          {..._extraProps}
          {...props}
        />
      </div>
    </div>
  );
}

export const TextAreaWithRef = forwardRef<HTMLTextAreaElement, TextAreaProps>(
  ({ label, className, register, name, required, ...props }, ref) => {
    const _extraProps = register ? register(name, { required }) : {};
    const { i18n } = useTranslation();
    return (
      <div className={clsx("[&>label]:focus-within:text-blue-400", className)}>
        <label
          htmlFor={label}
          className={clsx(
            i18n.dir() === "rtl" ? "text-right" : "text-left",
            "font-thin text-xs w-full inline-block"
          )}
        >
          {label}
          {required ? "*" : ""}
        </label>
        <div className="bg-neutral-100 rounded py-1 px-2 w-full" id={label}>
          <textarea
            ref={ref}
            dir={i18n.dir()}
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
