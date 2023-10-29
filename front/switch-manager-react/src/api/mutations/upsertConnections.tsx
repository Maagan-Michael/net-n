import { useMutation } from "react-query";
import { ConnectionInput } from "../types";

const upsertConnections = async (params: ConnectionInput) => {
  const res = await fetch(
    `${process.env.REACT_APP_API_URL}/api/v1/connections/upsert`,
    {
      method: "POST",
      body: JSON.stringify(params),
    }
  );
  return res.json();
};

export function useConnectionUpdateMutation() {
  return useMutation((params: ConnectionInput) => upsertConnections(params));
}
