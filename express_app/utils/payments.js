import {
  createQuote,
  createIncomingPayment,
  createGrant,
  createOutgoingPayment,
} from "./paymentTypes.js";
import { validateWalletAddress } from "./wallet.js";
import { client } from "./client.js";
export const executeRecurringPayments = async (parameters) => {
  try {
    const token = await client.token.rotate({
      url: parameters.manageURL,
      accessToken: parameters.previousToken,
    });

    if (!token.access_token) {
      console.error("** Failed to rotate token.");
      throw new Error("Failed to rotate token");
    }

    const manageurl = token.access_token.manage;
    const used_token = token.access_token.value;

    const tokenAccessDetails = token.access_token.access;

    let receiveAmount = tokenAccessDetails[0]?.limits?.receiveAmount?.value;

    if (parameters.contributionValue != null) {
      receiveAmount = parameters.contributionValue;
    }

    const receiverWallet = await validateWalletAddress(
      parameters.receiverWalletAddress
    );
    const senderWallet = await validateWalletAddress(
      tokenAccessDetails[0]?.identifier ?? ""
    );

    const grant = await createGrant(
      receiverWallet,
      "incoming-payment",
      false
      // {}
    );

    const incomingPayment = await createIncomingPayment(
      receiverWallet,
      receiveAmount,
      grant,
      new Date(Date.now() + 60_000 * 10).toISOString()
    );

    const quote = await createQuote(senderWallet, incomingPayment.id);
    const authParameters = {
      senderWalletAddress: senderWallet.id,
      quote_id: quote.id,
      continueAccessToken: grant.continue.access_token.value,
      continueUri: grant.continue.uri,
      tokenValue: token.access_token.value,
    };
    const outgoingPayment = await createOutgoingPayment(authParameters);

    console.log("TOKEN INFO USED:");
    console.log(manageurl);
    console.log(used_token);

    return {
      outgoingPayment: outgoingPayment,
      manageurl: manageurl,
      token: used_token,
    };
  } catch (error) {
    console.error("Error processing recurring payments:", error);
    throw new Error("Failed to process recurring payments");
  }
};
