import { useForm } from "react-hook-form";
import {
  ConnectionInput,
  SwitchInput,
  CustomerInput,
} from "../../../../api/types";
import TextButton from "../../../../components/inputs/textBtn";
import { ReactComponent as Cross } from "../../../../components/icons/cross.svg";
import CustomerSection from "./CustomerSection";
import TechnicalSection from "./TechnicalSection";

function getTouchedValues<T extends Record<string, any>>(
  data?: Record<string, any>,
  dirtyFields?: Record<string, any>
): T | undefined {
  if (!dirtyFields || !data) return undefined;
  const keys = Object.keys(dirtyFields);
  if (!keys.length) return undefined;
  const touchedValues: Record<string, any> = {};
  keys.forEach((k) => {
    if (dirtyFields[k]) {
      touchedValues[k] = data[k];
    }
  });
  return touchedValues as T;
}

const Separator = () => (
  <div className="relative col-span-1 px-4 py-20">
    <div className="absolute bg-neutral-100 rounded-full w-2 h-4/6 block"></div>
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
    formState: { dirtyFields },
  } = useForm({
    defaultValues: data,
  });
  return (
    <form
      className="relative w-[600px] h-[440px] bg-white rounded-md z-10 shadow-md"
      onSubmit={handleSubmit((d) => {
        const { switch: dsw, customer: dcustomer, ...dcon } = dirtyFields;
        const input: {
          sw?: SwitchInput;
          customer?: CustomerInput;
          con?: ConnectionInput;
        } = {
          sw: getTouchedValues<SwitchInput>(d.switch, dsw),
          customer: getTouchedValues<CustomerInput>(d.customer, dcustomer),
          con: getTouchedValues<ConnectionInput>(d, dcon),
        };
        console.log(input);
        //goBack();
      })}
    >
      <Cross
        className="absolute w-6 h-6 top-4 right-4 cursor-pointer hover:opacity-60 transition-all"
        onClick={goBack}
      />
      <div className="grid grid-cols-11 justify-evenly p-4">
        <TechnicalSection register={register} control={control} />
        <Separator />
        <CustomerSection register={register} />
      </div>
      <TextButton
        className="absolute bg-blue-400 w-6/12 bottom-8 left-1/2 transform -translate-x-1/2"
        label="save"
      />
    </form>
  );
}
