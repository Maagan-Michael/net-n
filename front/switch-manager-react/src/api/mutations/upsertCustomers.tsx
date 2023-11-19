import { useMutation } from "react-query";
import { CustomerInput } from "../types";

export const upsertCustomers = async (params: CustomerInput) => {
  const res = await fetch(
    `${import.meta.env.VITE_API_URL}/api/v1/customers/upsert`,
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

export function useCustomersUpdateMutation() {
  return useMutation((params: CustomerInput) => upsertCustomers(params));
}
