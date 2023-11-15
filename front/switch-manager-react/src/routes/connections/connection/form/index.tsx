import { useForm } from "react-hook-form";
import {
  ConnectionInput,
  SwitchInput,
  CustomerInput,
  fullConnectionUpdateInput,
} from "../../../../api/types";
import TextButton from "../../../../components/inputs/textBtn";
import { ReactComponent as Cross } from "../../../../components/icons/cross.svg";
import CustomerSection from "./CustomerSection";
import TechnicalSection from "./TechnicalSection";
import { useUpsertFullConnection } from "../../../../api/mutations/upsertFullConnection";
import { MouseEventHandler, useEffect } from "react";
import { toast, CloseButtonProps } from "react-toastify";

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
  <div className="relative col-span-1 px-4 py-20">
    <div className="absolute bg-neutral-100 rounded-full w-2 h-4/6 block"></div>
  </div>
);

const CloseButton = ({ closeToast }: CloseButtonProps) => (
  <Cross
    className="absolute w-6 h-6 top-5 right-4 cursor-pointer hover:opacity-60 transition-all text-black"
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
  const { mutate, isLoading, data: response } = useUpsertFullConnection();
  useEffect(() => {
    if (!isLoading && response) {
      if (response.errors.length) {
        toast.error("an error has occured");
        console.error(response.errors);
      } else {
        toast.success("connection updated", {
          className: "bg-neutral-100 rounded-md",
          bodyClassName: "text-black text-sm font-sans",
          closeButton: CloseButton,
        });
        goBack();
      }
    }
  }, [isLoading, response, goBack]);
  return (
    <form
      className="relative w-[600px] h-[440px] bg-white rounded-md z-10 shadow-md"
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
        className="absolute w-6 h-6 top-4 right-4 cursor-pointer hover:opacity-60 transition-all"
        onClick={goBack}
      />
      <div className="grid grid-cols-11 justify-evenly p-4">
        <TechnicalSection
          register={register}
          control={control}
          setValue={setValue}
        />
        <Separator />
        <CustomerSection register={register} />
      </div>
      <TextButton
        className="absolute bg-blue-400 w-6/12 bottom-8 left-1/2 transform -translate-x-1/2"
        label="save"
        disabled={isLoading || !isDirty}
      />
    </form>
  );
}
