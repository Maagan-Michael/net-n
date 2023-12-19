import { useEffect, useState } from "react";
import {
  Controller,
  UseFormRegister,
  Control,
  FieldValues,
  UseFormSetValue,
} from "react-hook-form";
import TextInput from "@components/inputs/TextInput";
import Toggle, { IconToggle } from "@components/inputs/toggle";
import Lock from "@icons/lock.svg?react";
import Unlock from "@icons/lock-open.svg?react";
import DatePicker from "@components/inputs/datePicker";
import { useTranslation } from "react-i18next";
import FormSection from "./section";

const ConnectionSection = ({
  register,
  control,
  setValue,
  shouldLock,
}: {
  register: UseFormRegister<any>;
  control: Control<FieldValues>;
  setValue: UseFormSetValue<any>;
  shouldLock: boolean;
}) => {
  const [locked, setLocked] = useState(true);
  const { t, i18n } = useTranslation("translation", {
    keyPrefix: "connection.form.connection",
  });
  useEffect(() => setLocked(true), [shouldLock]);
  const disabled = shouldLock && locked;
  return (
    <FormSection
      title={t("title")}
      ltr={i18n.dir() === "ltr"}
      rightComponent={
        shouldLock && (
          <IconToggle
            name="locked"
            icons={[Lock, Unlock]}
            toggled={locked}
            onChange={(e) => setLocked(!locked)}
          />
        )
      }
    >
      <div className="flex flex-col gap-y-2 mt-4 h-full">
        <div className="flex flex-row gap-x-2 justify-between items-end">
          <TextInput
            disabled={disabled}
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
            className="w-24"
            disabled
          />
          <Controller
            control={control}
            name="toggled"
            disabled={disabled}
            render={({ field: { value, onChange } }) => (
              <Toggle
                label=""
                name="toggled"
                className="w-9 mb-1"
                toggled={value}
                onChange={(e) => onChange(!value)}
                disabled={disabled}
              />
            )}
          />
        </div>
        <TextInput
          register={register}
          name="address"
          label={t("address")}
          disabled={disabled}
          required
        />
        <TextInput
          register={register}
          name="flat"
          label={t("flat")}
          disabled={disabled}
        />
        <DatePicker
          control={control}
          label={t("toggleDate")}
          disabled={disabled}
        />
        <div className="flex flex-row gap-x-2 items-center justify-between">
          <span className="text-sm font-thin  underline">
            {t("autoUpdate")} :
          </span>
          <Controller
            control={control}
            name="autoUpdate"
            disabled={disabled}
            render={({ field: { value, onChange } }) => (
              <Toggle
                label=""
                name="autoUpdate"
                className="w-9 mb-1"
                toggled={value}
                onChange={(e) => onChange(!value)}
                disabled={disabled}
              />
            )}
          />
        </div>
      </div>
    </FormSection>
  );
};

export default ConnectionSection;
