import {
  Controller,
  UseFormRegister,
  Control,
  FieldValues,
  UseFormSetValue,
} from "react-hook-form";
import TextInput from "@components/inputs/TextInput";
import Toggle from "@components/inputs/toggle";
import Lock from "@icons/lock.svg?react";
import Unlock from "@icons/lock-open.svg?react";
import GPS from "@icons/gps.svg?react";
import IconRoundBtn from "@components/inputs/iconRoundBtn";
import { useTranslation } from "react-i18next";
import FormSection from "./section";
import TextArea from "@/components/inputs/TextArea";
import DropDownSection from "@/components/dropdownSection";
import TextAction from "@/components/inputs/textAction";

const SwitchSection = ({
  register,
  control,
  setValue,
}: {
  register: UseFormRegister<any>;
  control: Control<FieldValues>;
  setValue: UseFormSetValue<any>;
}) => {
  const { t, i18n } = useTranslation("translation", {
    keyPrefix: "connection.form.switch",
  });
  return (
    <FormSection title={t("title")} ltr={i18n.dir() === "ltr"}>
      <TextInput
        register={register}
        name="switch.id"
        label={t("ID")}
        disabled
      />
      <TextInput
        register={register}
        name="switch.ip"
        label={t("ip")}
        disabled
      />
      <TextInput
        register={register}
        name="switch.name"
        label={t("name")}
        required
      />
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
        <TextInput register={register} name="switch.gpsLat" label={t("lat")} />
        <TextInput register={register} name="switch.gpsLong" label={t("lng")} />
      </div>
      <div className="flex flex-col gap-x-2 w-full">
        <TextArea
          register={register}
          name="switch.description"
          label={t("description")}
        />
      </div>
      <div className="flex flex-row gap-x-2 items-center justify-between">
        {" "}
        <span className="text-sm font-thin  underline">
          {t("restricted")} :
        </span>
        <Controller
          control={control}
          name="switch.restricted"
          render={({ field: { value, onChange } }) => (
            <Toggle
              label=""
              name="switch.restricted"
              className="w-9 mb-1"
              toggled={value}
              onChange={(e) => onChange(!value)}
            />
          )}
        />
      </div>
      <div>
        <DropDownSection
          label={t("restricted-ports")}
          action={<TextAction text="+" className="text-xl" />}
        ></DropDownSection>
      </div>
    </FormSection>
  );
};

export default SwitchSection;
