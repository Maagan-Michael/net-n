import { useMutation } from "react-query";
import { ConnectionInput } from "../types";

export const upsertConnections = async (params: ConnectionInput) => {
  const res = await fetch(
    `${process.env.REACT_APP_API_URL}/api/v1/connections/upsert`,
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

export function useConnectionUpdateMutation() {
  return useMutation((params: ConnectionInput) => upsertConnections(params));
}
