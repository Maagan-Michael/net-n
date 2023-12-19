import clsx from "clsx";
import { MouseEventHandler } from "react";

export default function TextAction({
  onMouseDown,
  text,
  className,
}: {
  text: string;
  className?: string;
  onMouseDown?: MouseEventHandler<HTMLButtonElement>;
}) {
  return (
    <button
      className={clsx(
        className,
        "text-blue-500 hover:text-blue-700 cursor-pointer"
      )}
      onMouseDown={onMouseDown}
    >
      {text}
    </button>
  );
}
