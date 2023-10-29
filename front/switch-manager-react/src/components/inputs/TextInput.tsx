import { UseFormRegister } from "react-hook-form";

export interface TextInputProps
  extends Partial<JSX.IntrinsicElements["input"]> {
  label: string;
  name: string;
  register: UseFormRegister<any>;
}

export default function TextInput({
  label,
  className,
  register,
  name,
  required,
  ...props
}: TextInputProps): JSX.Element {
  return (
    <div className="[&>label]:focus-within:text-blue-400">
      <label htmlFor={label} className="font-thin text-sm">
        {label}
        {required ? "*" : ""}
      </label>
      <div className="bg-neutral-100 rounded-md p-2 mt-1" id={label}>
        <input
          type="text"
          className="bg-transparent outline-none w-full text-sm"
          required={required}
          {...register(name, { required })}
        />
      </div>
    </div>
  );
}
