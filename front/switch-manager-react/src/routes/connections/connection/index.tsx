import { useForm, Controller } from "react-hook-form";
import { useNavigate, useParams } from "react-router-dom";
import { useConnectionQuery } from "../../../api/queries/getConnection";
import {
  ConnectionInput,
  SwitchInput,
  CustomerInput,
} from "../../../api/types";
import { useCallback } from "react";
import TextButton from "../../../components/inputs/textBtn";
import TextInput from "../../../components/inputs/TextInput";
import Toggle from "../../../components/inputs/toggle";
import { ReactComponent as Cross } from "../../../components/icons/cross.svg";

function ConnectionForm({ data, goBack }: { data: any; goBack: () => void }) {
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
          sw: undefined,
          customer: undefined,
          con: undefined,
        };
        // generate inputs with only touched fields
        if (dsw) {
          let sw: SwitchInput = { id: d.switch.id };
          Object.keys(dsw).forEach((k) => {
            //@ts-ignore
            sw[k] = d.switch[k as keyof SwitchInput];
          });
          input.sw = sw;
        }
        if (dcustomer) {
          let customer: CustomerInput = { id: d.customer.id };
          Object.keys(dcustomer).forEach((k) => {
            //@ts-ignore
            customer[k] = d.customer[k as keyof CustomerInput];
          });
          input.customer = customer;
        }
        const dconKeys = Object.keys(dcon);
        if (dconKeys.length) {
          let con: ConnectionInput = { id: d.id };
          Object.keys(dcon).forEach((k) => {
            //@ts-ignore
            con[k] = d.customer[k as keyof CustomerInput];
          });
          input.con = con;
        }
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

export default function Connection() {
  const { id } = useParams<{ id: string }>();
  if (!id) {
    // todo handle error route
    throw new Error("no id");
  }
  const { data, isLoading } = useConnectionQuery({ id });
  const navigate = useNavigate();
  const goBack = useCallback(
    () => navigate(`/${window.location.search}`),
    [navigate]
  );
  if (isLoading) {
    return <div>loading...</div>;
  }
  return (
    <div className="fixed top-0 left-0 w-full h-full flex justify-center items-center">
      <ConnectionForm data={data} goBack={goBack} />
      <div
        className="absolute top-0 left-0 w-full h-full backdrop-blur-md flex justify-center items-center cursor-pointer hover:backdrop-blur-sm transition-all"
        onMouseDown={goBack}
      ></div>
    </div>
  );
}
