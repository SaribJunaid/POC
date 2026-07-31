/** Decrypted GHL user context - Agency level */
export interface GHLUserContext {
  userId: string;
  companyId: string;
  role: string;
  type: 'agency' | 'location';
  userName: string;
  email: string;
  isAgencyOwner: boolean;
  activeLocation?: string;
  versionId: string;
  appStatus: string;
  whitelabelDetails: {
    domain: string;
    logoUrl: string;
  };
}

/** Response from POST /sso/decrypt */
export interface SSOLoginResponse {
  token_type: 'Bearer';
  access_token: string;
  expires_in: number;
}

/** Response from GET /sso/session */
export interface SSOSessionResponse {
  status: 'success' | 'error';
  data: {
    userId: string;
    companyId: string;
    role: string;
    type: string;
    activeLocation?: string;
  };
}
