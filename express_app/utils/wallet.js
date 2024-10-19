import { client } from "./client.js";
import { OpenPaymentsClientError } from "@interledger/open-payments";

export const validateWalletAddress = async (walletAddress) => {
  try {
    if (walletAddress.startsWith("$")) {
      walletAddress = walletAddress.replace("$", "https://");
    }
    const response = await client.walletAddress.get({
      url: walletAddress,
    });

    return response;
  } catch (error) {
    if (error instanceof OpenPaymentsClientError) {
      const invalidWalletError = {
        ...error,
        status: error.status || 500,
        description: error.description || "Unknown error occurred",
      };
      // Throw the error so it can be caught by the calling function
      throw invalidWalletError;
    }

    console.error("Unexpected error type:", error);
    throw new Error("An unexpected error occurred during wallet validation.");
  }
};
