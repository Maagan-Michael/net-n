import { UseFormRegister } from "react-hook-form";
import TextInput from "../../../../components/inputs/TextInput";

const CustomerSection = ({ register }: { register: UseFormRegister<any> }) => (
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
);

export default CustomerSection;
