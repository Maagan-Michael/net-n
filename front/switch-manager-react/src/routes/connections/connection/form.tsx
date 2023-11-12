import { useForm, Controller } from "react-hook-form";
import {
  ConnectionInput,
  SwitchInput,
  CustomerInput,
} from "../../../api/types";
import TextButton from "../../../components/inputs/textBtn";
import TextInput from "../../../components/inputs/TextInput";
import Toggle from "../../../components/inputs/toggle";
import { ReactComponent as Cross } from "../../../components/icons/cross.svg";

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
        <div className="p-4 col-span-5">
          <h3 className="font-bold text-2xl">technical options</h3>
          <div className="flex flex-col gap-y-2 mt-4 h-full">
            <div className="flex flex-row gap-x-2 justify-between items-end">
              <TextInput
                register={register}
                name="name"
                label="ppp"
                required
                className="grow"
              />
              <TextInput
                register={register}
                name="port"
                type="number"
                label="port"
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
              name="toggleDate"
              label="scheduled activation / deactivation"
            />
            <div className="flex flex-row gap-x-2">
              <TextInput
                register={register}
                name="switch.gpsLat"
                label="latitude"
              />
              <TextInput
                register={register}
                name="switch.gpsLong"
                label="longitude"
              />
            </div>
          </div>
        </div>
        <div className="relative col-span-1 px-4 py-20">
          <div className="absolute bg-neutral-100 rounded-full w-2 h-4/6 block"></div>
        </div>
        <div className="p-4 col-span-5">
          <h3 className="font-bold text-2xl">customer details</h3>
          <div className="flex flex-col gap-y-2 mt-4">
            <TextInput
              register={register}
              name="customer.firstname"
              label="firstname"
              required
            />
            <TextInput
              register={register}
              name="customer.lastname"
              label="lastname"
              required
            />
            <TextInput
              register={register}
              name="customer.type"
              label="type"
              required
            />
            <TextInput
              register={register}
              name="customer.address"
              label="address"
              required
            />
          </div>
        </div>
      </div>
      <TextButton
        className="absolute bg-blue-400 w-6/12 bottom-8 left-1/2 transform -translate-x-1/2"
        label="save"
      />
    </form>
  );
}
