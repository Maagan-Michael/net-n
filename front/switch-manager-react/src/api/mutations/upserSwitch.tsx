import { useMutation } from "react-query";
import { SwitchInput } from "../types";

const upserSwitches = async (params: SwitchInput) => {
  const res = await fetch(
    `${process.env.REACT_APP_API_URL}/api/v1/customers/upsert`,
    {
      method: "POST",
      body: JSON.stringify(params),
    }
  );
  return res.json();
};

export function useSwitchUpdateMutation() {
  return useMutation((params: SwitchInput) => upserSwitches(params));
}
