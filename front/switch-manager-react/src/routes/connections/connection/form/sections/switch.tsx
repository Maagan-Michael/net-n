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
import { useEffect } from "react";

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
  useEffect(() => {
    register("switch.restrictedPorts");
    register("switch.restrictedPortsDesc");
  }, [register]);

  return (
    <DropDownSection
      label={clsx(t("restricted-ports"), `(${restrictedPorts.length})`)}
      action={
        <TextAction
          text="+"
          className="text-xl"
          type="button"
          onMouseDown={(e) => {
            e.preventDefault();
            e.stopPropagation();
            const ports = [0, ...restrictedPorts];
            const descs = ["", ...restrictedDescs];
            setValue("switch.restrictedPorts", ports, {
              shouldDirty: true,
            });
            setValue("switch.restrictedPortsDesc", descs, {
              shouldDirty: true,
            });
          }}
        />
      }
    >
      <div className="flex flex-col gap-y-1 items-center justify-between p-2 overflow-scroll max-h-[156px]">
        {restrictedPorts.map((port: any, i: number) => (
          <div
            key={`${port}-${i}`}
            className="grid grid-cols-12 gap-x-1 items-center w-full"
          >
            <TextAction
              text="-"
              type="button"
              className="text-xl col-span-1"
              onMouseDown={(e) => {
                e.preventDefault();
                e.stopPropagation();
                const ports = [...restrictedPorts];
                const descs = [...restrictedDescs];
                ports.splice(i, 1);
                descs.splice(i, 1);
                setValue("switch.restrictedPorts", ports, {
                  shouldDirty: true,
                  shouldTouch: true,
                });
                setValue("switch.restrictedPortsDesc", descs, {
                  shouldDirty: true,
                  shouldTouch: true,
                });
              }}
            />
            <TextInput
              type="number"
              min="0"
              max="65535"
              className="col-span-3"
              register={register}
              name={`switch.restrictedPorts.${i}`}
            />
            <TextInput
              className="col-span-8"
              register={register}
              name={`switch.restrictedPortsDesc.${i}`}
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
        <div className="self-end">
          <IconRoundBtn
            type="button"
            icon={<GPS className="w-4 h-4" />}
            className="w-8 h-8 text-blue-500"
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
        </div>
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
