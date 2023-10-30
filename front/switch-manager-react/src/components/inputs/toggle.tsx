import clsx from "clsx";
import { MouseEventHandler } from "react";
import { ReactComponent as ToggleOn } from "../icons/toggleOn.svg";

export default function Toggle({
  label,
  name,
  toggled,
  onChange,
  className = "w-9",
}: {
  label?: string;
  name: string;
  toggled: boolean;
  onChange?: MouseEventHandler<HTMLDivElement>;
  className?: string;
}) {
  return (
    <div onMouseDown={onChange}>
      {label && (
        <label htmlFor={name} className="">
          {label}
        </label>
      )}
      <input type="checkbox" id={name} name={name} hidden />
      <ToggleOn
        className={clsx(
          "cursor-pointer transition-colors",
          className,
          toggled ? "fill-green-400" : "rotate-180 fill-red-500"
        )}
      />
    </div>
  );
}
