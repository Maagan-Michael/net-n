import { useMutation, useQueryClient } from "react-query";
import { fullConnectionUpdateInput } from "../types";
import { upsertConnections } from "./upsertConnections";
import { upsertCustomers } from "./upsertCustomers";
import { upsertSwitches } from "./upsertSwitches";

const upsertFullConnection = async (params: fullConnectionUpdateInput) => {
  const { con, customer, sw } = params;
  let promises: Promise<any>[] = [];
  let _res = {
    items: [],
    errors: [],
  };
  if (con) {
    promises.push(upsertConnections(con));
  }
  if (customer) {
    promises.push(upsertCustomers(customer));
  }
  if (sw) {
    promises.push(upsertSwitches(sw));
  }
  for (let i = 0; i < promises.length; i++) {
    const p = promises[i];
    await p.then((res) => {
      _res.items = [..._res.items, ...res.items];
      _res.errors = [..._res.errors, ...res.errors];
    });
  }
  return _res;
};

export function useUpsertFullConnection() {
  const queryClient = useQueryClient();
  return useMutation(
    (params: fullConnectionUpdateInput) => upsertFullConnection(params),
    {
      onSuccess: () => queryClient.invalidateQueries(["connections"]),
    }
  );
}
