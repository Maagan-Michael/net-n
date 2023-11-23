import {
  Controller,
  UseFormRegister,
  Control,
  FieldValues,
  UseFormSetValue,
} from "react-hook-form";
import TextInput from "@components/inputs/TextInput";
import Toggle from "@components/inputs/toggle";
import DatePicker from "@components/inputs/datePicker";
import GPS from "@icons/gps.svg?react";
import IconRoundBtn from "@components/inputs/iconRoundBtn";
import { useTranslation } from "react-i18next";
import clsx from "clsx";

const TechnicalSection = ({
  register,
  control,
  setValue,
}: {
  register: UseFormRegister<any>;
  control: Control<FieldValues>;
  setValue: UseFormSetValue<any>;
}) => {
  const { t, i18n } = useTranslation("translation", {
    keyPrefix: "connection.form.technical",
  });
  return (
    <div className="p-4 col-span-5">
      <h3
        className={clsx(
          "font-bold text-2xl",
          i18n.dir() === "ltr" ? "text-left" : "text-right"
        )}
      >
        {t("title")}
      </h3>
      <div className="flex flex-col gap-y-2 mt-4 h-full">
        <div className="flex flex-row gap-x-2 justify-between items-end">
          <TextInput
            register={register}
            name="name"
            label={t("ppp")}
            required
            className="grow"
          />
          <TextInput
            register={register}
            name="port"
            type="number"
            label={t("port")}
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
        <DatePicker control={control} label={t("toggleDate")} />
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
          <TextInput
            register={register}
            name="switch.gpsLat"
            label={t("lat")}
          />
          <TextInput
            register={register}
            name="switch.gpsLong"
            label={t("lng")}
          />
        </div>
      </div>
    </div>
  );
};

export default TechnicalSection;
