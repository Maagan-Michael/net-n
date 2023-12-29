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
  <div className="hidden md:flex items-center justify-center col-span-1 py-5">
    <div className="bg-neutral-100 rounded-full w-1 h-full">&nbsp;</div>
  </div>
);

const CloseButton = ({ closeToast }: CloseButtonProps) => (
  <Cross
    className="w-6 h-6 cursor-pointer hover:opacity-60 transition-all text-black"
    onClick={closeToast as unknown as MouseEventHandler<SVGElement>}
  />
);

const FormContent = ({
  register,
  control,
  setValue,
  watch,
}: {
  register: ReturnType<typeof useForm>["register"];
  control: ReturnType<typeof useForm>["control"];
  setValue: ReturnType<typeof useForm>["setValue"];
  watch: ReturnType<typeof useForm>["watch"];
}) => (
  <div className="md:grid md:grid-cols-11 justify-evenly grow">
    <div className="w-full col-span-5">
      <ConnectionSection
        register={register}
        control={control}
        setValue={setValue}
        watch={watch}
      />
      <CustomerSection register={register} setValue={setValue} watch={watch} />
    </div>
    <Separator />
    <div className="w-full col-span-5">
      <SwitchSection
        register={register}
        control={control}
        setValue={setValue}
        watch={watch}
      />
    </div>
  </div>
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
    watch,
    formState: { dirtyFields, isDirty },
    setValue,
  } = useForm({
    defaultValues: data,
  });
  const { t, i18n } = useTranslation("translation", {
    keyPrefix: "connection.form",
  });
  const {
    mutate,
    isLoading,
    data: response,
  } = useUpsertFullConnection(data.id);
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
      className="relative flex flex-col p-4 items-center w-full max-h-full md:w-[600px] md:h-[700px] bg-white rounded-md z-10 shadow-md overflow-scroll"
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
          "fixed md:absolute w-6 h-6 top-4 cursor-pointer hover:opacity-60 transition-all z-20",
          i18n.dir() === "ltr" ? "right-4" : "left-4"
        )}
        onClick={goBack}
      />
      <FormContent {...{ register, control, setValue, watch }} />
      <TextButton
        className="bg-blue-400 w-6/12"
        label={t("save")}
        disabled={isLoading || !isDirty}
        type="submit"
      />
    </form>
  );
}
