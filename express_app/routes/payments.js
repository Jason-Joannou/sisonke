import express from "express";

import {
  createGrant,
  createIncomingPayment,
  createQuote,
  createInitialOutgoingPayment,
  createRecurringGrant,
  createOutgoingPayment,
} from "../utils/paymentTypes.js";
import { validateWalletAddress } from "../utils/wallet.js";
import { executeRecurringPayments } from "../utils/payments.js";

const paymentRouter = express.Router();

paymentRouter.get("/", (req, res) => {
  res.json({
    message: "Welcome to the payments API! This is the base endpoint.",
  });
});

paymentRouter.post("/user_payment_setup", async (req, res) => {
  try {
    const {
      value,
      pool_contributions_start_date,
      walletAddressURL,
      sender_walletAddressURL,
      payment_periods,
      number_of_periods,
      payment_period_length,
      user_id,
      pool_id,
      user_contribution,
    } = req.body; // Get data from request body

    const recieverWallet = await validateWalletAddress(walletAddressURL);
    const senderWallet = await validateWalletAddress(sender_walletAddressURL);

    const grant = await createGrant(
      recieverWallet,
      "incoming-payment",
      false,
      "user",
      {},
      user_id,
      pool_id,
      null
    );

    const incomingPayment = await createIncomingPayment(
      recieverWallet,
      value,
      grant,
      pool_contributions_start_date
    );

    const quote = await createQuote(senderWallet, incomingPayment.id);

    const authParameters = {
      senderWalletAddress: senderWallet,
      poolContributionStartDate: pool_contributions_start_date,
      payment_periods: payment_periods,
      payment_period_length: payment_period_length,
      number_of_periods: number_of_periods,
      quote_id: quote.id,
      debitAmount: {
        value: user_contribution,
        assetCode: quote.debitAmount.assetCode,
        assetScale: quote.debitAmount.assetScale,
      },
      receiveAmount: {
        value: user_contribution,
        assetCode: quote.receiveAmount.assetCode,
        assetScale: quote.receiveAmount.assetScale,
      },
      user_id: user_id,
      pool_id: pool_id,
    };
    const recurringGrant = await createRecurringGrant(authParameters);

    res.json({
      recurring_grant: recurringGrant,
      continue_uri: recurringGrant.continue.uri,
      continue_token: recurringGrant.continue.access_token,
      quote_id: quote.id,
    });
  } catch (error) {
    console.log(error);
    return res
      .status(500)
      .json({ error: "An unexpected error occurred during grant creation." });
  }
});

paymentRouter.post("/initial_outgoing_payment", async (req, res) => {
  try {
    const {
      quote_id,
      continueUri,
      continueAccessToken,
      walletAddressURL,
      interact_ref,
    } = req.body;

    const authParameters = {
      quote_id: quote_id,
      continueUri: continueUri,
      continueAccessToken: continueAccessToken,
      senderWalletAddress: walletAddressURL,
      interactRef: interact_ref,
    };

    const { payment, token, manageurl } = await createInitialOutgoingPayment(
      authParameters
    );

    return res.json({ payment: payment, token: token, manageurl: manageurl });
  } catch (error) {
    console.log(error);
    return res
      .status(500)
      .json({ error: "An unexpected error occurred during grant creation." });
  }
});

paymentRouter.post("/process-recurring-payments", async (req, res) => {
  try {
    const {
      sender_wallet_address,
      receiving_wallet_address,
      manageUrl,
      previousToken,
      contributionValue,
    } = req.body; // Get data from request body

    const recurringPaymentParameters = {
      senderWalletAddress: sender_wallet_address,
      receiverWalletAddress: receiving_wallet_address,
      manageURL: manageUrl,
      previousToken: previousToken,
      contributionValue: contributionValue,
    };
    const recurringPayment = await executeRecurringPayments(
      recurringPaymentParameters
    );

    res.json(recurringPayment);
  } catch (error) {
    console.log(error);
    return res
      .status(500)
      .json({ error: "An unexpected error occurred during grant creation." });
  }
});

export default paymentRouter;
