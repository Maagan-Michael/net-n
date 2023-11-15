import {
  Controller,
  UseFormRegister,
  Control,
  FieldValues,
  UseFormSetValue,
} from "react-hook-form";
import TextInput from "../../../../components/inputs/TextInput";
import Toggle from "../../../../components/inputs/toggle";
import DatePicker from "../../../../components/inputs/datePicker";
import { ReactComponent as GPS } from "../../../../components/icons/gps.svg";
import IconRoundBtn from "../../../../components/inputs/iconRoundBtn";

const TechnicalSection = ({
  register,
  control,
  setValue,
}: {
  register: UseFormRegister<any>;
  control: Control<FieldValues>;
  setValue: UseFormSetValue<any>;
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
      <DatePicker control={control} />
      <div className="flex flex-row gap-x-2 items-center justify-between">
        <IconRoundBtn
          icon={<GPS className="w-4 h-4" />}
          className="w-12 h-8 self-end text-blue-500"
          onClick={(e) =>
            navigator.geolocation.getCurrentPosition(
              (position) => {
                setValue("switch.gpsLat", position.coords.latitude, {
                  shouldDirty: true,
                });
                setValue("switch.gpsLong", position.coords.longitude, {
                  shouldDirty: true,
                });
              },
              (err) => {
                console.error(err);
              }
            )
          }
        />
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
