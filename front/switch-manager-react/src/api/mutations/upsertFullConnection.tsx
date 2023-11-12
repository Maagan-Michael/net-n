import { useMutation } from "react-query";
import { fullConnectionUpdateInput } from "../types";
import { upsertConnections } from "./upsertConnections";
import { upsertCustomers } from "./upsertCustomers";
import { upsertSwitches } from "./upsertSwitches";

const upsertFullConnection = async (params: fullConnectionUpdateInput) => {
  const { con, customer, sw } = params;
  let promises: Promise<any>[] = [];
  if (con) {
    promises.push(upsertConnections(con));
  }
  if (customer) {
    promises.push(upsertCustomers(customer));
  }
  if (sw) {
    promises.push(upsertSwitches(sw));
  }
  return Promise.all(promises);
};

export function useUpsertFullConnection() {
  return useMutation((params: fullConnectionUpdateInput) =>
    upsertFullConnection(params)
  );
}
