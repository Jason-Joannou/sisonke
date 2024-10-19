import { client } from "./createClient.js";

export const getDebitsPosted = async (accountId) => {
  try {
    const result = await client.lookupAccounts([accountId]);
    if (result.length > 0) {
      return result[0].debits_posted;
    }

    return -1;
  } catch (error) {
    console.log(error);
    return -1;
  }
};

export const getCreditsPosted = async (accountId) => {
  try {
    const result = await client.lookupAccounts([accountId]);
    if (result.length > 0) {
      return result[0].credits_posted;
    }

    return -1;
  } catch (error) {
    console.log(error);
    return -1;
  }
};

export const lookUpTransfer = async (transferId) => {
  try {
    const transfer = await client.lookupTransfers([transferId]);
    if (transfer.length > 0) {
      return transfer[0];
    }
    return -1;
  } catch (error) {
    console.log(error);
    return -1;
  }
};
