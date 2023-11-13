import {
  Controller,
  UseFormRegister,
  Control,
  FieldValues,
} from "react-hook-form";
import TextInput, {
  TextInputWithRef,
} from "../../../../components/inputs/TextInput";
import Toggle from "../../../../components/inputs/toggle";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import clsx from "clsx";

const TechnicalSection = ({
  register,
  control,
}: {
  register: UseFormRegister<any>;
  control: Control<FieldValues>;
}) => (
  <div className="p-4 col-span-5">
    <h3 className="font-bold text-2xl">technical options</h3>
    <div className="flex flex-col gap-y-2 mt-4 h-full">
      <div className="flex flex-row gap-x-2 justify-between items-end">
        <TextInput
          register={register}
          name="name"
          label="ppp"
          required
          className="grow"
        />
        <TextInput
          register={register}
          name="port"
          type="number"
          label="port"
          required
          className="w-24"
        />
        <Controller
          control={control}
          name="toggled"
          render={({ field: { value, onChange } }) => (
            <Toggle
              label=""
              name="toggled"
              className="w-9 mb-1"
              toggled={value}
              onChange={(e) => onChange(!value)}
            />
          )}
        />
      </div>
      <Controller
        control={control}
        name="toggleDate"
        render={({ field: { value, onChange } }) => {
          const date = new Date(value);
          date.setHours(0, 0, 0, 0);
          date.setMinutes(0, 0, 0);
          return (
            <DatePicker
              selected={date}
              onChange={(date: Date) => onChange(date)}
              minDate={new Date()}
              calendarClassName="rounded-md shadow-md"
              dayClassName={(_date) => {
                // not working (overloaded by css)
                return clsx(
                  "text-xs font-sans",
                  date.getTime() === _date.getTime() && "bg-blue-400 text-white"
                );
              }}
              customInput={
                <TextInputWithRef
                  name=""
                  label="scheduled activation / deactivation"
                />
              }
            />
          );
        }}
      />
      {/* <TextInput
        register={register}
        name="toggleDate"
        label="scheduled activation / deactivation"
      /> */}
      <div className="flex flex-row gap-x-2">
        <TextInput register={register} name="switch.gpsLat" label="latitude" />
        <TextInput
          register={register}
          name="switch.gpsLong"
          label="longitude"
        />
      </div>
    </div>
  </div>
);

export default TechnicalSection;
