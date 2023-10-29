import { useNavigate } from "react-router-dom";
import { useCallback } from "react";
import TextButton from "../../../components/inputs/textBtn";
import TextInput from "../../../components/inputs/TextInput";

export default function Connection() {
  const navigate = useNavigate();
  const goBack = useCallback(() => navigate(-1), [navigate]);
  return (
    <div className="fixed top-0 left-0 w-full h-full flex justify-center items-center">
      <div className="relative w-[600px] h-[500px] bg-white rounded-md z-10 shadow-md flex justify-evenly p-4">
        <div className="p-4">
          <h3 className="font-bold text-2xl">technical options</h3>
          <div className="flex flex-col gap-y-2 mt-4">
            <TextInput label="ppp" required />
            <TextInput label="scheduled activation / deactivation" />
            <TextInput label="location (GPS)" />
          </div>
        </div>
        <div className="p-4">
          <h3 className="font-bold text-2xl">customer details</h3>
          <div className="flex flex-col gap-y-2 mt-4">
            <TextInput label="firstname" required />
            <TextInput label="lastname" required />
            <TextInput label="type" required />
            <TextInput label="address" required />
          </div>
        </div>
        <TextButton
          className="absolute bg-blue-400 w-8/12 bottom-8 left-2/12"
          label="save"
          onClick={goBack}
        />
      </div>
      <div
        className="absolute top-0 left-0 w-full h-full backdrop-blur-md flex justify-center items-center cursor-pointer hover:backdrop-blur-sm transition-all"
        onMouseDown={goBack}
      ></div>
    </div>
  );
}
