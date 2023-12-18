import { useForm } from "react-hook-form";
import {
  ConnectionInput,
  SwitchInput,
  CustomerInput,
  fullConnectionUpdateInput,
} from "@api/types";
import TextButton from "@components/inputs/textBtn";
import Cross from "@icons/cross.svg?react";
import CustomerSection from "./sections/customer";
import SwitchSection from "./sections/switch";
import ConnectionSection from "./sections/connection";
import { useUpsertFullConnection } from "@api/mutations/upsertFullConnection";
import { MouseEventHandler, useEffect } from "react";
import { toast, CloseButtonProps } from "react-toastify";
import { useTranslation } from "react-i18next";
import clsx from "clsx";

function getTouchedValues<T extends Record<string, any>>(
  data?: Record<string, any>,
  dirtyFields?: Record<string, any>
): T | undefined {
  if (!dirtyFields || !data) return undefined;
  const keys = Object.keys(dirtyFields);
  if (!keys.length) return undefined;
  const touchedValues: Record<string, any> = {
    id: data.id,
  };
  keys.forEach((k) => {
    if (dirtyFields[k]) {
      touchedValues[k] = data[k];
    }
  });
  return touchedValues as T;
}

function cleanInput<T extends Record<string, any>>(
  input: T
): Partial<T> | undefined {
  const keys = Object.keys(input);
  const cleanedInput: Record<string, any> = {};
  let modified = false;
  keys.forEach((k) => {
    if (input[k] !== undefined) {
      modified = true;
      cleanedInput[k] = input[k];
    }
  });
  if (!modified) return undefined;
  return cleanedInput as Partial<T>;
}

const Separator = () => (
  <div className="relative col-span-1 px-4 py-20 hidden md:block">
    <div className="absolute bg-neutral-100 rounded-full w-2 h-4/6 block"></div>
  </div>
);

const CloseButton = ({ closeToast }: CloseButtonProps) => (
  <Cross
    className="w-6 h-6 cursor-pointer hover:opacity-60 transition-all text-black"
    onClick={closeToast as unknown as MouseEventHandler<SVGElement>}
  />
);

export default function ConnectionForm({
  data,
  goBack,
}: {
  data: any;
  goBack: () => void;
}) {
  const {
    register,
    handleSubmit,
    control,
    formState: { dirtyFields, isDirty },
    setValue,
  } = useForm({
    defaultValues: data,
  });
  const { t, i18n } = useTranslation("translation", {
    keyPrefix: "connection.form",
  });
  const { mutate, isLoading, data: response } = useUpsertFullConnection();
  useEffect(() => {
    const position = i18n.dir() === "rtl" ? "top-left" : "top-right";
    if (!isLoading && response) {
      if (response.errors.length) {
        toast.error(
          t("errors.general", {
            position,
            rtl: i18n.dir() === "rtl",
          })
        );
        console.error(response.errors);
      } else {
        toast.success(t("success"), {
          className: "bg-neutral-100 rounded-md",
          bodyClassName: "text-black text-sm font-sans",
          closeButton: CloseButton,
          position,
          rtl: i18n.dir() === "rtl",
        });
        goBack();
      }
    }
  }, [isLoading, response, goBack, t, i18n]);
  return (
    <form
      className="relative flex flex-col p-4 items-center w-11/12 md:w-[600px] md:h-[500px] bg-white rounded-md z-10 shadow-md overflow-scroll"
      onSubmit={handleSubmit((d) => {
        const { switch: dsw, customer: dcustomer, ...dcon } = dirtyFields;
        let input: fullConnectionUpdateInput | undefined = {
          sw: getTouchedValues<SwitchInput>(d.switch, dsw),
          customer: getTouchedValues<CustomerInput>(d.customer, dcustomer),
          con: getTouchedValues<ConnectionInput>(d, dcon),
        };
        input = cleanInput(input);
        if (!input) return;
        mutate(input);
      })}
    >
      <Cross
        className={clsx(
          "absolute w-6 h-6 top-4 cursor-pointer hover:opacity-60 transition-all",
          i18n.dir() === "ltr" ? "right-4" : "left-4"
        )}
        onClick={goBack}
      />
      <div className="md:grid md:grid-cols-11 justify-evenly">
        <ConnectionSection
          register={register}
          control={control}
          setValue={setValue}
        />
        <Separator />
        <div className="w-full col-span-5">
          <SwitchSection
            register={register}
            control={control}
            setValue={setValue}
          />
          <CustomerSection register={register} />
        </div>
      </div>
      <TextButton
        className="bg-blue-400 w-6/12 md:absolute md:bottom-8 md:left-1/2 md:transform md:-translate-x-1/2"
        label={t("save")}
        disabled={isLoading || !isDirty}
      />
    </form>
  );
}
