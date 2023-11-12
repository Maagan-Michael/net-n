import { useMutation } from "react-query";
import { SwitchInput } from "../types";

export const upsertSwitches = async (params: SwitchInput) => {
  const res = await fetch(
    `${process.env.REACT_APP_API_URL}/api/v1/customers/upsert`,
    {
      method: "POST",
      body: JSON.stringify(params),
      headers: {
        "Content-Type": "application/json",
      },
    }
  );
  return res.json();
};

export function useSwitchUpdateMutation() {
  return useMutation((params: SwitchInput) => upsertSwitches(params));
}
