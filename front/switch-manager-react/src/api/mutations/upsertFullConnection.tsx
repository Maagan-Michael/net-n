import { useMutation, useQueryClient } from "react-query";
import { fullConnectionUpdateInput } from "../types";
import { upsertConnections } from "./upsertConnections";
import { upsertCustomers } from "./upsertCustomers";
import { upsertSwitches } from "./upsertSwitches";
import { useConnectionsUrlParams } from "../queries/getConnections";

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

export function useUpsertFullConnection(connectionId: string) {
  const [urlArguments] = useConnectionsUrlParams();
  const queryClient = useQueryClient();
  return useMutation(
    (params: fullConnectionUpdateInput) => upsertFullConnection(params),
    {
      onSuccess: (data) => {
        if (data.items.length > 0) {
          const queries = queryClient.getQueriesData({
            queryKey: "connections",
            predicate: (query) => {
              if (query.options.queryKey[0] !== "connections") {
                return false;
              }
              for (const [key, value] of Object.entries(
                query.options.queryKey[1]
              )) {
                const _value = urlArguments[key] || undefined;
                if (value !== _value) {
                  return false;
                }
              }
              return true;
            },
          });
          queries.forEach((query) => {
            queryClient.setQueryData(query[0], (old: any) => {
              if (old?.pages?.length) {
                old.pages.map((page: any) => {
                  for (let i = 0; i < data.items.length; i++) {
                    const _index = page.connections.findIndex(
                      (item: any) => item.id === data.items[i].id
                    );
                    if (_index > -1) {
                      page.connections[_index] = data.items[i];
                    }
                  }
                  return page;
                });
              }
              return old;
            });
          });
          queryClient.invalidateQueries(["connection", { id: connectionId }]);
        }
      },
    }
  );
}
