import { createClient } from "tigerbeetle-node";

export const client = createClient({
  cluster_id: 0n,
  replica_addresses: [process.env.TB_ADDRESS || "3000"],
});
