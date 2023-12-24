import { useQuery } from "react-query";
import { CustomerOutput } from "../types";

const getCustomers = async (params: { search: string; limit: number }) => {
  const querystring = new URLSearchParams({
    search: params.search,
    limit: params.limit.toString(),
  }).toString();
  const res = await fetch(
    `${import.meta.env.VITE_API_URL}/api/v1/customers?${querystring}`
  );
  return res.json();
};

export function useCustomersQuery(params: { search: string }) {
  return useQuery<CustomerOutput[]>(
    [
      "customers",
      { search: params.search, limit: 5 },
      {
        enabled: params.search.length,
      },
    ],
    () => getCustomers({ search: params.search, limit: 5 })
  );
}
