import clsx from "clsx";
import React, { MouseEventHandler } from "react";
import ToggleOn from "@icons/toggleOn.svg?react";

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
          toggled ? "fill-green-400 rotate-180" : "fill-red-500"
        )}
      />
    </div>
  );
}

export function IconToggle({
  label,
  name,
  toggled,
  onChange,
  className = "w-9",
  icons,
}: {
  label?: string;
  name: string;
  toggled: boolean;
  onChange?: MouseEventHandler<HTMLDivElement>;
  className?: string;
  icons: [React.FunctionComponent<any>, React.FunctionComponent<any>];
}) {
  const Icon = toggled ? icons[0] : icons[1];
  return (
    <div onMouseDown={onChange}>
      {label && (
        <label htmlFor={name} className="">
          {label}
        </label>
      )}
      <input type="checkbox" id={name} name={name} hidden />
      <Icon className={clsx(className, "cursor-pointer")} />
    </div>
  );
}
