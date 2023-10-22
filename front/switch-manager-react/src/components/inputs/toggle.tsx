import { MouseEventHandler } from "react";
import { ReactComponent as ToggleOff } from "../icons/toggleOff.svg";
import { ReactComponent as ToggleOn } from "../icons/toggleOn.svg";

export default function Toggle({
  label,
  name,
  toggled,
  onChange,
}: {
  label?: string;
  name: string;
  toggled: boolean;
  onChange?: MouseEventHandler<HTMLDivElement>;
}) {
  return (
    <div onMouseDown={onChange}>
      {label && (
        <label htmlFor={name} className="">
          {label}
        </label>
      )}
      <input type="checkbox" id={name} name={name} hidden />
      {toggled ? (
        <ToggleOn className="w-9 fill-green-400" />
      ) : (
        <ToggleOff className="w-9 fill-red-500" />
      )}
    </div>
  );
}
