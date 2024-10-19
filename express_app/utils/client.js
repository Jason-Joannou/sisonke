import { createAuthenticatedClient } from "@interledger/open-payments";
import { getEnviromentVariables } from "../enviroment/index.js";

const { walletAddressUrl, keyID, privateKeyID } = getEnviromentVariables();

export const client = await createAuthenticatedClient({
  walletAddressUrl,
  keyId: keyID,
  privateKey: privateKeyID,
  validateResponses: false,
});
