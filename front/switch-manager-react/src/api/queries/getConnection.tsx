import { useQuery } from "react-query";
import { ConnectionOutput } from "../types";

const fetchConnection = async (params: { id: string }) => {
  const res = await fetch(
    `${import.meta.env.VITE_API_URL}/api/v1/connections/${params.id}`
  );
  return res.json();
};

export function useConnectionQuery(params: { id: string }) {
  return useQuery<ConnectionOutput>(["connection", { id: params.id }], () =>
    fetchConnection(params)
  );
}
