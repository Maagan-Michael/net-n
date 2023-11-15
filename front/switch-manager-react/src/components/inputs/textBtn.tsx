import clsx from "clsx";
export interface TextButtonProps
  extends Partial<JSX.IntrinsicElements["button"]> {
  label: string;
}

export default function TextButton({
  label,
  className = "bg-red-400 w-full",
  ...props
}: TextButtonProps) {
  return (
    <button
      className={clsx(
        "text-white px-4 py-2 rounded-md hover:enabled:shadow-md active:enabled:shadow-inner font-light hover:enabled:bg-blue-300 disabled:bg-neutral-100 transition-all",
        className
      )}
      {...props}
    >
      {label}
    </button>
  );
}
