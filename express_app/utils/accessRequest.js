export const buildGrantAccessRequest = async (
  grantType,
  walletId,
  paymentLimits
) => {
  switch (grantType) {
    case "incoming-payment":
      return {
        type: "incoming-payment",
        actions: ["read", "create", "complete"],
      };
    case "outgoing-payment":
      return {
        type: "outgoing-payment",
        actions: ["read", "create", "read-all", "list", "list-all"],
        identifier: walletId,
        limits: paymentLimits ? { ...paymentLimits } : undefined,
      };
    case "quote":
      return {
        type: "quote",
        actions: ["create", "read", "read-all"],
      };
    default:
      throw new Error("Invalid grant type provided.");
  }
};

export const buildIncomingPaymentAccessRequest = async (
  walletId,
  walletAssetCode,
  walletAssetScale,
  expiryDate,
  value
) => {
  return {
    walletAddress: walletId,
    incomingAmount: {
      value: value,
      assetCode: walletAssetCode,
      assetScale: walletAssetScale,
    },
    expiresAt: new Date(expiryDate + 48 * 60 * 60 * 1000).toISOString(),
  };
};

export const buildQuoteAccessRequest = async (walletID, incomingPaymentUrl) => {
  return {
    method: "ilp",
    walletAddress: walletID,
    receiver: incomingPaymentUrl,
  };
};
