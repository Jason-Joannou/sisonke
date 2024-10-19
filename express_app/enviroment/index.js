import dotenv from "dotenv";
import path from "path";

dotenv.config();

export const getEnviromentVariables = () => {
  const variables = {
    clientWalletAddress: process.env.WALLET_ADDRESS_URL || "",
    keyID: process.env.KEY_ID || "853aa509-9d78-4354-96d1-4236cbe1236e",
    privateKeyID: process.env.PRIVATE_KEY_ID,
  };
};
