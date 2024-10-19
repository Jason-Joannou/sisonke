import id from "tigerbeetle-node";
import { client } from "./createClient";

// Need to store in db

export const createPersonEntityAccount = async () => {
  try {
    // person Entities will be ledger 1
    const personEntityAccount = {
      id: id(), // Generate a unique Tyger Beetle account ID
      debits_pending: 0n,
      debits_posted: 0n,
      credits_pending: 0n,
      credits_posted: 0n,
      user_data_128: 0n,
      user_data_64: 0n,
      user_data_32: 0,
      reserved: 0,
      ledger: 1,
      code: 718,
      flags: 0,
      timestamp: 0n,
    };

    const accountErrors = await client.createAccounts([personEntityAccount]);

    if (accountErrors > 0) {
      console.log(`Failed to create ${accountErrors} account(s).`);
      throw new Error(`Failed to create ${accountErrors} account(s).`);
    }
  } catch (error) {
    console.log(error);
  }
};

export const createPoolEntities = async () => {
  try {
    // pool entities will be ledger 2
    const contributionEntityAccount = {
      id: id(), // Generate a unique Tyger Beetle account ID
      debits_pending: 0n,
      debits_posted: 0n,
      credits_pending: 0n,
      credits_posted: 0n,
      user_data_128: 0n,
      user_data_64: 0n,
      user_data_32: 0,
      reserved: 0,
      ledger: 2,
      code: 718,
      flags: 0,
      timestamp: 0n,
    };

    const accountErrors = await client.createAccounts([personEntityAccount]);

    if (accountErrors > 0) {
      console.log(`Failed to create ${accountErrors} account(s).`);
      throw new Error(`Failed to create ${accountErrors} account(s).`);
    }
  } catch (error) {
    console.log(error);
  }
};
