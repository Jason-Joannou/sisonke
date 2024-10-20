import { createAuthenticatedClient } from "@interledger/open-payments";
import { getEnviromentVariables } from "../enviroment/index.js";

const { clientWalletAddress, keyID, privateKeyID } = getEnviromentVariables();
console.log({ clientWalletAddress, keyID, privateKeyID });

export const client = await createAuthenticatedClient({
  walletAddressUrl: clientWalletAddress,
  keyId: keyID,
  privateKey: privateKeyID,
  validateResponses: false,
});
