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
      onSuccess: (data) => {
        if (data.items.length > 0) {
          console.log(queryClient);
          const params = new URLSearchParams(window.location.search);
          queryClient.invalidateQueries({
            queryKey: "connections",
            predicate: (query) => {
              if (query.options.queryKey[0] !== "connections") {
                return false;
              }
              for (const [key, value] of Object.entries(
                query.options.queryKey[1]
              )) {
                const _value = params.get(key) || undefined;
                if (value !== _value && value) {
                  return false;
                }
              }
              console.log("worked");
              return true;
            },
          });
          queryClient.invalidateQueries([
            "connection",
            { id: data.items[0].id },
          ]);
        }
      },
    }
  );
}
