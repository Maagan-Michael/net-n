import clsx from "clsx";
export interface TextButtonProps
  extends Partial<JSX.IntrinsicElements["button"]> {
  label: string;
}

export default function TextButton({
  label,
  className,
  ...props
}: TextButtonProps) {
  return (
    <button
      className={clsx(
        "bg-red-400 text-white px-4 py-2 rounded-md hover:shadow-md w-full font-light hover:bg-blue-300 transition-all",
        className
      )}
      {...props}
    >
      {label}
    </button>
  );
}
