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
}: {
  register: UseFormRegister<any>;
  control: Control<FieldValues>;
  setValue: UseFormSetValue<any>;
}) => {
  const { t, i18n } = useTranslation("translation", {
    keyPrefix: "connection.form.connection",
  });
  return (
    <FormSection title={t("title")} ltr={i18n.dir() === "ltr"}>
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
        <TextInput
          register={register}
          name="address"
          label={t("address")}
          required
        />
        <TextInput register={register} name="flat" label={t("flat")} />
        <DatePicker control={control} label={t("toggleDate")} />
        <div className="flex flex-row gap-x-2 items-center justify-between">
          <span className="text-sm font-thin  underline">
            {t("autoUpdate")} :
          </span>
          <Controller
            control={control}
            name="autoUpdate"
            render={({ field: { value, onChange } }) => (
              <Toggle
                label=""
                name="autoUpdate"
                className="w-9 mb-1"
                toggled={value}
                onChange={(e) => onChange(!value)}
              />
            )}
          />
        </div>
      </div>
    </FormSection>
  );
};

export default ConnectionSection;
