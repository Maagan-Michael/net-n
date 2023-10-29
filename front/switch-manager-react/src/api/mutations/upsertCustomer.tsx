import { useMutation } from "react-query";
import { CustomerInput } from "../types";

const upsertConnections = async (params: CustomerInput) => {
  const res = await fetch(
    `${process.env.REACT_APP_API_URL}/api/v1/customers/upsert`,
    {
      method: "POST",
      body: JSON.stringify(params),
    }
  );
  return res.json();
};

export function useConnectionUpdateMutation() {
  return useMutation((params: CustomerInput) => upsertConnections(params));
}
