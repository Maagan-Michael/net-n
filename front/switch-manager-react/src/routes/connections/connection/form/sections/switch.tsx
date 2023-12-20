import {
  Controller,
  UseFormRegister,
  Control,
  FieldValues,
  UseFormSetValue,
  UseFormWatch,
} from "react-hook-form";
import TextInput from "@components/inputs/TextInput";
import Toggle from "@components/inputs/toggle";
import GPS from "@icons/gps.svg?react";
import IconRoundBtn from "@components/inputs/iconRoundBtn";
import { useTranslation } from "react-i18next";
import FormSection from "./section";
import TextArea from "@/components/inputs/TextArea";
import DropDownSection from "@/components/dropdownSection";
import TextAction from "@/components/inputs/textAction";
import clsx from "clsx";

const RestrictedPorts = ({
  register,
  setValue,
  watch,
}: {
  register: UseFormRegister<any>;
  control: Control<FieldValues>;
  setValue: UseFormSetValue<any>;
  watch: UseFormWatch<any>;
}) => {
  const { t } = useTranslation("translation", {
    keyPrefix: "connection.form.switch",
  });
  const restrictedPorts = watch("switch.restrictedPorts");
  const restrictedDescs = watch("switch.restrictedPortsDesc");
  return (
    <DropDownSection
      label={clsx(t("restricted-ports"), `(${restrictedPorts.length})`)}
      action={
        <TextAction
          text="+"
          className="text-xl"
          onMouseDown={(e) => {
            e.preventDefault();
            e.stopPropagation();
            setValue("switch.restrictedPorts", [0, ...restrictedPorts]);
            setValue("switch.restrictedPortsDesc", ["", ...restrictedDescs]);
          }}
        />
      }
    >
      <div className="flex flex-col gap-y-1 items-center justify-between p-2 overflow-scroll max-h-[156px]">
        {restrictedPorts.map((port: any, i: number) => (
          <div
            key={`${port}-${i}`}
            className="grid grid-cols-12 gap-x-1 items-center"
          >
            <TextAction
              text="-"
              className="text-xl col-span-1"
              onMouseDown={(e) => {
                e.preventDefault();
                e.stopPropagation();
                setValue("switch.restrictedPorts", [
                  ...restrictedPorts.slice(0, i),
                  ...restrictedPorts.slice(i + 1),
                ]);
                setValue("switch.restrictedPortsDesc", [
                  ...restrictedDescs.slice(0, i),
                  ...restrictedDescs.slice(i + 1),
                ]);
              }}
            />
            <TextInput
              type="number"
              min="0"
              max="65535"
              className="col-span-3"
              register={register}
              name={`switch.restrictedPorts[${i}]`}
            />
            <TextInput
              className="col-span-8"
              register={register}
              name={`switch.restrictedPortsDesc[${i}]`}
            />
          </div>
        ))}
      </div>
    </DropDownSection>
  );
};

const SwitchSection = ({
  register,
  control,
  setValue,
  watch,
}: {
  register: UseFormRegister<any>;
  control: Control<FieldValues>;
  setValue: UseFormSetValue<any>;
  watch: UseFormWatch<any>;
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
      <RestrictedPorts
        register={register}
        control={control}
        setValue={setValue}
        watch={watch}
      />
    </FormSection>
  );
};

export default SwitchSection;
