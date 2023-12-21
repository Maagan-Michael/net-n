import {
  default as DP,
  ReactDatePickerCustomHeaderProps,
} from "react-datepicker";
import { Controller, Control, FieldValues } from "react-hook-form";
import clsx from "clsx";
import { TextInputWithRef } from "./TextInput";
import Carret from "@icons/carret.svg?react";
import "react-datepicker/dist/react-datepicker.css";

const DatePickerHeader = ({
  date,
  decreaseMonth,
  increaseMonth,
}: ReactDatePickerCustomHeaderProps) => (
  <div className="font-bold text-md font-sans flex items-center justify-between">
    <Carret
      className="rotate-90 w-6 cursor-pointer hover:opacity-50 ml-2"
      onClick={decreaseMonth}
    />
    <span className="cursor-default">
      {date.toLocaleDateString("en", {
        year: "numeric",
        month: "long",
      })}
    </span>
    <Carret
      className="-rotate-90 w-6 cursor-pointer hover:opacity-50 mr-2"
      onClick={increaseMonth}
    />
  </div>
);

export default function DatePicker({
  control,
  label,
  disabled,
}: {
  control: Control<FieldValues>;
  label: string;
  disabled?: boolean;
}) {
  return (
    <Controller
      control={control}
      name="toggleDate"
      render={({ field: { value, onChange } }) => {
        let date: Date | null = null;
        if (value !== null) {
          date = new Date(value);
          date.setHours(0, 0, 0, 0);
          date.setMinutes(0, 0, 0);
        }
        return (
          <DP
            disabled={disabled}
            selected={date}
            onChange={(date: Date) => onChange(date)}
            minDate={new Date()}
            calendarClassName="shadow-md border-none"
            wrapperClassName={clsx(
              "w-full",
              "[&+div_.react-datepicker]:border-none",
              //prettier-ignore
              "[&+div_.react-datepicker\_\_header]:bg-neutral-100"
            )}
            dayClassName={(_date) => {
              // not working (overloaded by css)
              return clsx(
                "text-xs font-sans",
                date &&
                  date.getTime() === _date.getTime() &&
                  "!bg-blue-400 text-white"
              );
            }}
            customInput={
              <TextInputWithRef name="" label={label} disabled={disabled} />
            }
            renderCustomHeader={DatePickerHeader}
          />
        );
      }}
    />
  );
}
