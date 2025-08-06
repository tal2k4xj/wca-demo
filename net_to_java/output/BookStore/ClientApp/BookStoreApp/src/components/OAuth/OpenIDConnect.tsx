// Assisted by watsonx Code Assistant 
// watsonx Code Assistant did not check whether this code suggestion might be similar to third party code.
import React, { useState } from 'react';
import { useAuth0 } from '@auth0/auth0-react';

const OpenIDConnect = () => {
  const { isAuthenticated, loginWithRedirect } = useAuth0();

  const handleLogin = () => {
    loginWithRedirect();
  };

  return (
    <div>
      {!isAuthenticated && (
        <button onClick={handleLogin}>Login with OAuth/OpenID Connect</button>
      )}
    </div>
  );
};

export default OpenIDConnect;