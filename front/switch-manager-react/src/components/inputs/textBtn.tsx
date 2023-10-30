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
        "text-white px-4 py-2 rounded-md hover:shadow-md font-light hover:bg-blue-300 transition-all",
        className
      )}
      {...props}
    >
      {label}
    </button>
  );
}
