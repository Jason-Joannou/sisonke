import { getEnviromentVariables } from "../enviroment/index.js";
import {
  buildGrantAccessRequest,
  buildIncomingPaymentAccessRequest,
  buildQuoteAccessRequest,
} from "./accessRequest.js";
import { client } from "./client.js";
import { randomUUID } from "crypto";
import { validateWalletAddress } from "./wallet.js";

const clientWalletAddress = getEnviromentVariables();

const { pythonServer } = getEnviromentVariables();
export const createGrant = async (
  walletAddress,
  grantType,
  withInteraction,
  dynamicEndpoint,
  paymentLimits,
  userId,
  poolId,
  quoteId
) => {
  try {
    let uri = `${pythonServer}/insurance/${dynamicEndpoint}_interactive_grant_response?user_id=${userId}&pool_id=${poolId}`;
    if (dynamicEndpoint === "adhoc") {
      uri = `${pythonServer}/insurance/${dynamicEndpoint}_payment_grant_accept?user_id=${userId}&pool_id=${poolId}&quote_id=${quoteId}`;
    }

    let accessRequest;

    if (paymentLimits) {
      accessRequest = await buildGrantAccessRequest(
        grantType,
        walletAddress.id,
        paymentLimits
      );
    } else {
      accessRequest = await buildGrantAccessRequest(
        grantType,
        walletAddress.id
      );
    }

    const interact = withInteraction
      ? {
          interact: {
            start: ["redirect"],
            finish: {
              method: "redirect",
              uri: uri,
              nonce: randomUUID(),
            },
          },
        }
      : {};

    const grantPayload = {
      access_token: {
        access: [accessRequest],
      },
      ...interact,
    };

    console.log(grantPayload);

    const grant = await client.grant.request(
      {
        url: walletAddress.authServer,
      },
      grantPayload
    );

    return grant;
  } catch (error) {
    // Log or handle the error accordingly
    console.error("Error creating grant:", error);
    throw new Error("Failed to create grant.");
  }
};

export const createIncomingPayment = async (
  walletAddress,
  value,
  grant,
  expiresAt
) => {
  try {
    const pool_contributions_start_date_converted = Date.parse(expiresAt);
    const incomingPaymentPayload = await buildIncomingPaymentAccessRequest(
      walletAddress.id,
      walletAddress.assetCode,
      walletAddress.assetScale,
      pool_contributions_start_date_converted,
      value
    );

    const incomingPayment = await client.incomingPayment.create(
      {
        url: new URL(walletAddress.id).origin,
        accessToken: grant.access_token.value,
      },
      incomingPaymentPayload
    );

    return incomingPayment;
  } catch (error) {
    // Log or handle the error accordingly
    console.error("Error creating IncomingPayment:", error);
    throw new Error("Failed to create IncomingPayment.");
  }
};

export const createQuote = async (walletAddress, incomingPaymentUrl) => {
  try {
    const grant_quote = await createGrant(walletAddress, "quote", false);
    const quotePayload = await buildQuoteAccessRequest(
      walletAddress.id,
      incomingPaymentUrl
    );
    const quote = await client.quote.create(
      {
        url: new URL(walletAddress.id).origin,
        accessToken: grant_quote.access_token.value,
      },
      quotePayload
    );
    return quote;
  } catch (error) {
    // Log or handle the error accordingly
    console.error("Error creating quote:", error);
    throw new Error("Failed to create quote.");
  }
};

export const createRecurringGrant = async (authParameters) => {
  try {
    const policy_contributions_start_date_converted = new Date(
      authParameters.poolContributionStartDate
    ).toISOString(); // Example date

    const interval = `R${authParameters.payment_periods}/${policy_contributions_start_date_converted}/P${authParameters.number_of_periods}${authParameters.payment_period_length}`;

    const paymentLimits = {
      debitAmount: authParameters.debitAmount,
      receiveAmount: authParameters.receiveAmount,
      interval: interval,
    };

    const pending_recurring_grant = await createGrant(
      authParameters.senderWalletAddress,
      "outgoing-payment",
      true,
      "user",
      paymentLimits,
      authParameters.user_id,
      authParameters.pool_id
    );

    return pending_recurring_grant;
  } catch (error) {
    console.error(error);
    throw new Error("An unexpected error occurred during authorization.");
  }
};

export const createInitialOutgoingPayment = async (authParameters) => {
  try {
    const senderWalletAddress = await validateWalletAddress(
      authParameters.senderWalletAddress
    );

    const outgoingPaymentGrant = await client.grant.continue(
      {
        accessToken: authParameters.continueAccessToken,
        url: authParameters.continueUri,
      },
      {
        interact_ref: authParameters?.interactRef,
      }
    );

    const outgoingPayment = await client.outgoingPayment.create(
      {
        url: new URL(senderWalletAddress.id).origin,
        accessToken: outgoingPaymentGrant.access_token.value,
      },
      {
        walletAddress: senderWalletAddress.id,
        quoteId: authParameters.quote_id,
      }
    );

    return {
      payment: outgoingPayment,
      token: outgoingPaymentGrant.access_token.value,
      manageurl: outgoingPaymentGrant.access_token.manage,
    };
  } catch (error) {
    console.error(error);
    throw new Error("An unexpected error occurred during authorization.");
  }
};

export const createOutgoingPayment = async (authParameters) => {
  try {
    const senderWalletAddress = await validateWalletAddress(
      authParameters.senderWalletAddress
    );

    const outgoingPayment = await client.outgoingPayment.create(
      {
        url: new URL(senderWalletAddress.id).origin,
        accessToken: authParameters?.tokenValue,
      },
      {
        walletAddress: senderWalletAddress.id,
        quoteId: authParameters.quote_id,
      }
    );

    return {
      payment: outgoingPayment,
    };
  } catch (error) {
    console.error(error);
    throw new Error("An unexpected error occurred during authorization.");
  }
};
