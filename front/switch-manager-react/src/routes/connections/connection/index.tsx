import { useForm, Controller } from "react-hook-form";
import { useNavigate, useParams } from "react-router-dom";
import { useConnectionQuery } from "../../../api/queries/getConnection";
import { useCallback } from "react";
import TextButton from "../../../components/inputs/textBtn";
import TextInput from "../../../components/inputs/TextInput";
import Toggle from "../../../components/inputs/toggle";

function ConnectionForm({ data, goBack }: { data: any; goBack: () => void }) {
  const { register, handleSubmit, control } = useForm({
    defaultValues: data,
  });
  return (
    <form
      className="relative w-[600px] h-[440px] bg-white rounded-md z-10 shadow-md flex justify-evenly p-4"
      onSubmit={handleSubmit((d) => {
        console.log(d);
        goBack();
      })}
    >
      <div className="p-4 w-1/2">
        <h3 className="font-bold text-2xl">technical options</h3>
        <div className="flex flex-col gap-y-2 mt-4">
          <div className="flex flex-row gap-x-2 justify-between items-end">
            <TextInput
              register={register}
              name="switch.name"
              label="ppp"
              required
              className="grow"
            />
            <Controller
              control={control}
              name="toggled"
              render={({ field: { value, onChange } }) => (
                <Toggle
                  label=""
                  name="toggled"
                  className="w-12"
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
      <div className="p-4">
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
      <TextButton
        className="absolute bg-blue-400 w-8/12 bottom-8 left-2/12"
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
  const goBack = useCallback(() => navigate(-1), [navigate]);
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
